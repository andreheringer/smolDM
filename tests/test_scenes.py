import pytest
from pathlib import Path
from smolDM.scenes import SceneLoader


@pytest.fixture
def scene_loader_instance():
    loader = SceneLoader()
    return loader


@pytest.fixture
def mock_game_file():
    path = Path(__file__).parent.absolute() / "mock_game/scene1.md"
    return path


def test_load_scenes(scene_loader_instance, mock_game_file):
    scenes = scene_loader_instance.load_scenes(mock_game_file)
    assert scenes is not None
    assert len(scenes) == 2
    assert scenes[1].title == "# Scene 1\n"


def test_load_options(scene_loader_instance, mock_game_file):
    scenes = scene_loader_instance.load_scenes(mock_game_file)
    assert scenes[1].options is not None
    assert type(scenes[1].options[0].destination) is list
