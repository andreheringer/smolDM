import random
from client import DiscordClient
from commands import CommandHandler
from configure import dev_env
from connection import SQLDataBase

cmd = CommandHandler()
db = SQLDataBase()
bot = DiscordClient(cmd, db)


@cmd.register("!roll<num>")
def roll(message, *, num):
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return(f"{author} rolled {number}")

# @cmd.register("!initicative")
# def roll_iniciative(message):


if __name__ == '__main__':
    bot.run(dev_env.DiscordBotToken)