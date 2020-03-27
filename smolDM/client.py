"""
This module defines the Discord Clint interface.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""

import asyncio
import discord
from typing import Optional

import smolDM.commands as cmd
from smolDM.compass import Compass
from smolDM.scenes import Scene


class DiscordClient(discord.Client):
    """Discord Client class.

    This class inhird from the discord client wrapper,
    should abstract the connection with the discord api.
    """

    def __init__(self):
        """Discord Client __init__ method.

        TODO: Doc string this.
        """

        self._commands = []
        self._special_commands = {"pick": cmd.build_command_pattern("!pick <num>")}
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

    def add_command(self, func: callable, command_str: str):
        """Add a command to the bot CommandHandler.

        Args:
            func: function called on command
            command_str: command patter string

        """
        cmd.add_command(self._commands, func, command_str)
        return self

    def load_adventure(self, adv_file):
        """Load a new adventure into the bot Compass.

        Args:
            adv_file: Adventure file path.
        """
        self.compass = Compass(adv_file)
        return self

    def here(self):
        """Return bot's current state in adventure."""
        return self.compass.cur_scene()

    def pick(self, message: discord.Message) -> Optional[Scene]:
        """Pick special command for adventure navegation.

        Args:
            message: Discord Message

        Returns:
            Optinoal current scene
        """
        if self._special_commands["pick"].match(message.content) is None:
            return None

        num = self._special_commands["pick"].match(message.content).group(1)

        self.compass.goto(num)
        return self.here()

    def special_macth(self, special_key, message):
        """Return a special command match."""
        return self._special_commands["pick"].match(message.content)

    async def display_scene(self, scene, channel):
        """Display scene.

        Args:
            scene: to be displayed
            channel: channel wich scene will be displayed
        """
        async with channel.typing():
            for line in scene.lines:
                if line == "\n":
                    await asyncio.sleep(3)
                else:
                    await channel.send(line)

            for option in scene.options:
                await channel.send(f"{option.description}")
        return

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
