"""Level 8 - Starburst constellations and gliding lanes."""

import math
from typing import List

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 8
LEVEL_NAME = "Starfall Run"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 12
STAR_INNER = STEP * 1.55
STAR_OUTER = STEP * 3.1
COMET_STEP = STEP * 1.08


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


def _add_star(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    motion = {"radius": 8, "frequency": 0.05, "phase": phase}
    _add_balloon(balloons, center_x, center_y, 4, speed_multiplier, "circular", dict(motion))

    for index in range(10):
        angle = -math.pi / 2 + index * (math.tau / 10)
        radius = STAR_OUTER if index % 2 == 0 else STAR_INNER
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        tier = 1 if index % 2 == 0 else 3
        _add_balloon(balloons, x, y, tier, speed_multiplier, "circular", dict(motion))

    side_angles = [-0.88, 0.88, math.pi - 0.88, math.pi + 0.88]
    for index, angle in enumerate(side_angles):
        x = center_x + math.cos(angle) * STEP * 1.9
        y = center_y + math.sin(angle) * STEP * 1.1
        tier = 0 if index < 2 else 2
        _add_balloon(balloons, x, y, tier, speed_multiplier, "circular", dict(motion))


def _add_comet_lane(
    balloons: List[Balloon],
    start_x: float,
    start_y: float,
    count: int,
    vx: float,
    vy: float,
    sway_phase: float,
) -> None:
    for index in range(count):
        x = start_x - index * COMET_STEP * 0.95
        y = start_y - index * COMET_STEP * 0.42
        tier = 4 if index < 2 else 3 if index < 5 else 1 if index < 8 else 0
        _add_balloon(
            balloons,
            x,
            y,
            tier,
            speed_multiplier=1.0,
            pattern="drift",
            pattern_data={
                "vx": vx,
                "vy": vy,
                "sway_amplitude": 12,
                "sway_frequency": 0.05,
                "phase": sway_phase + index * 0.22,
            },
        )


def _add_spark_band(
    balloons: List[Balloon],
    center_y: float,
    direction: float,
    speed_multiplier: float,
) -> None:
    xs = [160, 300, 440, 580, 720, 860, 1000]
    for index, x in enumerate(xs):
        _add_balloon(
            balloons,
            x,
            center_y + (-1 if index % 2 == 0 else 1) * STEP * 0.45,
            index % 5,
            speed_multiplier,
            "wave",
            {"amplitude": 30 * direction, "frequency": 0.05, "phase": index * 0.45},
        )


def create_balloons() -> List[Balloon]:
    """Create star shapes, comet tails, and sparkling crosswinds."""
    balloons: List[Balloon] = []

    _add_star(balloons, 260, -260, phase=0.0, speed_multiplier=2.0)
    _add_star(balloons, SCREEN_WIDTH - 260, -640, phase=1.1, speed_multiplier=2.1)
    _add_star(balloons, SCREEN_WIDTH / 2, -1040, phase=2.0, speed_multiplier=2.15)

    _add_comet_lane(balloons, -140, -1340, count=11, vx=3.6, vy=2.25, sway_phase=0.0)
    _add_comet_lane(
        balloons,
        SCREEN_WIDTH + 140,
        -1540,
        count=11,
        vx=-3.6,
        vy=2.35,
        sway_phase=1.7,
    )
    _add_comet_lane(balloons, -220, -1740, count=11, vx=3.9, vy=2.45, sway_phase=3.2)

    _add_spark_band(balloons, -2040, direction=1.0, speed_multiplier=1.9)
    _add_spark_band(balloons, -2220, direction=-1.0, speed_multiplier=2.0)
    _add_spark_band(balloons, -2400, direction=1.0, speed_multiplier=2.1)

    return balloons


def get_total_balloons() -> int:
    return 99
