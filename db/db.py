import psycopg2
from psycopg2 import Error
import os

class Db:
    def __init__(self):
        self.conn_str = os.getenv("CONN_STR")
        print(self.conn_str)
        self.conn = None
        self.curs = None
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(self.conn_str)
        except Error as e:
            print("Unable to connect to the database.")
            print(e)
        else:
            print("Connection to the database was successful.")
    
    def __enter__(self):
        print("entering context manager")
        self.connect()
        return self
    
    def __exit__(self, *args):
        print("exiting context manager")
        self.conn.close()

    def query_all(self, query, params):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(query, params)
                return curs.fetchall()
    
    def query_one(self, query, params):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(query, params)
                return curs.fetchone()
