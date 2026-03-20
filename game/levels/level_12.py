"""Level 12 - Finale collage mixing all late-game motifs."""

import math
from typing import List

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 12
LEVEL_NAME = "Sky Parade Finale"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 12
ROSETTE_INNER = STEP * 1.45
ROSETTE_OUTER = STEP * 2.45


def _add_balloon(
    balloons: List[Balloon],
    x: float,
    y: float,
    tier: int,
    pattern: str,
    pattern_data: dict,
    speed_multiplier: float = 1.0,
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


def _add_rosette(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    motion = {"radius": 10, "frequency": 0.05, "phase": phase}
    _add_balloon(balloons, center_x, center_y, 4, "circular", dict(motion), speed_multiplier)
    for index in range(12):
        angle = index * (math.tau / 12)
        radius = ROSETTE_OUTER if index % 2 == 0 else ROSETTE_INNER
        tier = 0 if index % 3 == 0 else 1 if index % 3 == 1 else 3
        _add_balloon(
            balloons,
            center_x + math.cos(angle) * radius,
            center_y + math.sin(angle) * radius,
            tier,
            "circular",
            dict(motion),
            speed_multiplier,
        )


def _add_ribbon_line(
    balloons: List[Balloon],
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    xs = [135, 240, 345, 450, 555, 660, 765, 870, 975]
    for index, x in enumerate(xs):
        _add_balloon(
            balloons,
            x,
            center_y + (-1 if index % 2 == 0 else 1) * STEP * 0.52,
            (index + 1) % 5,
            "wave",
            {"amplitude": 34, "frequency": 0.05, "phase": phase + index * 0.22},
            speed_multiplier,
        )


def _add_bee(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
) -> None:
    motion = {"amplitude": 28, "frequency": 0.05, "phase": phase}
    offsets = [(-1.5, 0.0, 4), (-0.5, 0.0, 1), (0.5, 0.0, 4), (1.5, 0.0, 1), (2.5, 0.0, 4)]
    for offset_x, offset_y, tier in offsets:
        _add_balloon(
            balloons,
            center_x + offset_x * STEP * 0.92,
            center_y + offset_y * STEP,
            tier,
            "wave",
            dict(motion),
            2.0,
        )
    for wing_x, wing_y in [(-0.5, -1.0), (1.5, -1.0)]:
        _add_balloon(
            balloons,
            center_x + wing_x * STEP * 0.92,
            center_y + wing_y * STEP,
            3,
            "wave",
            dict(motion),
            2.0,
        )
    _add_balloon(
        balloons,
        center_x + 3.45 * STEP * 0.92,
        center_y - 0.1 * STEP,
        0,
        "wave",
        dict(motion),
        2.0,
    )


def _add_starburst_comets(
    balloons: List[Balloon],
    start_x: float,
    start_y: float,
    vx: float,
    phase: float,
) -> None:
    for index in range(9):
        _add_balloon(
            balloons,
            start_x + (-1 if vx > 0 else 1) * index * STEP,
            start_y - index * STEP * 0.4,
            index % 5,
            "drift",
            {
                "vx": vx,
                "vy": 2.2,
                "sway_amplitude": 0.38,
                "sway_frequency": 0.05,
                "phase": phase + index * 0.25,
            },
            1.0,
        )


def _add_orchard_block(
    balloons: List[Balloon],
    start_x: float,
    start_y: float,
    vx: float,
    phase: float,
) -> None:
    for row in range(4):
        for col in range(4):
            _add_balloon(
                balloons,
                start_x + col * STEP * 0.98,
                start_y - row * STEP * 0.9,
                (row + col) % 5,
                "drift",
                {
                    "vx": vx,
                    "vy": 2.7,
                    "sway_amplitude": 2.1,
                    "sway_frequency": 0.04,
                    "phase": phase + row * 0.45,
                },
            )


def create_balloons() -> List[Balloon]:
    """Create a finale that revisits every upgraded late-game pattern."""
    balloons: List[Balloon] = []

    _add_rosette(balloons, 260, -240, phase=0.0, speed_multiplier=2.0)
    _add_rosette(balloons, SCREEN_WIDTH - 260, -560, phase=1.0, speed_multiplier=2.05)
    _add_rosette(balloons, SCREEN_WIDTH / 2, -900, phase=2.1, speed_multiplier=2.1)

    _add_ribbon_line(balloons, -1240, phase=0.0, speed_multiplier=2.0)
    _add_ribbon_line(balloons, -1400, phase=1.2, speed_multiplier=2.05)

    _add_bee(balloons, 280, -1700, phase=0.4)
    _add_bee(balloons, SCREEN_WIDTH - 310, -1880, phase=1.4)

    _add_starburst_comets(balloons, -160, -2140, vx=4.0, phase=0.0)
    _add_starburst_comets(balloons, SCREEN_WIDTH + 160, -2300, vx=-4.0, phase=1.8)

    _add_orchard_block(balloons, start_x=-220, start_y=-2560, vx=3.1, phase=0.2)
    _add_orchard_block(balloons, start_x=SCREEN_WIDTH - 90, start_y=-2820, vx=-3.1, phase=1.6)

    return balloons


def get_total_balloons() -> int:
    return 115
