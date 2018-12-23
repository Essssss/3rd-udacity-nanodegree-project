# Logs Analysis Project
This is a reporting tool built in Python `newsdb.py` that answers some question as shown in the text file `An example of the program's output.txt`.

## Prepare the software and the data
* You should have the virtual machine `VirtualBox` installed on your device.
* [Download Vagrant](https://www.vagrantup.com/downloads.html) and go to the same directory where you downloaded vagrant and bring up the virtual machine with `vagrant up` and log into it with `vagrant ssh`.
* [Download the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it.
* Move the file `newsdata.sql` to the shared vagrant directory.
* From the virtual machine `cd` into the vagrant directory and load the date `psql -d news -f newsdata.sql`.
* Move the file of the reporting tool program `newsdb.py` to the vagrant directory and run the program `python newsdb.py`.
* The program will run and will extract the desired information from the database as shown in the example text file.

## Description of the code in `newsdb.py`
This program consists of five functions. The first two functions are `db_connect()` and `execute_query()`the first one connects to the database and the second one executes queries and they are used in each of the functions below.
* First question "What are the most popular three articles of all time?" is answered by this function `most_visited()`.
* Second question "Who are the most popular article authors of all time?" is answered by this function `popular_authors()`.
* Third question "On which days did more than 1% of requests lead to errors?" is answered by this function `error_percent()`.
Further explanation is in the comments in the `newsdb.py` file.

## The create view commands
Connect to the database `psql -d news`, and Run these commands before running the `newsdb.py`.
#### Views in the function `most_visited()`
* `create view most_visited_article as select path,
  count(*) as num from log group by path
  order by num desc offset 1`
View explanation:
Create view most_visited_article with two columns path, and num which is the count of each time a path is visited for the first three highest visited path excluding the '/' the root path.

#### Views in the function `popular_authors()`
* The first view is needed, because the following view is dependent on the first view above.
* `create view subview as select author,title,num from articles,
  most_visited_article where  most_visited_article.path like
  '%' || articles.slug order by num desc`
View explanation:
Create view subview which is an inner join of the articles table and the most_visited_article view table with columns, author, title, num to find the name of the author later.

#### Views in the function `error_percent()`
* `create view datepart as select time,
  time::timestamp::date as date, status from log`
View explanation:
Create view datepart with two columns status and date, where date is the date part of timestamp to count according to days not according to timestamp.
* `create view error_tb as select date, count(*) as error_code
  from datepart where status like '4%' group by date order by error_code desc`
View explanation:
Create view error_tb with two columns date and error_code which is the count of the error status code on each day.
* `create view status_tb as select date, count(*) as status_code
  from datepart group by date order by status_code desc`
View explanation:
Create view status_tb with two columns date and status_code which is the count of all status codes on each day.
* `create view percentage_tb as select status_tb.date,
  error_code, status_code, (cast(error_code as decimal)/cast(status_code as decimal))*100
  as error_percent from error_tb, status_tb
  where error_tb.date=status_tb.date order by error_code desc`
View explanation:
Create view percentage_tb that is an inner join between the error_tb and status_tb with three columns, error_code status_code, and one of the error percenage.
