import pytest
from crael.scenes import SceneLoader


@pytest.fixture
def scene_loader_instance():
    loader = SceneLoader()
    return loader


def test_load_scenes(scene_loader_instance):
    scenes = scene_loader_instance.load_scenes(
        "/home/andre/Projects/crael/tests/mock_game/scene1.md"
    )
    assert scenes is not None
    assert len(scenes) == 2
    assert scenes[1].title == "# Scene 1\n"
    assert len(scenes[1].options) == 2
