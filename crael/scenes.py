"""
This module defines the Scene related interfaces.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Scene:
    """Data class representing a crael Scene."""

    scene_id: int
    title: str
    lines: List[str]
    options: List[str]


class SceneLoader:
    """This class loads scenes from markdown files."""

    def __init__(self):
        """Initiaze SceneLoader.

        The regular expressions match multiple scene attributes
        """
        # Thank you Ciça for the regex help
        self._scene_re = r"^\#\s(?:.|\n)*?\={5}$"
        self._scene_title_re = r"^\#.*\n"
        self._scene_edge_re = r"^[1-99].\s"

    def _parse_scene(self, scene_content: str, scene_num: int) -> Scene:
        lines = list()
        options = list()
        for scene_att in scene_content.splitlines(True):
            title_match = re.match(self._scene_title_re, scene_att)
            if title_match:
                title = title_match.group()
                continue
            option_match = re.match(self._scene_edge_re, scene_att)
            if option_match:
                options.append(option_match.group())
                continue
            lines.append(scene_att)
        return Scene(scene_num, title, lines, options)

    def load_scenes(self, scene_file_path: str) -> Dict[int, Scene]:
        """Load scenes from file path.

        Args:
            scene_file_path: mardown file with scene definitions

        Returns:
            scenes: Dictionary with numbered keys and Snece object values

        """
        scenes = dict()
        scene_file = open(scene_file_path, "r")
        scene_file_content = scene_file.read()
        scene_file.close()
        matches = re.finditer(self._scene_re, scene_file_content, re.MULTILINE)
        for scene_num, scene_match in enumerate(matches, start=1):
            scenes[scene_num] = self._parse_scene(scene_match.group(0), scene_num)
        return scenes
