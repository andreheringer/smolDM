"""This module defines the Scene related interfaces.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
import re
from dataclasses import dataclass
from typing import List, Dict, Sequence
from loguru import logger


# Thank you Ciça for the regex help
SCENE_RE = r"^\#\s(?:.|\n)*?\={5}$"
SCENE_TITLE_RE = r"^\#.*\n"
SCENE_EDGE_RE = r"^(\d+).\s(.*)\${(.*)}"


@dataclass
class Option:
    """Data class representing a Option the player have."""

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


def _parse_option(option_param_seq: Sequence) -> Option:
    dests = [int(dest) for dest in option_param_seq[2].split("/")]
    return Option(option_param_seq[0], dests, option_param_seq[1])


def _parse_scene(scene_content: str, scene_num: int) -> Scene:
    lines = list()
    options = list()
    for scene_att in scene_content.splitlines(True):
        title_match = re.match(SCENE_TITLE_RE, scene_att)
        if title_match:
            title = title_match.group()
            continue
        option_match = re.match(SCENE_EDGE_RE, scene_att)
        if option_match:
            options.append(_parse_option(option_match.groups()))
            continue
        lines.append(scene_att)
    return Scene(scene_num, title, lines, options)


def load_scenes(scene_file_path: str) -> Dict[int, Scene]:
    """Load scenes from file path.

    Args:
        scene_file_path: file with scene definitions

    Returns:
        scenes: Dictionary with numbered keys and Snece object values, starts from 1

    """
    scenes = dict()
    scene_file = open(scene_file_path, "r")
    logger.info("Attemping to read adventure file content.")
    scene_file_content = scene_file.read()
    scene_file.close()
    logger.info("Loading scenes....")
    matches = re.finditer(SCENE_RE, scene_file_content, re.MULTILINE)
    for scene_num, scene_match in enumerate(matches, start=1):
        logger.debug(f"Loading scene {scene_num}...")
        scenes[scene_num] = _parse_scene(scene_match.group(), scene_num)
    return scenes
