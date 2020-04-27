# SmolDM

Very smol Dungeon Master for one shot RPG sessions.

This project was built intending to be a Python exercise. I love Python and want to keep working with it even tho my current work place is a Java shop.

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

## Example adventure file

```
# Scene 1

This is an amazing adventure!
Welcome to the first scene.
Now, imagine a fantastic lore description here, and then pick your option with "!pick <option-id>" command

1. Option 1: go to scene 2 ${2}
2. Option 2: end adventure ${0}

=======================================

# Scene 2
This is the second scene 
I will now make a dramatic pause...




Uuuhhh...thriller...

1. Option 1: go back to scene 1 ${1}
2. Option 2: end adventure ${0}

=====================================
```
