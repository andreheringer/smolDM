import random
from client import DiscordClient


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
        bot.db_init()
        return(f"A Data Base was created!")
    except Exception as e:
        print(e)
    return(f"Failled.")


if __name__ == '__main__':
    bot.run('NTM5MjMwNTI5MTgzMTU0MjE2.D4AA2g.kzn7149rpqEs2B8AsvYhrOinkTU')
