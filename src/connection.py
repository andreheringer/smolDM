"""
    This module defines all interactions with the internal database.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import os
import sqlite3 as lite
from sqlite3 import Error
from configure import dev_env


class SQLDataBase:
    """This class acts as a interface for the SQLite Crael database"""

    DATABASE_URI = os.path.join(os.path.dirname(__file__), dev_env.DatabaseFile)
    SCHEMA_URI = os.path.join(os.path.dirname(__file__), dev_env.Schema)

    def __init__(self):
        """Init method instancite a None connection

            Properties:
                _conn: The sqlite connection object
        """
        self._conn = None

    @property
    def get_connection(self):
        """Connection proprety getter.

            Returns: self._conn
        """
        return self._conn

    @property.setter
    def set_connection(self, signal: bool):
        """Connection proprety setter

            Parameters:
                signal: boolean that changes the connection state,
                        true -> open connection
                        false -> close connection
            Returns:
                nothing
        """
        if self._conn is not None and signal is False:
            self._conn.close()
            self._conn = None
            return

        if self._conn is None and signal is True:
            try:
                self._conn = lite.connect(self.DATABASE_URI)
                return
            except Error as Err:
                print(Err)
                self._conn = None
        return


    def db_init(self):

        if not self.get_connection():
            print(f"[Err] A Connection to the DB {dev_env.DatabaseFile} already exists")
            return

        self.set_connection(True)
        cur = self._conn.cursor()

        with open(self.SCHEMA_URI, mode='r') as schema:
            script = schema.read()
            cur.executescript(script)

        self._conn.commit()
        print("DB Created Sucessifuly")
        return
