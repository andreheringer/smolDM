"""
    This module defines the Discord Bot interface.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import sys
import discord
import asyncio
from loguru import logger

from connection import SQLDataBase
from commands import CommandHandler


class DiscordClient(discord.Client):
    """
    This class inhird from the discord client wrapper,
    should abstract the connection with the discord api.
    """

    # TODO: Add a way to control 'state' in the bot
    # TODO: Add encryption of some sort

    def __init__(self):
        """
            DiscordClient __init__ method, this method
            calls for the discord.Client(parent class) __init__
            it also makes compositions with CommandHandler and
            SQLDatabase objects.
            Parameters:
                self
            Returns:
                DiscordClient object.
        """
        self.cmd = CommandHandler()  # Command Handler composition
        self.db = SQLDataBase()  # Data Base context Manager composition
        logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
        super().__init__()

    def db_init(self):
        """
            This method executes the sqlschema script and mounts the SQLite
            database.
        """
        with self.db as db:
            with open(db.SCHEMA_URI, mode="r") as sql:
                script = sql.read()
            cur = db.get_cursor()
            cur.executescript(script)
            logger.info(f"Database created gracefully")
        return

    def register_command(self, command_str: str):
        """
            Bounds command string to a function, see CommandHandler for more info.
        """
        return self.cmd.register(command_str)

    def execute_sql_script(self, script):
        with self.db as db:
            cur = db.get_cursor()
            cur.executescript(script)
            logger.debug(f"Query executed:\n{script}")

    # There should be a safer way to execute querys in SQLite
    # TODO: Look for safer options
    def execute_query(self, query: str):
        """
            Executes the query string into the DataBase
            USE WITH CAUTION THIS EXECUTES ANY VALID SQL SCRIPT
            Parameters:
                query: SQL script to be executed
            Returns:
                Nothing
        """
        with self.db as db:
            cur = db.get_cursor()
            cur.execute(query)
            rows = cur.fetchall()
            logger.debug(f"Query executed:\n{query}")
        return rows

    @staticmethod
    async def on_ready():
        """Re-implementation from parent class.

            Event triggered whenever the client is ready for
            interaction. Parent class requires it to be static.
        """
        logger.info("Logged\n------")

    @logger.catch()
    async def on_message(self, message):
        """Re-implementation from parent class.

            Event triggered whenever the client receives a new menssage.
        """
        patern_match = self.cmd.get_command_match(message)
        if not patern_match:
            return None
        kwargs, func = patern_match
        coro = asyncio.coroutine(func)
        response = await coro(message, **kwargs)
        channel = message.channel
        await channel.send(response)
