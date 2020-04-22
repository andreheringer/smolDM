"""
Main module for the bot, game especific machenics go here.

:copywrite: Andre Heringer 2018-2020
:license: MIT, see license for details
"""
import os
import random
import discord
from loguru import logger
from smolDM.client import DiscordClient


async def game_loop(bot: DiscordClient, session: str):
    """Control game loop.

    Args:
        bot: bot instance
        session: gameplay session key
    """

    def check(message):
        return (
            bot.special_macth("pick", message) is not None
            and message.channel == session.channel
            and message.author == session.player
        )

    while session.here is not None:
        await bot.display_scene(session.here, session.channel)
        msg = await bot.wait_for("message", check=check)
        session.here = bot.pick(msg, session)
    return


async def start_default(bot: DiscordClient, message: discord.Message) -> str:
    """Start the default/example adventure.

    Args:
        bot: bot instance
        message: message evaluated
    """

    ses_key = bot.hash_session_key(message.author, message.channel.id)
    if ses_key in bot.sessions():
        return f"An adventure is already in place."

    path = bot.adventures / "default.md"
    new_session = bot.load_adventure(path, message.author, message.channel)
    _ = await game_loop(bot, new_session)
    bot.end_adventure(ses_key)
    return f"The adventure has ended, see you soon."


async def start_adventure(bot, message, *, adventure) -> str:
    """Start adventure.

    Args:
        bot: bot instance
        message: message evaluated
        adventure: adventure file name
    """
    ses_key = bot.hash_session_key(message.author, message.channel.id)
    if ses_key in bot.sessions():
        return f"An adventure is already in place."
    path = bot.adventures / adventure
    new_session = bot.load_adventure(path, message.author, message.channel)
    _ = await game_loop(bot, new_session)
    bot.end_adventure(ses_key)
    return f"The adventure has ended, see you soon."


async def read(bot, message: discord.Message, *, adv):
    """Read an adventure file attached to a message."""
    f = message.attachments[0]
    bts = await f.save(bot.adventures / adv)
    logger.info(f"Saved {bts} bytes, at {adv} file.")
    return f"Adventure {adv} was archived and can now be played."


async def roll(bot: DiscordClient, message: discord.Message, *, num: str) -> str:
    """Dice roll command.

    Args:
        bot: the current bot instance
        message: message evaluated
        num: command paramenter especifing dice size

    Retruns:
        A string saying what the player rolled.
    """
    x = int(num)
    number = random.randint(1, x)
    logger.info(f"Player {message.author} rolled {number}")
    return f"{message.author} rolled {number}"


def main():
    """Bot instanciation."""

    bot = DiscordClient()
    bot.add_command(read, "!read <adv>")
    bot.add_command(roll, "!roll d<num>")
    bot.add_command(start_default, "!default")
    bot.run(os.getenv("SMOLDM_SECRET_TOKEN"))
