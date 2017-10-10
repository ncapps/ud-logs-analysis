# Logs Analysis Project
The objective of this project was to develop a reporting tool using Python and
PostgreSQL to analyze a mock news website relational database and discover
which articles and authors are the most popular based on page views.
This project is part of Udacity's Full Stack Web Developer Nanodegree Program.

## Prepare the environment and data
You will use a virtual machine (VM) to run a SQL database server and the
reporting tool web app.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to run the VM.
2. Install [Vagrant](https://www.vagrantup.com/downloads.html) to configure
    the VM and to share files between the host computer the VM's filesystem.
3. Fork and clone the [VM configuration](https://github.com/udacity/fullstack-nanodegree-vm).
4. [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) the database data. The file inside is called ```newsdata.sql``` and should be moved to the ```fullstack-nanodegree-vm/vagrant/``` directory.
5. Set the working directory to ```vagrant```.
6. Bring the VM online with ```vagrant up``` Then log into it with ```vagrant ssh```.
7. Create the database tables and populate them with data: ```psql -d news -f newsdata.sql```.
8. While still connected to the ```news``` database build the ```article_views``` view.
    ```
        CREATE VIEW article_views as
        select replace(path,'/article/','') as slug,
        count(1) as num from log
        where status = '200 OK'
        and path like '%/article/%'
        group by author, path;
    ```
9. Download ```log-report.py``` and move to the ```vagrant``` directory.
10. Execute the report using command: ```python3 log-report.py```.

## Report summary
The report aims to answer the following questions:
1. Which articles have the most views?
2. Which article authors have the most total views?
3. On which days did more than 1% of http requests end in error?

Report results are included in the ```sample-output.txt``` file.

## How it works
The ```article_views``` view returns the article slug and number of views. This
was created to simplify the SQL queries used to answer the first two questions.

1. Article title and number of views were found by joining the ```article_views```
view and ```articles``` table on the ```slug``` field.
2. The most popular authors were found by joining the ```article_views``` view
and ```articles``` table on the ```slug``` field. The ```articles``` table was
also joined with the ```authors``` table using the ```author``` and ```id``` fields.
The ```sum()``` function was used with ```group by``` clause on the author ```id``` and  ```name``` fields to aggregate total views by author.
3. The number of requests that ended in success or error for a given day were
aggregated in separate queries and then joined together on the ```day``` alias.
Error percentage was then calculated for each day.

## License
The contents of this repository are covered under the [MIT License](https://opensource.org/licenses/MIT).
