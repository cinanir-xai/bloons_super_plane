"""Level 9 - Side-entry squadrons, bees, and aggressive sweeps."""

from typing import List

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import Balloon, get_balloon_radius

LEVEL_NUMBER = 9
LEVEL_NAME = "Honeycomb Havoc"
BALLOON_TIER = 0

MAX_RADIUS = get_balloon_radius(0)
STEP = MAX_RADIUS * 2 + 12
BEE_BODY_STEP = STEP * 0.95


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


def _add_scout_line(
    balloons: List[Balloon],
    start_y: float,
    vx: float,
    count: int,
    phase_offset: float,
) -> None:
    if vx > 0:
        start_x = -MAX_RADIUS * 2
        spacing = -STEP * 1.08
    else:
        start_x = SCREEN_WIDTH + MAX_RADIUS * 2
        spacing = STEP * 1.08

    for index in range(count):
        _add_balloon(
            balloons,
            start_x + index * spacing,
            start_y - index * STEP * 0.26,
            index % 5,
            "drift",
            {
                "vx": vx,
                "vy": 1.9,
                "sway_amplitude": 0.18,
                "sway_frequency": 0.05,
                "phase": phase_offset + index * 0.35,
            },
        )


def _add_bee(
    balloons: List[Balloon],
    center_x: float,
    center_y: float,
    wave_phase: float,
) -> None:
    motion = {"amplitude": 32, "frequency": 0.05, "phase": wave_phase}
    for offset_x, offset_y, tier in [
        (-1.5, 0.0, 4),
        (-0.5, 0.0, 1),
        (0.5, 0.0, 4),
        (1.5, 0.0, 1),
        (2.5, 0.0, 4),
    ]:
        _add_balloon(
            balloons,
            center_x + offset_x * BEE_BODY_STEP,
            center_y + offset_y * BEE_BODY_STEP,
            tier,
            "wave",
            dict(motion),
            speed_multiplier=1.95,
        )

    for wing_x, wing_y in [(-0.5, -1.05), (1.5, -1.05)]:
        _add_balloon(
            balloons,
            center_x + wing_x * BEE_BODY_STEP,
            center_y + wing_y * BEE_BODY_STEP,
            3,
            "wave",
            dict(motion),
            speed_multiplier=1.95,
        )

    _add_balloon(
        balloons,
        center_x + 3.55 * BEE_BODY_STEP,
        center_y - 0.15 * BEE_BODY_STEP,
        0,
        "wave",
        dict(motion),
        speed_multiplier=1.95,
    )


def _add_honeycomb_block(
    balloons: List[Balloon],
    start_x: float,
    start_y: float,
    vx: float,
    sway_phase: float,
) -> None:
    rows = 4
    cols = 4
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * STEP * 0.98 + (row % 2) * STEP * 0.49
            y = start_y - row * STEP * 0.88
            tier = (row + col) % 5
            _add_balloon(
                balloons,
                x,
                y,
                tier,
                "drift",
                {
                    "vx": vx,
                    "vy": 2.4,
                    "sway_amplitude": 1.15,
                    "sway_frequency": 0.035,
                    "phase": sway_phase + row * 0.6,
                },
            )


def create_balloons() -> List[Balloon]:
    """Create lateral attack lines and bee-themed formations."""
    balloons: List[Balloon] = []

    _add_scout_line(balloons, start_y=-180, vx=4.6, count=10, phase_offset=0.0)
    _add_scout_line(balloons, start_y=-420, vx=-4.6, count=10, phase_offset=1.5)
    _add_scout_line(balloons, start_y=-660, vx=4.9, count=10, phase_offset=2.7)

    _add_bee(balloons, 280, -980, wave_phase=0.0)
    _add_bee(balloons, SCREEN_WIDTH - 310, -1160, wave_phase=1.2)
    _add_bee(balloons, SCREEN_WIDTH / 2, -1340, wave_phase=2.3)

    _add_honeycomb_block(balloons, start_x=-220, start_y=-1640, vx=3.2, sway_phase=0.6)
    _add_honeycomb_block(
        balloons,
        start_x=SCREEN_WIDTH - 80,
        start_y=-1880,
        vx=-3.2,
        sway_phase=2.2,
    )

    return balloons


def get_total_balloons() -> int:
    return 83
