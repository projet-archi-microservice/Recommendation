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


def get_user_token(name, password):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"SELECT * FROM users  WHERE name = \'{name}\';")
    # cur.excute(f"genre_ids")
   
    # display the query result
    result = cur.fetchone()

    print(result)

    if(result == None):
        return "Invalid Account"
    else :
        if result[3] != password:
            return "Invalid Password"

    payload = {
        'username': result[1],
        'email': result[2]
    }
    
    secret_key = 'my-secret-key'
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    print(token)

    cur.close()
    conn.close()
    return token