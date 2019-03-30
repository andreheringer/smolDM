import random
from client import DiscordClient
from configure import dev_env


bot = DiscordClient()


@bot.register_command("!roll d<num>")
def roll(message, *, num):
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return(f"{author} rolled {number}")


@bot.register_command("!startDB")
def startDB(message):
    try:
        bot.db.db_init()
        return(f"A Data Base was created!")
    except Exception as e:
        print(e)
    return(f"Failled.")


if __name__ == '__main__':
    bot.run(dev_env.DiscordBotToken)
