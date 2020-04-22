"""
This module defines the Discord Clint interface.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""

import asyncio
import discord
from pathlib import Path
from typing import Optional
from loguru import logger

import smolDM.commands as cmd
import smolDM.compass as compass
import smolDM.scenes as scene
import smolDM.session as session


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
        self._sessions = {}
        self.hash_session_key = lambda player, channel_id: f"{player}@{channel_id}"
        self.adventures = Path(__file__).parent.absolute() / "adventures/"

        logger.add(
            Path(__file__).parent.parent.absolute() / "logs/file_1.log",
            level="INFO",
            rotation="600 MB",
            serialize=True,
        )

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

    def special_macth(self, special_key, message):
        """Return a special command match."""
        return self._special_commands["pick"].match(message.content)

    def load_adventure(self, adv_file, player, channel):
        """Load a new adventure into the bot Compass.

        Args:
            adv_file: Adventure file path.
        """
        _scenes = scene.load_scenes(adv_file)

        session_key = self.hash_session_key(player, channel.id)

        self._sessions[session_key] = session.start_session(player, channel, _scenes)
        return self._sessions[session_key]

    def sessions(self):
        """Return bot's sessions."""
        return self._sessions.keys()

    def end_adventure(self, ses_key):
        del self._sessions[ses_key]

    def here(self, session_key):
        """Return bot's current state in adventure."""
        return self._sessions[session_key].here

    def pick(self, message: discord.Message, session) -> Optional[scene.Scene]:
        """Pick special command for adventure navegation.

        Args:
            message: Discord Message

        Returns:
            Optinoal current scene
        """
        if self._special_commands["pick"].match(message.content) is None:
            return None

        option = self._special_commands["pick"].match(message.content).group(1)

        return compass.goto(session.here, session.scenes, option)

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
        logger.info("Logged in ----")

    async def on_message(self, message: discord.Message) -> None:
        """Event triggered whenever the client receives a new message.

        Re-implementation from parent class.

        Args:
            message: Discord.py message object

        """
        logger.info("Listening to messages...")
        patern_match = cmd.get_command_match(self._commands, message)
        logger.info("Searching command match for new message")
        if not patern_match:
            return None
        kwargs, func = patern_match
        response = await func(self, message, **kwargs)
        channel = message.channel
        await channel.send(response)
