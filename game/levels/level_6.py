"""Level 6 - Mixed Balloons (15x15 per color) + Special Balloon Test Row."""

from typing import List
from ..enemies import (
    Balloon,
    get_balloon_radius,
    BALLOON_TYPE_BLACK,
    BALLOON_TYPE_WHITE,
    BALLOON_TYPE_LEAD,
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Rainbow Rush"
BALLOON_TIER = 0  # Mixed

SPECIAL_TEST_ROW_Y = -80  # Early spawn for testing special balloons


def create_balloons() -> List[Balloon]:
    """Create 15x15 grid for each balloon type plus special test row (1152 total)."""
    balloons: List[Balloon] = []
    cols = 15
    rows_per_type = 15

    # Use red balloon (smallest) as base for consistent spacing
    balloon_radius = get_balloon_radius(4)
    balloon_diameter = balloon_radius * 2
    gap = balloon_diameter * 0.2
    spacing_x = balloon_diameter + gap

    grid_width = spacing_x * cols - gap
    start_x = (SCREEN_WIDTH - grid_width) / 2 + balloon_radius
    spacing_y = 50

    # Tiers: red(4), blue(3), green(2), yellow(1), pink(0)
    tiers = [4, 3, 2, 1, 0]

    for tier in tiers:
        for row in range(rows_per_type):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = -100 - (row * spacing_y) - (tier * 300)

                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                )
                balloons.append(balloon)

    # Add a full test row of special balloons (black, white, lead) for testing
    special_types = [BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE, BALLOON_TYPE_LEAD]
    special_count = 27  # 9 of each type
    special_spacing = spacing_x * 0.95
    special_start_x = (SCREEN_WIDTH - special_spacing * (special_count - 1)) / 2

    for index in range(special_count):
        balloon_type = special_types[index % 3]
        balloon = Balloon(
            x=special_start_x + index * special_spacing,
            y=SPECIAL_TEST_ROW_Y,
            tier=4,
            speed=BALLOON_SPEED,
            balloon_type=balloon_type,
        )
        balloons.append(balloon)

    return balloons


def get_total_balloons() -> int:
    return 1152
