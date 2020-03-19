"""
Main module for the bot, game especific machenics go here.

:copywrite: Andre Heringer 2018-2020
:license: MIT, see license for details
"""
import os
import random
from crael.client import DiscordClient


def roll(bot, message, *, num):
    """
    """
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return f"{author} rolled {number}"


def main():
    """Define main entry point for the bot."""

    bot = DiscordClient()
    bot.add_command(roll, "roll d<num>")
    bot.run(os.getenv("CRAEL_SECRET_TOKEN"))


if __name__ == "__main__":
    main()
