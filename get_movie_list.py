import psycopg2
import json
import os

from configparser import ConfigParser


def config():
    db = {
      'host': os.environ.get('DB_HOST'),
      'database': os.environ.get('DB_DB'),
      'password': os.environ.get('DB_PASSWORD'),
      'user': os.environ.get('DB_USER'),
      'port': os.environ.get('DB_PORT')
    }

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
