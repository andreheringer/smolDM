"""
This module defines the Discord Clint interface.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""

import discord
import asyncio

from crael.commands import CommandHandler
from crael.session import SessionHandler


class DiscordClient(discord.Client):
    """Discord Client class.

    This class inhird from the discord client wrapper,
    should abstract the connection with the discord api.
    """

    # TODO: Add a way to control 'state' in the bot
    # TODO: Add encryption of some sort

    def __init__(self):
        """Discord Client __init__ method.

        Calls for the discord.Client(parent class) __init__
        it also makes compositions with CommandHandler and
        SessionHandler objects.
        """
        # self.logger = logging.getLogger(__name__)

        self.cmd = CommandHandler()  # Command Handler composition
        self.session = SessionHandler()

        super().__init__()

    def register(self, command_str: str) -> callable:
        """Bot resgister decorator, bounds command string to a function.

        Args:
            command_str: Command match string

        Returns:
            A callable wich is the decorated function.

        """
        return self.cmd.register(command_str)

    def add_command(self, func, command_str):
        """Add a command to the bot CommandHandler.

        Args:
            func: function called on command
            command_str: command patter string

        """
        self.cmd.add_command(func, command_str)

    @staticmethod
    async def on_ready():
        """Re-implementation from parent class.

        Event triggered whenever the client is ready for
        interaction. Parent class requires it to be static.
        """
        print("Logged in ------")

    async def on_message(self, message) -> None:
        """Event triggered whenever the client receives a new message.

        Re-implementation from parent class.

        Args:
            message: Discord.py message object

        Returns:
            None

        """
        patern_match = self.cmd.get_command_match(message)
        if not patern_match:
            return None
        kwargs, func = patern_match
        coro = asyncio.coroutine(func)
        response = await coro(self, message, **kwargs)
        channel = message.channel
        await channel.send(response)
