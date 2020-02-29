import re
from dataclasses import dataclass
from typing import List


@dataclass
class Scene:
    """
        This appers there?
    """
    scene_id: int
    title: str
    lines: List[str]
    options: str

    def __str__(self):
        return f"A sacene in the Crael game"


class SceneLoader:

    def __init__(self):
        self.scene_re = re.compile(r"^\#\s*={5}")
        self.scene_list = list()

    def parse_scene(self, reset):
        
        if reset:
            self.parse_scene.counter = 0
        title = 
        return Scene(self.parse_scene.counter,)

    def load_scenes(self, scene_file_path):
        with open(scene_file_path) as scene_file:
            yield ##scene_raw
