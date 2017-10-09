#!/usr/bin/env python3
import psycopg2
DBNAME = 'news'


def article_views():
    '''Return the 3 articles with the most views.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select a.title, b.num from articles a, article_views b
                where a.slug = b.slug
                order by num desc limit 3;''')
    results = c.fetchall()
    print('\nTop 3 Articles - Ranked by View Count.')
    for article in results:
        print('"{}" - {:,d} views'.format(article[0], article[1]))
    db.close()
    return


def author_views():
    '''Return the 3 authors with the most total article views.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select a.id, a.name, sum(c.num) as views
                    from authors a, articles b, article_views c
                    where a.id = b.author
                    and c.slug = b.slug
                    group by a.id, a.name
                    order by views desc limit 3;''')
    results = c.fetchall()
    print('\nTop 3 Authors - Ranked by Total Article View Count.')
    for article in results:
        print('{} - {:,f} views'.format(article[1], article[2]))
    db.close()
    return


def error_days():
    '''Return days where more than 1% of requests were errors.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select a.day, success, error, (error/success) * 100 as err_pct
                    from (select date(time) as day,
                    cast(count(status) as float) as success from log
                    where status = '200 OK' group by day) as a,
                    (select date(time) as day,
                    cast(count(status) as float) as error from log
                    where status = '404 NOT FOUND' group by day) as b
                    where a.day = b.day and (error / success) > 0.01;''')
    results = c.fetchall()
    print('\nDays Where 1% of Requests Ended in Error.')
    for article in results:
        print('{:%B %d, %Y} - {:,.2f}% errors'.format(article[0], article[3]))
    db.close()
    return


article_views()
author_views()
error_days()
