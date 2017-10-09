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
4. [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) the database data. The file inside is called ```newsdata.sql``` and should be moved to the ```vagrant``` directory.
5. Bring the VM online with ```vagrant up``` Then log into it with ```vagrant ssh```.
6. Create the database tables and populate them with data: ```psql -d news -f newsdata.sql```.
7. While still connected to the ```news``` database build this ```view```:
    ```
        CREATE VIEW article_views as
        select replace(path,'/article/','') as slug,
        count(1) as num from log
        where status = '200 OK'
        and path like '%/article/%'
        group by author, path;
    ```
8. Download ```log-report.py``` and move to the ```vagrant``` directory.
9. Execute report with this command: ```python3 log-report.py```.

## License
The contents of this repository are covered under the [MIT License](https://opensource.org/licenses/MIT).
