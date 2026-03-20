"""Level 7 - Floral formations with polished circular motion."""

import math
from typing import List

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 7
LEVEL_NAME = "Bloom Ballet"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 12
PETAL_RADIUS = STEP * 1.25
OUTER_RING_RADIUS = STEP * 2.3
BUD_RADIUS = STEP * 0.95


def _add_balloon(
    balloons: List[Balloon],
    x: float,
    y: float,
    tier: int,
    speed_multiplier: float,
    pattern: str,
    pattern_data: dict,
) -> None:
    balloons.append(
        Balloon(
            x=x,
            y=y,
            tier=tier,
            speed=BALLOON_SPEED,
            speed_multiplier=speed_multiplier,
            pattern=pattern,
            pattern_data=pattern_data,
        )
    )


def _add_large_bloom(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    motion = {"radius": 0.0, "frequency": 0.05, "phase": phase}
    _add_balloon(balloons, center_x, center_y, 1, speed_multiplier, "circular", dict(motion))

    for index in range(8):
        angle = index * (math.tau / 8)
        x = center_x + math.cos(angle) * PETAL_RADIUS
        y = center_y + math.sin(angle) * PETAL_RADIUS * 0.86
        tier = 0 if index % 2 == 0 else 4
        _add_balloon(balloons, x, y, tier, speed_multiplier, "circular", dict(motion))

    for index in range(16):
        angle = index * (math.tau / 16) + math.pi / 16
        x = center_x + math.cos(angle) * OUTER_RING_RADIUS
        y = center_y + math.sin(angle) * OUTER_RING_RADIUS * 0.86
        tier = 2 if index % 2 == 0 else 3
        _add_balloon(balloons, x, y, tier, speed_multiplier, "circular", dict(motion))

    for leaf_x in (-0.9, 0.9):
        _add_balloon(
            balloons,
            center_x + leaf_x * STEP,
            center_y + STEP * 2.45,
            2,
            speed_multiplier,
            "circular",
            dict(motion),
        )


def _add_bud(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    motion = {"amplitude": 34, "frequency": 0.04, "phase": phase}
    _add_balloon(balloons, center_x, center_y, 1, speed_multiplier, "wave", dict(motion))

    for index in range(6):
        angle = -math.pi / 2 + index * (math.tau / 6)
        x = center_x + math.cos(angle) * BUD_RADIUS
        y = center_y + math.sin(angle) * BUD_RADIUS * 0.88
        tier = 0 if index in (0, 1, 5) else 4
        _add_balloon(balloons, x, y, tier, speed_multiplier, "wave", dict(motion))

    for leaf_x in (-0.72, 0.72):
        _add_balloon(
            balloons,
            center_x + leaf_x * STEP,
            center_y + STEP * 1.6,
            2,
            speed_multiplier,
            "wave",
            dict(motion),
        )


def _add_vine_arc(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    speed_multiplier: float,
) -> None:
    motion = {"amplitude": 28, "frequency": 0.035, "phase": 1.4}
    offsets = [-4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    for index, dx in enumerate(offsets):
        arch = 1.0 - (dx / 4.8) ** 2
        x = center_x + dx * STEP
        y = center_y - arch * STEP * 1.2
        tier = 2 if index % 2 == 0 else 1
        _add_balloon(balloons, x, y, tier, speed_multiplier, "wave", dict(motion))


def create_balloons() -> List[Balloon]:
    """Create layered floral set pieces with clean spacing and motion."""
    balloons: List[Balloon] = []

    first_row_x = [220, SCREEN_WIDTH / 2, SCREEN_WIDTH - 220]
    for index, x in enumerate(first_row_x):
        _add_large_bloom(
            balloons,
            x,
            -240,
            phase=index * 0.8,
            speed_multiplier=1.9,
        )

    second_row_x = [340, SCREEN_WIDTH - 340]
    for index, x in enumerate(second_row_x):
        _add_large_bloom(
            balloons,
            x,
            -760,
            phase=1.0 + index * 1.2,
            speed_multiplier=2.1,
        )

    _add_vine_arc(balloons, SCREEN_WIDTH / 2, -1120, speed_multiplier=1.8)

    bud_positions = [180, 420, 705, 945]
    for index, x in enumerate(bud_positions):
        _add_bud(
            balloons,
            x,
            -1360 - (index % 2) * 80,
            phase=index * 0.9,
            speed_multiplier=1.85,
        )

    return balloons


def get_total_balloons() -> int:
    return 181
