import mysql.connector
from flask import g
from backend.constants import db_config

def connect_to_database():
    # connect to the database
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    # get the database
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db
    