#!/usr/bin/env python3
import psycopg2
import string
import calendar

DBNAME = 'news'

def db_connect():
    '''
    Creates and returns a connection to the database defined by DBNAME, as well as
    cursor for the database
    Returns:
    db, c - a tuple. The first element is a connection to the database.
    The second element is a cursor for the database.
    '''
    db = psycopg2.connect(dbname = DBNAME)
    c = db.cursor()
    return(db,c)

def execute_query(query):
    '''
    execute_query takes an SQL query as a parameter. Executes the query and returns
    the results as a list of tuplesself.
    args:
    query - an SQL query statement to be executed.
    returns:
    A list of tuples containing the result of the query.
    '''
    c = db_connect()[1]
    c.execute(query)
    db = db_connect()[0]
    result = c.fetchall()
    return(result)
    db.close()

def most_visited():
    # This function finds the three most viewed articles
    # on the newspaper website

    # Join the articles table with the most_visited_article view table
    # and select the title for each path
    cursor.execute('''select title, most_visited_article.num
    from articles, most_visited_article where
    most_visited_article.path like '%' || articles.slug order by num desc''')
    result = cursor.fetchall()
    db.close()
    print"Three Most Visited Articles:\n1)", result[0][0],
    print" - ", result[0][1], "views"
    print"2)", result[1][0], " - ", result[1][1], "views"
    print"3)", result[2][0], " - ", result[2][1], "views"


def popular_authors():
    # This function finds the most popular authors and thier maximum views



    # Join the authors table with a subquery that finds the maximum number of
    # views for each author and order the results according to views
    cursor.execute('''select name, subquery.num
    from (select author,count(*) as nom, max(num) as num from subview
    group by author order by author) as subquery, authors
    where subquery.author = authors.id order by num desc''')
    result = cursor.fetchall()
    db.close()
    print"Most Popular Authors:\n1)", result[0][0], " - ",
    print result[0][1], "views"
    print"2)", result[1][0], " - ", result[1][1], "views"
    print"3)", result[2][0], " - ", result[2][1], "views"
    print"3)", result[3][0], " - ", result[3][1], "views"


def error_percent():
    # This function find the percenage error if it exceeds 1% for a day

    # Find the error percent where it is above 1%
    cursor.execute('''select date, round(error_percent,1) from percentage_tb
    where error_percent > 1.00''')
    result = cursor.fetchall()
    db.close()
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
