"""
This module defines the compass class.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
import random
from smolDM.scenes import SceneLoader as scene_loader
from smolDM.scenes import Scene


class Compass:
    """This class controls where the player is in regards to the adventure."""

    def __init__(self, scenes_file):
        """Compass init method."""

        self._scenes = scene_loader.load_scenes(scenes_file)
        self._here = self._scenes[1]

    def cur_scene(self):
        """Return current scene."""
        return self._here

    def goto(self, option_id: str) -> Scene:
        """Go to scene described in option.

        Args:
            option_id: Option id for current scene.
        """

        if self._here is None:
            return None

        cur_options = [
            option for option in self._here.options if option.option_id == option_id
        ]
        for option in cur_options:
            dice = random.randint(0, 100)
            next_scene = option.destination[dice % len(cur_options)]
            if next_scene == 0:
                self._here = None
            else:
                self._here = self._scenes[next_scene]
        return self._here
