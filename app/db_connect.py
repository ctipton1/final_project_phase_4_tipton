import pymysql
import pymysql.cursors
from flask import g

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        g.db = pymysql.connect(
            # Database configuration
            # Configure MySQL
            host = 'p1us8ottbqwio8hv.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user = 'jxt86n3m3xv2h4nv',
            password = 'a7pl7ttmyvpf0bs9',
            database = 'atbrp8ng90t4o8d9',
            cursorclass=pymysql.cursors.DictCursor  # Set the default cursor class to DictCursor
        )
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()



