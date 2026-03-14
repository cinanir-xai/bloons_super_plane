"""Sky Defender Game Package.

A modular vertical top-down shooter game.
"""

from .constants import *
from .game import Game, main
from .player import Player
from .projectiles import Dart, DartManager
from .background import Background
from .effects import (
    Particle, ParticleSystem, EngineGlow, MuzzleFlash, DartTrail
)
from .utils import *

__version__ = "1.0.0"
__all__ = [
    # Game
    "Game", "main",
    # Player
    "Player",
    # Projectiles
    "Dart", "DartManager",
    # Background
    "Background",
    # Effects
    "Particle", "ParticleSystem", "EngineGlow", "MuzzleFlash", "DartTrail",
    # Constants
    "SCREEN_WIDTH", "SCREEN_HEIGHT",
    # Utils
    "clamp", "lerp", "lerp_color", "distance", "angle_to",
    "random_in_range", "random_color_variation", "wrap_position", "off_screen",
]
