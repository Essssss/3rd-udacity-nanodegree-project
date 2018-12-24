#!/usr/bin/env python
import psycopg2
import string
import calendar

DBNAME = 'news'


def db_connect():
    '''
    Creates and returns a connection to the database defined by DBNAME,
    as well as cursor for the database
    Returns:
    db, c - a tuple. The first element is a connection to the database.
    The second element is a cursor for the database.
    '''
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    return(db, c)


def execute_query(query):
    '''
    execute_query takes an SQL query as a parameter. Executes the query
    and returns the results as a list of tuplesself.
    args:
    query - an SQL query statement to be executed.
    returns:
    A list of tuples containing the result of the query.
    '''
    db, c = db_connect()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return(result)


def most_visited():
    '''
    This function finds the three most viewed articles
    on the newspaper website
    '''

    '''Run the first function view from the README.md file first'''
    # Join the articles table with the most_visited_article view table
    # and select the title for each path
    result = execute_query('''select title, most_visited_article.num
    from articles, most_visited_article where
    most_visited_article.path like '%' || articles.slug
    order by num desc limit 3''')

    n = len(result)
    print"Three Most Visited Articles:"
    for x in range(0, n):
        print x+1, ")", result[x][0], " - ", result[x][1], "views"


def popular_authors():
    '''
    This function finds the most popular authors and the sum of their views
    and order the authors them according to the heighest views
    '''
    '''Run the second function views from the README.md file first'''
    # Join the authors table with a subquery that finds the maximum number of
    # views for each author and order the results according to views
    result = execute_query('''select name, subquery.num
    from (select author,count(*) as nom, sum(num) as num from subview
    group by author order by author) as subquery, authors
    where subquery.author = authors.id order by num desc''')

    n = len(result)
    print"Most Popular Authors:"
    for x in range(0, n):
        print x+1, ")", result[x][0], " - ", result[x][1], "views"


def error_percent():
    '''
    This function finds the percentage error if it exceeds 1% for a day
    '''

    '''Run the third function views from the README.md file first'''
    # Find the error percent where it is above 1%
    result = execute_query('''select date, round(error_percent,1) from percentage_tb
    where error_percent > 1.00''')
    date = result[0][0]
    date = str(date)
    # Clean date from dashes
    cleandate = date.replace('-', ' ')
    # If it is less than 10 remove the preceding zero
    if int(cleandate[5:7]) < 10:
        month = cleandate[6:7]
    else:
        month = cleandate[5:7]
    # Convert month number to name
    monthname = calendar.month_name[int(month)]
    print"Error Percentage:\n", monthname, cleandate[7:],
    print",", cleandate[:4], "-", result[0][1], "% errors."

most_visited()
popular_authors()
error_percent()
