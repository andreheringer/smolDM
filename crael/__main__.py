# TODO: Add player 'login' into a char
# TODO: Let a char enter a campaing
# TODO: Basic char actions
# TODO: Let player delete a char

import os
import random
import logging as logger
from crael.client import DiscordClient

bot = DiscordClient()


@bot.register("!player")
def create_new_player(message):
    """
    """
    player = message.author
    player_id = bot.execute_query(f"SELECT * FROM players WHERE discord_id=\"{player.id}\";")

    if player_id:
        return f"Player {player.name} was already added."

    script = f"INSERT INTO players(nickname, discord_id) \
               VALUES(\"{player.name}\", \"{player.id}\");"

    _ = bot.execute_sql_script(script)

    return f"Added {player.display_name} as a player."


@bot.register("!begin")
def start_game_session(message):
    bot.session.start_session(message.channel.id)
    logger.debug(f"Added {message.channel.id} into sessions\n {bot.session._sessions}")
    return f"Stated a new session with id {message.channel.id}"


@bot.register("!play <char_name>")
def join_game_session(message, *, char_name):
    # player = message.author
    # player_id = bot.execute_query(f"SELECT id FROM players WHERE name={player.name};")

    # char = bot.execute_query(f"SELECT * FROM characters WHERE \
    #                           player_id={player_id} AND name={char_name};")

    q = bot.execute_query("SELECT * FROM players;")
    return f"{q}"


@bot.register("!roll d<num>")
def roll(message, *, num):
    """
    """
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return f"{author} rolled {number}"


@bot.register("!startDB")
def startDB(message):
    """
    """
    try:
        bot.db_init()
        return f"A Data Base was created!"
    except Exception as e:
        print(e)
    return f"Failled."


if __name__ == "__main__":
    bot.run(os.getenv("CRAEL_SECRET_TOKEN"))
