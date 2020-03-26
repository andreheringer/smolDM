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

        self._here = None
        self._scenes = scene_loader.load_scenes(scenes_file)

    def cur_scene(self):
        """
        """
        if self._here is None:
            self._here = self._scenes[1]
        return self._here

    def goto(self, option_id: str) -> Scene:
        """
        """
        cur_options = [
            option for option in self._here.options if option.option_id == option_id
        ]
        for option in cur_options:
            dice = random.randint(0, 100)
            next_scene = option.destination[dice % len(cur_options)]
            self._here = self._scenes[next_scene]
        return self._here
