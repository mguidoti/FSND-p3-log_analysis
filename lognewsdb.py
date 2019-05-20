#!/usr/bin/env python2

import psycopg2
import os

# Used SQL queries

# Query 01
# Question: What are the three most popular articles of all time?
query_articles = """select articles.title, articles.id, count(*) as num
                    from articles, log where log.path like concat('%',
                    articles.slug) group by articles.id order by num
                    desc limit 3;"""

# Query 02
# Question: Who are the most popular article authors of all time?
query_authors = """select authors.name, count(*) as num from authors,
                    articles, log where authors.id = articles.author
                    and log.path like concat('%', articles.slug) group
                    by authors.name order by num desc;"""

# Query 03
# Question: On which day did more than 1% of requests lead to errors?
query_errors = """select * from (select day, round(cast((errors/
                    views)*100 as numeric), 2) as percent from (select
                    logviews.day, logviews.views::float,
                    logerrors.errors::float from logviews, logerrors
                    where logviews.day = logerrors.day) as summary) as
                    summary2 where percent >= 1.0 order by percent
                    desc;"""


# Function for querying data from the database
def querying_db(my_query):
    connect = psycopg2.connect(database="news")
    c = connect.cursor()
    c.execute(my_query)
    results = c.fetchall()
    connect.close()

    return results


# Writes a message into the log file
def writing_log(message):

    if os.path.isfile("lognews.txt"):
        log_file = open("lognews.txt", "a")

    else:
        log_file = open("lognews.txt", "w")

    # Checks if the file is empty to add the headers first
    if os.stat("lognews.txt").st_size == 0:
        log_file.write("Log Analysis of the Newsdata Database")
        log_file.write("\n-------------------------------------\n")
        log_file.write(message)

    # Writes all other messages
    else:
        log_file.write("\n")
        log_file.write(message)

    log_file.close()


# Print the top three articles of all time - Question 01
def top_three_articles():
    results = querying_db(query_articles)

    writing_log("\n1. Top 3 articles of all time:\n")

    for each in results:
        writing_log("* '{}', with {} views".format(each[0], each[2]))


# Print the top authors of all time - Question 02
def top_authors():
    results = querying_db(query_authors)

    writing_log("\n2. Top authors of all time:\n")

    for each in results:
        writing_log("* {}, with {} views".format(each[0], each[1]))


# Print the days with >= 1% of bad requests - Question 03
def over_1percent_daily_errors():
    results = querying_db(query_errors)

    writing_log("\n3. Days with >=1.0% of bad requests:\n")

    for each in results:
        writing_log("* {} had {} of error".format(each[0], each[1]))


if __name__ == '__main__':
    top_three_articles()
    top_authors()
    over_1percent_daily_errors()
