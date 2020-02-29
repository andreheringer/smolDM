import os
import random
import logging as logger
from crael.client import DiscordClient

bot = DiscordClient()


@bot.register("!begin")
def start_game_session(message):
    bot.session.start_session(message.channel.id)
    logger.debug(f"Added {message.channel.id} into sessions\n {bot.session._sessions}")
    return f"Stated a new session with id {message.channel.id}"


@bot.register("!roll d<num>")
def roll(message, *, num):
    """
    """
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return f"{author} rolled {number}"


if __name__ == "__main__":
    bot.run(os.getenv("CRAEL_SECRET_TOKEN"))
