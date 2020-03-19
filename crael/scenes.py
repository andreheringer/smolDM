"""
"""
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Scene:
    """
    """

    scene_id: int
    title: str
    lines: List[str]
    options: List[str]

    def __str__(self):
        return f"A sacene in the Crael game"


class SceneLoader:
    """
    """

    def __init__(self):
        """
        """
        # Thank you Ciça for the regex help
        self._scene_re = r"^\#\s(?:.|\n)*?\={5}$"
        self._scene_title_re = r"^\#.*\n"
        self._scene_edge_re = r"^[1-9].\s"

    def _parse_scene(self, scene_content, scene_num):
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

    def load_scenes(self, scene_file_path):
        """
        """
        scenes = dict()
        scene_file = open(scene_file_path, "r")
        scene_file_content = scene_file.read()
        scene_file.close()
        matches = re.finditer(self._scene_re, scene_file_content, re.MULTILINE)
        for scene_num, scene_match in enumerate(matches, start=1):
            scenes[scene_num] = self._parse_scene(scene_match.group(0), scene_num)
        return scenes
