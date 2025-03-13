"""
The required files for my game
"""

from .g import screen
from .keys import keychecks
from .actor import Actor

__all__ = list(
    {
        "Actor",
        "keychecks",
        "screen"
    }
)