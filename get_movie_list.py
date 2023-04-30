import psycopg2
import json

from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def get_search_result(search):
    # read connection parameters
    params = config()
    n = 30
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"SELECT json_agg(json_build_object('id', id, 'title', title, 'release_date', release_date, 'poster_path', poster_path, 'genre_ids', genre_ids)) FROM (SELECT id, title, release_date, poster_path, genre_ids FROM movies WHERE lower(title) LIKE lower('%{search}%') LIMIT {n}) as subquery;")
    # cur.excute(f"genre_ids")
   
    unique = ""
    result = cur.fetchone()

    # display the query result
    if (result != (None,)):
        unique = json.dumps({ x['id'] : x for x in result[0] })
        print(unique)
    else:
        unique = "Nothing found"
    
    cur.close()
    conn.close()
    return unique
