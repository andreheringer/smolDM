# TODO: Create Graph Struct
# TODO: Build bot interactions based on graph struct

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
    bot = DiscordClient()
    bot.register(roll, "roll d<num>")
    bot.run(os.getenv("CRAEL_SECRET_TOKEN"))
