import psycopg2
import string
import calendar


def most_visited():
    # This function finds the three most viewed articles
    # on the newspaper website
    db = psycopg2.connect("dbname=news")  # Connect to the database
    cursor = db.cursor()
    # Create view most_visited_article with two columns
    # path, and num which is the count of each time a path is visited
    # for the first three heighest visited path excluding the '/' the root path
    cursor.execute('''create view most_visited_article as select path,
    count(*) as num from log group by path
    order by num desc limit 3 offset 1''')
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
    db = psycopg2.connect("dbname=news")  # Connect to the database
    cursor = db.cursor()
    # Create view most_visited_article with two columns
    # path, and num which is the count of each time a path is visited
    # excluding the '/' the root path
    cursor.execute('''create view most_visited_article as select path, count(*) as num from log
    group by path order by num desc offset 1''')
    # Create view subview which is an inner join of the articles table and
    # the most_visited_article view table with columns, author, title, num
    # to find the name of the author later
    cursor.execute('''create view subview as select author,title,num from articles,
    most_visited_article where  most_visited_article.path like
    '%' || articles.slug order by num desc''')
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
    db = psycopg2.connect("dbname=news")  # Connect to the database
    cursor = db.cursor()
    # Create view datepart with two columns status and date, where date
    # is the date part of timestamp
    # To count according to days not according to timestamp
    cursor.execute('''create view datepart as select time,
    time::timestamp::date as date, status from log''')
    # Create view error_tb with two columns date and
    # error_code which is the count of the error status code on each day
    cursor.execute('''create view error_tb as select date, count(*) as error_code
    from datepart where status like '4%'
    group by date order by error_code desc''')
    # Create view status_tb with two columns date and status_code
    # which is the count of all status codes on each day
    cursor.execute('''create view status_tb as select date, count(*) as status_code
    from datepart group by date order by status_code desc''')
    # Create view percentage_tb that is an inner join between the error_tb
    # and status_tb with three columns, error_code
    # status_code, and one of the error percenage
    cursor.execute('''create view percentage_tb as select status_tb.date,
    error_code, status_code,
    (cast(error_code as decimal)/cast(status_code as decimal))*100
    as error_percent from error_tb, status_tb
    where error_tb.date=status_tb.date order by error_code desc''')
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
