"""
Main module for the bot, game especific machenics go here.

:copywrite: Andre Heringer 2018-2020
:license: MIT, see license for details
"""
import os
import random
import discord
from pathlib import Path
from loguru import logger
from smolDM.client import DiscordClient


async def game_loop(bot: DiscordClient, session):
    """Control game loop.

    Args:
        bot: the bot instance the game is running
        channel: the channel used to interact with the bot for this game run
        scene: current game scene
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


async def start_default(bot: DiscordClient, message: discord.Message):
    """Start the default/example adventure.

    Args:
        bot: the current bot instance
        message: current message been evaluated
    """
    ses_key = bot.hash_session_key(message.author, message.channel.id)
    if ses_key in bot.sessions():
        return f"An adventure is already in place."

    path = Path(__file__).parent.absolute() / "adventures/default.md"
    new_session = bot.load_adventure(path, message.author, message.channel)
    _ = await game_loop(bot, new_session)
    bot.end_adventure(ses_key)
    return f"The adventure has ended, see you soon."


async def roll(bot, message, *, num: str) -> str:
    """Dice roll command.

    Args:
        bot: the current bot instance
        message: current message been evaluated
        num: command paramenter for the dice size

    Retruns:
        A string saying the player roll.
    """
    x = int(num)
    number = random.randint(1, x)
    logger.info(f"Player {message.author} rolled {number}")
    return f"{message.author} rolled {number}"


def main():
    """Define main entry point for the bot."""

    bot = DiscordClient()
    bot.add_command(roll, "!roll d<num>")
    bot.add_command(start_default, "!default")
    bot.run(os.getenv("SMOLDM_SECRET_TOKEN"))
