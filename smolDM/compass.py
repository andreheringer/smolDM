"""This module controls the player's motions through the game.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
import random
from typing import Dict, Optional
from smolDM.scenes import Scene


def goto(here: Scene, scenes: Dict[int, Scene], option_id: str) -> Optional[Scene]:
    """Go to scene described in option.

    Args:
        here: Current scene
        scenes: Bot scene structure
        option_id: Option id for current scene.

    Returns:
        Either the new scene loaded or None
    """

    if here is None:
        return None

    cur_options = [
        option for option in here.options if option.option_id == option_id
    ]
    for option in cur_options:
        dice = random.randint(0, 100)
        next_scene = option.destination[dice % len(cur_options)]
        if next_scene == 0:
            here = None
        else:
            here = scenes[next_scene]
    return here
