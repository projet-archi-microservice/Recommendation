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


def get_n_movies(n):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"SELECT json_agg(json_build_object('id', id, 'title', title, 'release_date', release_date, 'genre_ids', genre_ids, 'vote_average', vote_average)) FROM (SELECT id, title, release_date, vote_average, genre_ids FROM movies ORDER BY vote_average DESC LIMIT {n}) as subquery;")
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
