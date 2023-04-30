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


def get_genre(id):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"SELECT json_agg(json_build_object('id', id, 'name', name)) FROM (SELECT id, name FROM genres WHERE id = {id}) as subquery;")
    # cur.excute(f"genre_ids")
   
    # display the query result
    result = json.dumps(cur.fetchone()[0][0]['name'])
    print(result)
    
    cur.close()
    conn.close()
    return result