import string

from Utilisateur import User
import psycopg2
import json
from configparser import ConfigParser


def read_db(req: string):
    conn = psycopg2.connect(
        host="bpv7mlbngflnnamyjr6x-postgresql.services.clever-cloud.com",
        port="6172",
        database="bpv7mlbngflnnamyjr6x",
        user="uljpz0f1fxjpdk0ps0be",
        password="xLpCEPFKqrG8uV12sQbK")
    # create a cursor
    cur = conn.cursor()

    cur.execute(req)
    conn.commit()

    # display the PostgreSQL database server version
    db_result = cur.fetchall()
    print(db_result)

    cur.close()
    conn.close()
    return db_result


def update_bdd(req: string):
    conn = psycopg2.connect(
        host="bpv7mlbngflnnamyjr6x-postgresql.services.clever-cloud.com",
        port="6172",
        database="bpv7mlbngflnnamyjr6x",
        user="uljpz0f1fxjpdk0ps0be",
        password="xLpCEPFKqrG8uV12sQbK")
    # create a cursor
    cur = conn.cursor()

    cur.execute(req)
    conn.commit()

    cur.close()
    conn.close()


def post_user_bdd(user: User):
    tmp: string = str(user.id)
    req = "UPDATE users SET email='"+user.email+"', password='"+user.password+"' WHERE id = "+tmp+";"

    print(update_bdd(req))
    return "ok"


def get_user_bdd(name: string):
    req = "SELECT * FROM users WHERE name='"+name+"'"
    return read_db(req)


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


# monUser = User()
# monUser.id = 7
# monUser.nom = "monSuperNomTropChouette"
# monUser.email = "monEmailBcpTropUtile"
# monUser.password = "monPasswordTropSecur"
# post_user_bdd(monUser)
