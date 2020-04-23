# SmolDM

Very smol Dungeon Master for one shot RPG sessions.

This project was built with intending to be a Python exercise. I love Python and want to keep working with it even tho my current work place is a Java shop.

## Commands

The bot comes equiped with some basic commands:

- ```!roll d<num>```: Roll a dice with "num" sides
- ```!read <adv>```: Read a adventure file attached to the message and save it as "adv"
- ```!start <adv>```: Start a adventure called "adv"
- ```!default```: Start example adventure

### Especial commands

- ```!pick <opt_id>```: Pick a opt

## Add commands

You can fork this repo and add more custom commands by calling ```bot.add_command(func, pattern)``` variables are defined like the Flask API, using "< variable >" syntax.

Variables are all strings tho.
