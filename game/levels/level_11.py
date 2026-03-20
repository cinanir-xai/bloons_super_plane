"""Level 11 - Orchard motifs and zigzagging balloon blocks."""

from typing import List

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 11
LEVEL_NAME = "Orchard Overdrive"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 12
APPLE_STEP = STEP * 0.94


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


def _add_apple(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    motion = {"radius": 5, "frequency": 0.04, "phase": phase}
    body_points = [
        (-1.0, -1.0, 4),
        (1.0, -1.0, 4),
        (-1.8, 0.0, 4),
        (0.0, -0.1, 1),
        (1.8, 0.0, 4),
        (-2.1, 1.1, 4),
        (-0.7, 1.1, 1),
        (0.7, 1.1, 1),
        (2.1, 1.1, 4),
        (-1.3, 2.1, 4),
        (1.3, 2.1, 4),
        (0.0, 2.85, 4),
    ]
    for offset_x, offset_y, tier in body_points:
        _add_balloon(
            balloons,
            center_x + offset_x * APPLE_STEP,
            center_y + offset_y * APPLE_STEP,
            tier,
            "circular",
            dict(motion),
            speed_multiplier=speed_multiplier,
        )

    _add_balloon(
        balloons,
        center_x + 1.35 * APPLE_STEP,
        center_y - 2.0 * APPLE_STEP,
        2,
        "circular",
        dict(motion),
        speed_multiplier=speed_multiplier,
    )
    _add_balloon(
        balloons,
        center_x,
        center_y - 2.45 * APPLE_STEP,
        3,
        "circular",
        dict(motion),
        speed_multiplier=speed_multiplier,
    )


def _add_leaf_swoosh(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
) -> None:
    offsets = [(-3.0, 0.5), (-2.0, 0.0), (-1.0, -0.4), (0.0, -0.7), (1.0, -0.55), (2.0, -0.1), (3.0, 0.45)]
    for index, (offset_x, offset_y) in enumerate(offsets):
        _add_balloon(
            balloons,
            center_x + offset_x * STEP,
            center_y + offset_y * STEP,
            2 if index in (0, 6) else 1 if index in (2, 4) else 3,
            "wave",
            {"amplitude": 24, "frequency": 0.05, "phase": phase + index * 0.2},
            speed_multiplier=1.9,
        )


def _add_zigzag_block(
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
                    "vy": 2.55,
                    "sway_amplitude": 2.0,
                    "sway_frequency": 0.04,
                    "phase": phase + row * 0.55,
                },
            )


def create_balloons() -> List[Balloon]:
    """Create apples, leaf arcs, and chunky zigzag orchard blocks."""
    balloons: List[Balloon] = []

    _add_apple(balloons, 280, -240, phase=0.0, speed_multiplier=1.9)
    _add_apple(balloons, SCREEN_WIDTH - 280, -700, phase=1.2, speed_multiplier=2.0)
    _add_apple(balloons, SCREEN_WIDTH / 2, -1160, phase=2.1, speed_multiplier=2.05)

    _add_leaf_swoosh(balloons, 300, -1500, phase=0.4)
    _add_leaf_swoosh(balloons, SCREEN_WIDTH - 300, -1680, phase=1.1)
    _add_leaf_swoosh(balloons, SCREEN_WIDTH / 2, -1860, phase=2.0)

    _add_zigzag_block(balloons, start_x=-230, start_y=-2140, vx=3.0, phase=0.0)
    _add_zigzag_block(balloons, start_x=-360, start_y=-2440, vx=3.4, phase=1.7)

    return balloons


def get_total_balloons() -> int:
    return 95
