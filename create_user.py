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


def create_user(name, email, password):
    # read connection parameters
    params = config()
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
        
    # execute a statement
    cur.execute(f"INSERT INTO users(name, email, password) VALUES (\'{name}\', \'{email}\', \'{password}\')")
    
    cur.close()
    conn.commit()
    conn.close()
