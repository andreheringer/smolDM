"""This module contros session initialization and mutability.

:copywrite: Andre Heringer 2018-2019
:license: MIT, see license for details
"""
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
    """Start session.

    Args:
        channel: Session channel
        scenes: Adventure's scenes available in session
        here: Optional adventures starting point, defaults to scenes[1]
    Returns:
        A session object
    """
    if here is None:
        here = scenes[1]
    return Session(player, scenes, here, channel)
