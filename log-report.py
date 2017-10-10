#!/usr/bin/env python3
import psycopg2
DBNAME = 'news'


def connect(database_name):
    '''Connect to the PostgreSQL database.  Returns a database connection.'''
    try:
        db = psycopg2.connect('dbname={}'.format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print('Unable to connect to database')
        sys.exit(1)


def get_query_results(query):
    '''Execute a given PostgrSQL query. Returns the query results.'''
    db, c = connect(DBNAME)
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == '__main__':
    results = get_query_results('''
                                select a.title, b.num
                                from articles a, article_views b
                                where a.slug = b.slug
                                order by num desc limit 3;
                                ''')
    print('\nTop 3 Articles - Ranked by View Count.')
    for article in results:
        print('"{}" - {:,d} views'.format(article[0], article[1]))

    results = get_query_results('''
                                select a.id, a.name, sum(c.num) as views
                                from authors a, articles b, article_views c
                                where a.id = b.author
                                and c.slug = b.slug
                                group by a.id, a.name
                                order by views desc limit 3;
                                ''')
    print('\nTop 3 Authors - Ranked by Total Article View Count.')
    for article in results:
        print('{} - {:,f} views'.format(article[1], article[2]))

    results = get_query_results('''
                                select a.day, success, error,
                                (error/success) * 100 as err_pct
                                from (select date(time) as day,
                                cast(count(status) as float) as success
                                from log where status = '200 OK'
                                group by day) as a,
                                (select date(time) as day,
                                cast(count(status) as float) as error from log
                                where status = '404 NOT FOUND'
                                group by day) as b
                                where a.day = b.day
                                and (error / success) > 0.01;
                                ''')
    print('\nDays Where 1% of Requests Ended in Error.')
    for article in results:
        print('{:%B %d, %Y} - {:,.2f}% errors'.format(article[0], article[3]))
