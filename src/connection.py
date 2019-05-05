"""
    This module defines all interactions with the internal database.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import os
import sqlite3 as lite
from sqlite3 import Error


class SQLDataBase:
    """This class acts as a interface for the SQLite Crael database.
        It's also defined as a context manager so it can be used alog side
        a "with" statement.
    """

    DATABASE_URI = os.path.join(os.path.dirname(__file__), "db/creal.db")
    SCHEMA_URI = os.getenv(
        "SHCEMA_", default=os.path.join(os.path.dirname(__file__), "db/schema.sql")
    )

    def __init__(self, conn=None):
        """Init method instancite a None connection

            Properties:
                _conn: The sqlite connection object
        """
        self.__conn = conn

    @property
    def conn(self):
        """Connection proprety getter.

            Returns: self.__conn
        """
        return self.__conn

    @conn.setter
    def conn(self, signal: bool):
        """Connection proprety setter

            Parameters:
                signal: boolean that changes the connection state,
                        true -> open connection
                        false -> close connection
            Returns:
                nothing
        """
        if signal is False:
            self.__conn.close()

        if signal is True:
            try:
                self.__conn = lite.connect(self.DATABASE_URI)
            except Error as Err:
                print(Err)
                self.__conn = None
        return

    def __enter__(self):
        """Defines the SQLDatabase entering context manager
        """
        self.conn = True
        return self

    def __exit__(self, exc_type, exc_log, exc_tb):
        """Defines the SQLDatabase exiting context manager
        """
        self.conn = False
        return False  # this propagates any exceptions inside the with block

    def get_cursor(self):
        """Returns a sqlite cursor."""
        return self.conn.cursor()
