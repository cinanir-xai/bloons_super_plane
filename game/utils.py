"""Utility functions for the game."""

import math
import random
from typing import Tuple, List

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def lerp_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Linear interpolation between two colors."""
    return (
        int(lerp(color1[0], color2[0], t)),
        int(lerp(color1[1], color2[1], t)),
        int(lerp(color1[2], color2[2], t))
    )


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_to(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate angle from point 1 to point 2 in radians."""
    return math.atan2(y2 - y1, x2 - x1)


def random_in_range(min_val: float, max_val: float) -> float:
    """Generate random float in range."""
    return random.uniform(min_val, max_val)


def random_color_variation(base_color: Tuple[int, int, int], variation: int = 30) -> Tuple[int, int, int]:
    """Add random variation to a color."""
    return (
        clamp(base_color[0] + random.randint(-variation, variation), 0, 255),
        clamp(base_color[1] + random.randint(-variation, variation), 0, 255),
        clamp(base_color[2] + random.randint(-variation, variation), 0, 255)
    )


def wrap_position(x: float, y: float, width: float, height: float) -> Tuple[float, float]:
    """Wrap position around screen edges."""
    return (
        x % width if x < 0 or x > width else x,
        y % height if y < 0 or y > height else y
    )


def off_screen(x: float, y: float, margin: float = 50) -> bool:
    """Check if position is off screen."""
    return x < -margin or x > SCREEN_WIDTH + margin or y < -margin or y > SCREEN_HEIGHT + margin
