"""Level 10 - Crisp geometric sweeps and impossible angles."""

from typing import List, Optional

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 10
LEVEL_NAME = "Vector Vortex"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 13


def _add_balloon(
    balloons: List[Balloon],
    x: float,
    y: float,
    tier: int,
    pattern: str = "vertical",
    pattern_data: Optional[dict] = None,
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
            pattern_data=pattern_data or {},
        )
    )


def _add_chevron(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    phase: float,
    speed_multiplier: float,
) -> None:
    for row, width in enumerate([1, 3, 5, 7]):
        y = center_y - row * STEP * 0.92
        x_start = center_x - (width - 1) * STEP * 0.5
        for col in range(width):
            x = x_start + col * STEP
            tier = (row + col) % 5
            _add_balloon(
                balloons,
                x,
                y,
                tier,
                pattern="wave",
                pattern_data={"amplitude": 22, "frequency": 0.045, "phase": phase + row * 0.35},
                speed_multiplier=speed_multiplier,
            )


def _add_crossfire(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    speed_multiplier: float,
) -> None:
    for offset in [-3, -2, -1, 0, 1, 2, 3]:
        tier = (offset + 5) % 5
        _add_balloon(balloons, center_x + offset * STEP, center_y, tier, speed_multiplier=speed_multiplier)
        if offset != 0:
            _add_balloon(
                balloons,
                center_x,
                center_y - offset * STEP,
                (tier + 2) % 5,
                speed_multiplier=speed_multiplier,
            )


def _add_diagonal_rail(
    balloons: List[Balloon],
    start_x: float,
    start_y: float,
    x_step: float,
    count: int,
    phase: float,
) -> None:
    for index in range(count):
        _add_balloon(
            balloons,
            start_x + index * x_step,
            start_y - index * STEP * 0.78,
            index % 5,
            pattern="zigzag",
            pattern_data={"amplitude": 26, "frequency": 0.05, "phase": phase + index * 0.22},
            speed_multiplier=2.0,
        )


def _add_gate_line(
    balloons: List[Balloon],
    start_y: float,
    vx: float,
    tier_offset: int,
) -> None:
    if vx > 0:
        start_x = -MAX_RADIUS * 2
        spacing = -STEP * 1.05
    else:
        start_x = SCREEN_WIDTH + MAX_RADIUS * 2
        spacing = STEP * 1.05

    for index in range(9):
        _add_balloon(
            balloons,
            start_x + index * spacing,
            start_y,
            (tier_offset + index) % 5,
            pattern="drift",
            pattern_data={"vx": vx, "vy": 1.8, "sway_amplitude": 0.0, "sway_frequency": 0.0},
        )


def create_balloons() -> List[Balloon]:
    """Create disciplined lines, chevrons, and lateral gate sweeps."""
    balloons: List[Balloon] = []

    _add_chevron(balloons, SCREEN_WIDTH / 2, -220, phase=0.0, speed_multiplier=1.95)
    _add_chevron(balloons, SCREEN_WIDTH / 2 - STEP * 2.2, -620, phase=1.1, speed_multiplier=2.0)
    _add_chevron(balloons, SCREEN_WIDTH / 2 + STEP * 2.2, -980, phase=2.2, speed_multiplier=2.05)

    _add_crossfire(balloons, SCREEN_WIDTH / 2, -1360, speed_multiplier=1.95)
    _add_crossfire(balloons, SCREEN_WIDTH / 2, -1640, speed_multiplier=2.05)

    _add_diagonal_rail(balloons, 150, -1940, STEP * 0.95, count=10, phase=0.5)
    _add_diagonal_rail(balloons, SCREEN_WIDTH - 150, -2120, -STEP * 0.95, count=10, phase=1.6)

    _add_gate_line(balloons, start_y=-2380, vx=4.7, tier_offset=0)
    _add_gate_line(balloons, start_y=-2540, vx=-4.7, tier_offset=2)
    _add_gate_line(balloons, start_y=-2700, vx=5.0, tier_offset=1)

    return balloons


def get_total_balloons() -> int:
    return 95
