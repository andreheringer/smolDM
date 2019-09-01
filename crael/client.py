"""
    This module defines the Discord Bot interface.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""


import discord
import asyncio
import logging as logger

from crael.connection import SQLDataBase
from crael.commands import CommandHandler
from crael.session import SessionHandler


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
        self.session = SessionHandler()
        logger.basicConfig(level= logger.INFO, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        super().__init__()

    def register(self, command_str: str):
        """
            Bounds command string to a function, see CommandHandler for more info.
        """
        return self.cmd.register(command_str)

    def start_session(self, session_id: str):
        """
            Starts a new bot session, see SessionHandler for more info 
        """
        self.session.start_session(session_id)

    def db_init(self):
        """
            This method executes the sqlschema script and mounts the SQLite
            database.
        """
        squema = self.db.get_schema_script()
        self.db.execute_script(squema)
        logger.debug(f"Database created gracefully")
        return

    # There should be a safer way to execute scripts in SQLite
    # TODO: Look for safer options
    async def execute_sql_script(self, script):
        """
            Executes the query string into the DataBase
            USE WITH CAUTION THIS EXECUTES ANY VALID SQL SCRIPT
            Parameters:
                query: SQL script to be executed
            Returns:
                Nothing
        """
        self.db.execute_script(self, script)

    # There should be a safer way to execute querys in SQLite
    # TODO: Look for safer options
    async def execute_query(self, query: str):
        rows = await self.db.execute_query(query)
        return rows

    @staticmethod
    async def on_ready():
        """Re-implementation from parent class.

            Event triggered whenever the client is ready for
            interaction. Parent class requires it to be static.
        """
        logger.info("Logged in ------")


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
