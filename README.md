## Log Analysis

> *This is the third project of the [Full Stack Web Development Nanodegree](https://in.udacity.com/course/full-stack-web-developer-nanodegree--nd004/) program, from Udacity.*



### Overview

This project aim to create an internal reporting tool that will analyzed the provided database, answering three specific questions using good code practices for both technologies involved, Python (PEP-8) and SQL (one single query per question).



The questions were: 

- What are the three most popular articles of all time?
- Who are the most popular article authors of all time?
- On which day did more than 1% of requests lead to errors?



### Installation Requirements

To run this project successfully you'll need:

1. [Python 2](https://www.python.org/downloads/)
2. [psycopg module](http://initd.org/psycopg/download/)
3. [https://www.postgresql.org/download/](https://www.postgresql.org/download/) 
4. [newsdata (database)](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)



### Used setup

I used a vagrant setup into a virtual machine, which included the database and the needed libraries. To have the exact same setup, you must:

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [vagrant](https://www.vagrantup.com/downloads.html);

Clone this [repository](https://github.com/udacity/fullstack-nanodegree-vm);

In your command prompter (bash) Navigate to the vagrant subdirectory in the repository folder and type `vagrant up`. If it's the first time, vagrant will download Linux and install it. When you get your prompt back, follow it by the command `vagrant ssh` to log in to your vagrant development environment.

Download and place the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into the vagrant directory inside the repository folder. Use `psql -d news -f newsdata.sql` to setup the database.



### How to run

To run your script: `python <script_name>.py` while logged into your development environment, assuming that it has all the requirements correctly installed.



### News database

The news database is a large database containing information regarding newspaper articles. It's composed by three tables, as follows:



#### authors

| Column | Type    | Modifiers                                            |
| ------ | ------- | ---------------------------------------------------- |
| name   | text    | not null                                             |
| bio    | text    |                                                      |
| id     | integer | not null default nextval('authors_id_seq'::regclass) |



#### articles

| Column | Type                     | Modifiers                                             |
| ------ | ------------------------ | ----------------------------------------------------- |
| author | integer                  | not null                                              |
| title  | text                     | not null                                              |
| slug   | text                     | not null                                              |
| lead   | text                     | not null                                              |
| body   | text                     |                                                       |
| time   | timestamp with time zone | default now()                                         |
| id     | integer                  | not null default nextval('articles_id_seq'::regclass) |



#### log

| Column | Type                     | Modifiers                                        |
| ------ | ------------------------ | ------------------------------------------------ |
| path   | text                     |                                                  |
| ip     | text                     |                                                  |
| method | text                     |                                                  |
| status | text                     |                                                  |
| time   | timestamp with time zone | default now()                                    |
| id     | integer                  | not null default nextval('log_id_seq'::regclass) |





### Create Views

Two views were created for the third and last SQL query: `logviews` and `logerrors`. 



#### Logviews

```
CREATE VIEW logviews as SELECT time::date as day, count(*) as views from log GROUP BY time::date;
```

```
select * from logviews limit 10;

    day     | views
------------+-------
 2016-07-01 | 38705
 2016-07-02 | 55200
 2016-07-03 | 54866
 2016-07-04 | 54903
 2016-07-05 | 54585
 2016-07-06 | 54774
 2016-07-07 | 54740
 2016-07-08 | 55084
 2016-07-09 | 55236
 2016-07-10 | 54489
(10 rows)
```



#### Logerrors

```
CREATE VIEW logerrors as SELECT time::date as day, count(*) as errors from log WHERE status like '%404%' GROUP BY time::date;
```

```
select * from logerrors limit 10;

    day     | errors
------------+--------
 2016-07-31 |    329
 2016-07-06 |    420
 2016-07-17 |   1265
 2016-07-12 |    373
 2016-07-10 |    371
 2016-07-25 |    391
 2016-07-14 |    383
 2016-07-28 |    393
 2016-07-30 |    397
 2016-07-22 |    406
(10 rows)
```



### Functions in `lognewsdb.py`

- **`querying_db()`** -> connects to the PostgreSQL database returning the results of the given query
- **`writing_log()`** -> writes messages to the log file
- **`top_three_articles()`** -> process the results of the first query, addressing the first question
- **`top_authors()`** -> process the results of the second query, addressing the second question
- **`over_1percent_daily_errors()`** -> process the results of the third query, addressing the third question



### Output

You can check the output text file [here](https://github.com/mguidoti/FSND-p3-log_analysis/blob/master/lognews.txt). 
