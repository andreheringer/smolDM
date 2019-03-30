"""
    This module defines the Discord Bot interface.

    :copywrite: Andre Heringer 2018-2019
    :license: MIT, see license for details
"""

import discord
import asyncio
from connection import SQLDataBase
from commands import CommandHandler


class DiscordClient(discord.Client):
    """
    This class inhird from the discord client wrapper,
    should abstract the connection with the discord api.
    """

    def __init__(self):
        """
            DiscordClient __init__ method, this method
            calls for the discord.Client(parent class) __init__
            it also makes compositions with CommandHandler and
            SQLDatabase objects.
            Parameters:
                command_handler: A command handler object
            Returns:
                DiscordClient object.
        """
        self.cmd = CommandHandler()
        self.db = SQLDataBase()
        super().__init__()

    def db_init(self):
        with self.db as db:
            with open(db.SCHEMA_URI, mode='r') as sql:
                script = sql.read()
            cur = db.get_cursor()
            cur.executescript(script)
            print(f"Database created gracefully")
        return

    def register_command(self, command_str: str):
        return self.cmd.register(command_str)

    @staticmethod
    async def on_ready():
        """Re-implementation from parent class.
            
            Event triggered whenever the client is ready for
            interaction. Parent class requires it to be static.
        """
        print("Logged")
        print("------")

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
        await self.send_message(message.channel, response)
