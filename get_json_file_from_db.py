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


def get_n_movies(n):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"SELECT json_agg(json_build_object('id', id, 'title', title, 'release_date', release_date, 'poster_path', poster_path, 'genre_ids', genre_ids, 'vote_average', vote_average)) FROM (SELECT id, title, release_date, vote_average, poster_path, genre_ids, adult FROM movies WHERE adult = false ORDER BY vote_average DESC LIMIT {n}) as subquery;")
    # cur.excute(f"genre_ids")
   
    # display the query result
    result = cur.fetchone()[0]
    print(result)

    # write result to a json file
    with open('movies.json', 'w') as f:
        json.dump(result, f, indent=4)
    
    cur.close()
    conn.close()
    
get_n_movies(50)
