import pytest
from pathlib import Path
import smolDM.scenes as scene



@pytest.fixture
def mock_game_file():
    path = Path(__file__).parent.absolute() / "mock_game/scene1.md"
    return path


def test_load_scenes(mock_game_file):
    scenes = scene.load_scenes(mock_game_file)
    assert scenes is not None
    assert len(scenes) == 2
    assert scenes[1].title == "# Scene 1\n"


def test_load_options(mock_game_file):
    scenes = scene.load_scenes(mock_game_file)
    assert scenes[1].options is not None
    assert type(scenes[1].options[0].destination) is list
