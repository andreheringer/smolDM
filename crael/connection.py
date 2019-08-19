"""
    This module defines all interactions with the internal database.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import os
import aiosqlite as aiolite


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
    async def conn(self):
        """Connection proprety getter.

            Returns: self.__conn
        """
        return self.__conn

    @conn.setter
    async def conn(self, signal: bool):
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
                self.__conn = await aiolite.connect(self.DATABASE_URI)
            except aiolite.Error as Err:
                print(Err)
                self.__conn = None
        return None

    async def __aenter__(self):
        """
            Defines the SQLDatabase entering context manager
            Returns itself.
        """
        self.conn = True
        return self

    async def __aexit__(self, exc_type, exc_log, exc_tb):
        """
            Defines the SQLDatabase exiting context manager
        """
        self.conn = False
        return False  # this propagates any exceptions inside the with block

    def get_schema_script(self):
        with open(self.SCHEMA_URI, mode="r") as sql:
            script = sql.read()
        return script

    async def execute_script(self, script: str):
        await self.__conn.execute(script)
        # logger.debug("Executed sql script:\n\n{script}\n\n")
        changes = await self.__conn.total_changes()
        # logger.debug(f"{changes} lines changed")
        return None

    async def execute_query(self, query: str):
        cursor = await self.__conn.execute(query)
        rows = await cursor.fetchall()
        return rows
