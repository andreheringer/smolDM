import os
import sqlite3
from sqlite3 import Error
from configure import dev_env

class SQLDataBase:

    DATABASE_URI = os.path.join(os.path.dirname(__file__), dev_env.DatabaseFile)

    def __init__(self):
        self.conn = None

    def _create_connection(self):
        try:
            self.conn = sqlite3.connect(self.DATABASE_URI)
            return
        except Error as Err:
            print(Err)
            self.conn = None
        return

    def db_init(self):
        
        if self.conn is not None:
            print(f"[Err] A Connection to the DB {dev_env.DatabaseFile} already exists")
            return
        
        _create_connection()
        
        if self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            print(f"The DB has tables in it")
            return
        
        cursor = self.conn.cursor()
        try:
            cursor.executescript(ConfigDev.Schema)
            print("DB Created Sucessifuly")
        except Exception as err:
            print(f"Something went wrong during schme execution.")
        
        return

