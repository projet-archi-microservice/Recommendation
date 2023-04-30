import psycopg2
import json
import jwt
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


def check_token(token):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
    
    secret_key = 'my-secret-key'

    test = True
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except:
        cur.close()
        conn.close()
        return(False)
    
    cur.execute(f"SELECT * FROM users WHERE name = \'{payload['username']}\';")

    result = cur.fetchone()
    if( result == None) and test:
        test = False
    else:
        print(result)
        test = True

    cur.close()
    conn.close()

    return(test)
