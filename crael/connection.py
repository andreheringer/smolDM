"""
    This module defines all interactions with the internal database.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import os
import logging as logger
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

    def get_schema_script(self):
        with open(self.SCHEMA_URI, mode="r") as sql:
            script = sql.read()
        return script

    async def execute_script(self, script: str):
        async with aiolite.connect(self.DATABASE_URI) as db:
            logger.info("Executing sql script:\n\n{script}\n\n")
            await db.execute(script)
            changes = db.total_changes()
            logger.info(f"{changes} lines changed")
        return changes

    async def execute_query(self, query: str):
        
        async with aiolite.connect(self.DATABASE_URI) as db:
            logger.info(f"Executing query {query}")
            async with db.execute(query) as cursor:
                rows = await cursor.fetchall()
        
        return rows
