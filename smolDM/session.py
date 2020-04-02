from discord.channel import TextChannel
from dataclasses import dataclass
from typing import Dict, Optional
import smolDM.scenes as scenes


@dataclass
class Session:
    """Session struct."""

    player: str
    scenes: Dict[int, scenes.Scene]
    here: Optional[scenes.Scene]
    channel: TextChannel


def start_session(player, channel, scenes, here=None) -> Session:
    """
    """
    if here is None:
        here = scenes[1]
    return Session(player, scenes, here, channel)
