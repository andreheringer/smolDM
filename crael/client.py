"""
This module defines the Discord Bot interface.

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
        """Bot resgister method.

        Bounds command string to a function, see CommandHandler for more info.
        """
        return self.cmd.register(command_str)

    @staticmethod
    async def on_ready():
        """Re-implementation from parent class.

        Event triggered whenever the client is ready for
        interaction. Parent class requires it to be static.
        """
        print("Logged in ------")

    async def on_message(self, message) -> None:
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
