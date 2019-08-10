# TODO: Add player 'login' into a char
# TODO: Let a char enter a campaing
# TODO: Basic char actions
# TODO: Let player delete a char

import os
import random
from crael.client import DiscordClient


bot = DiscordClient()


@bot.register_command("!player")
def create_new_player(message):
    player = message.author
    player_id = bot.execute_query(f"SELECT id FROM players WHERE name={player.id};")

    if player_id:
        return f"Player {player.name} was already added."

    script = f"INSERT INTO players(nickname, discord_id) \
               VALUES(\"{player.name}\", \"{player.id}\");"
    _ = bot.execute_sql_script(script)
    return f"Added {player.display_name} as a player."


@bot.register_command("!play <char_name>")
def start_game_session(message, *, char_name):
    player = message.author
    player_id = bot.execute_query(f"SELECT id FROM players WHERE name={player.name};")

    char = bot.execute_query(f"SELECT * FROM characters WHERE \
                               player_id={player_id} AND name={char_name};")

    q = bot.execute_query("SELECT * FROM players;")
    return f"{q}"


@bot.register_command("!roll d<num>")
def roll(message, *, num):
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return f"{author} rolled {number}"


@bot.register_command("!startDB")
def startDB(message):
    try:
        bot.db_init()
        return f"A Data Base was created!"
    except Exception as e:
        print(e)
    return f"Failled."


if __name__ == "__main__":
    bot.run(os.getenv("CRAEL_SECRET_TOKEN"))
