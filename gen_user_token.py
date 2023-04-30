import psycopg2
import json
import jwt

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