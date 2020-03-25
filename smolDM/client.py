"""
This module defines the Discord Clint interface.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""

import discord
from typing import Optional

import smolDM.commands as cmd
from smolDM.compass import Compass


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

        self._commands = []
        self._special_handlers = {}
        self.compass = None

        super().__init__()

    def register(self, command_str: str) -> callable:
        """Bot resgister decorator, bounds command string to a function.

        Args:
            command_str: Command match string

        Returns:
            A callable wich is the decorated function.

        """
        return cmd.register(self._commands, command_str)

    def add_command(
        self, func: callable, command_str: str, special_handler: Optional[str] = None
    ):
        """Add a command to the bot CommandHandler.

        Args:
            func: function called on command
            command_str: command patter string

        """
        if special_handler:
            self._special_handlers = cmd.add_special_handler(
                self._special_handlers, func, command_str, special_handler
            )
        else:
            cmd.add_command(self._commands, func, command_str)
        return self

    def match_special_handler(self, special_key, message):
        command = [self._special_handlers[special_key]]
        return cmd.get_command_match(command, message)

    def load_adventure(self, adv_file):
        self.compass = Compass(adv_file)
        return self

    def here(self):
        return self.compass.cur_scene()
    
    def goto(self, option_id):
        return self.compass.goto(option_id)

    @staticmethod
    async def on_ready() -> None:
        """Re-implementation from parent class.

        Event triggered whenever the client is ready for
        interaction. Parent class requires it to be static.
        """
        print("Logged in ------")

    async def on_message(self, message: discord.Message) -> None:
        """Event triggered whenever the client receives a new message.

        Re-implementation from parent class.

        Args:
            message: Discord.py message object

        """
        patern_match = cmd.get_command_match(self._commands, message)
        if not patern_match:
            return None
        kwargs, func = patern_match
        response = await func(self, message, **kwargs)
        channel = message.channel
        await channel.send(response)
