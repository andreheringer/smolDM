"""
Main module for the bot, game especific machenics go here.

:copywrite: Andre Heringer 2018-2020
:license: MIT, see license for details
"""
import asyncio
import os
import random
import discord
from pathlib import Path
from smolDM.client import DiscordClient
from smolDM.scenes import Scene


async def pick(bot, message, *, num):
    if num == "0":
        return None
    bot.goto(num)
    return bot.here()


async def game_loop(
    bot: DiscordClient, channel: discord.channel.TextChannel, scene: Scene
) -> None:

    if scene is None:
        return

    def check(message):
        return (
            bot.match_special_handler("pick", message) is not None
            and message.channel == channel
        )

    async with channel.typing():
        for line in scene.lines:
            if line == "\n":
                await asyncio.sleep(5)
            else:
                await channel.send(line)

        for option in scene.options:
            await channel.send(f"{option.description}")

    msg = await bot.wait_for("message", check=check)
    kwargs, func = bot.match_special_handler("pick", msg)
    new_scene = await func(bot, msg, **kwargs)
    await channel.send(f"vc escolheu {new_scene.scene_id}")
    # game_loop(bot, msg.channel, new_scene)


async def start_default(bot: DiscordClient, message: discord.Message):
    path = Path(__file__).parent.absolute() / "adventures/default.md"
    bot.load_adventure(path)
    await game_loop(bot, message.channel, bot.here())
    return f"The adventure has ended, see you soon."


async def roll(bot, message, *, num):
    """
    """
    x = int(num)
    number = random.randint(1, x)
    author = message.author
    return f"{author} rolled {number}"


def main():
    """Define main entry point for the bot."""

    bot = DiscordClient()
    bot.add_command(roll, "!roll d<num>")
    bot.add_command(pick, "!pick <num>", "pick")
    bot.add_command(start_default, "!default")
    bot.run(os.getenv("SMOLDM_SECRET_TOKEN"))


if __name__ == "__main__":
    main()
