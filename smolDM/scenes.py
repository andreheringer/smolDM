"""
This module defines the Scene related interfaces.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
import re
from dataclasses import dataclass
from typing import List, Dict, Sequence


@dataclass
class Option:
    """Data class representing Option the player have."""

    option_id: int
    destination: List[int]
    description: str


@dataclass
class Scene:
    """Data class representing a Scene."""

    scene_id: int
    title: str
    lines: List[str]
    options: List[Option]


class SceneLoader:
    """This class loads scenes from files."""

    # Thank you Ciça for the regex help
    SCENE_RE = r"^\#\s(?:.|\n)*?\={5}$"
    SCENE_TITLE_RE = r"^\#.*\n"
    SCENE_EDGE_RE = r"^(\d+).\s(.*)\${(.*)}"

    def _parse_option(option_param_seq: Sequence) -> Option:
        dests = [int(dest) for dest in option_param_seq[2].split("/")]
        return Option(option_param_seq[0], dests, option_param_seq[1])

    def _parse_scene(scene_content: str, scene_num: int) -> Scene:
        lines = list()
        options = list()
        for scene_att in scene_content.splitlines(True):
            title_match = re.match(SceneLoader.SCENE_TITLE_RE, scene_att)
            if title_match:
                title = title_match.group()
                continue
            option_match = re.match(SceneLoader.SCENE_EDGE_RE, scene_att)
            if option_match:
                options.append(SceneLoader._parse_option(option_match.groups()))
                continue
            lines.append(scene_att)
        return Scene(scene_num, title, lines, options)

    @staticmethod
    def load_scenes(scene_file_path: str) -> Dict[int, Scene]:
        """Load scenes from file path.

        Args:
            scene_file_path: file with scene definitions

        Returns:
            scenes: Dictionary with numbered keys and Snece object values

        """
        scenes = dict()
        scene_file = open(scene_file_path, "r")
        scene_file_content = scene_file.read()
        scene_file.close()
        matches = re.finditer(SceneLoader.SCENE_RE, scene_file_content, re.MULTILINE)
        for scene_num, scene_match in enumerate(matches, start=1):
            scenes[scene_num] = SceneLoader._parse_scene(scene_match.group(), scene_num)
        return scenes
