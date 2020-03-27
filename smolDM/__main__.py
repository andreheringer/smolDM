"""
Main module for the bot, game especific machenics go here.

:copywrite: Andre Heringer 2018-2020
:license: MIT, see license for details
"""
import os
import random
import discord
from pathlib import Path
from smolDM.client import DiscordClient
from smolDM.scenes import Scene


async def game_loop(
    bot: DiscordClient, channel: discord.channel.TextChannel, scene: Scene
):
    """Control game loop.

    Args:
        bot: the bot instance the game is running
        channel: the channel used to interact with the bot for this game run
        scene: current game scene
    """

    def check(message):
        return (
            bot.special_macth("pick", message) is not None
            and message.channel == channel
        )

    while scene is not None:
        await bot.display_scene(scene, channel)
        msg = await bot.wait_for("message", check=check)
        scene = bot.pick(msg)
    return


async def start_default(bot: DiscordClient, message: discord.Message):
    """Start the default/example adventure.

    Args:
        bot: the current bot instance
        message: current message been evaluated
    """
    path = Path(__file__).parent.absolute() / "adventures/default.md"
    bot.load_adventure(path)
    _ = await game_loop(bot, message.channel, bot.here())
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
    author = message.author
    return f"{author} rolled {number}"


def main():
    """Define main entry point for the bot."""

    bot = DiscordClient()
    bot.add_command(roll, "!roll d<num>")
    bot.add_command(start_default, "!default")
    bot.run(os.getenv("SMOLDM_SECRET_TOKEN"))


if __name__ == "__main__":
    main()
