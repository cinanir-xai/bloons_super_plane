"""Level 6 - All Balloon Types with Layered Cubes."""

from typing import List
from ..enemies import (
    Balloon,
    get_balloon_radius,
    get_balloon_radius_by_type,
    BALLOON_TYPE_BLACK,
    BALLOON_TYPE_WHITE,
    BALLOON_TYPE_LEAD,
    BALLOON_TYPE_ZEBRA,
    BALLOON_TYPE_RAINBOW,
    BALLOON_TYPE_CERAMIC,
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Balloon Showcase"
BALLOON_TIER = 0  # Mixed


def create_balloons() -> List[Balloon]:
    """Create layered cubes of all balloon types for comprehensive testing."""
    balloons: List[Balloon] = []

    # Grid settings
    cols = 15
    rows_per_type = 15

    # Use the largest balloon size (ceramic) as base for consistent spacing
    ceramic_radius = get_balloon_radius_by_type(BALLOON_TYPE_CERAMIC)
    balloon_diameter = ceramic_radius * 2
    gap = balloon_diameter * 0.15
    spacing_x = balloon_diameter + gap

    # Center the grid horizontally
    grid_width = spacing_x * cols - gap
    start_x = (SCREEN_WIDTH - grid_width) / 2 + ceramic_radius

    spacing_y = 52
    current_y = -100

    # Define balloon type layers (top to bottom)
    # Each layer is (balloon_type, rows, tier_for_normal)
    layers = [
        (BALLOON_TYPE_CERAMIC, 8, 4),   # Ceramic cube (8 rows)
        (BALLOON_TYPE_RAINBOW, 8, 4),   # Rainbow cube (8 rows)
        (BALLOON_TYPE_ZEBRA, 8, 4),     # Zebra cube (8 rows)
        (BALLOON_TYPE_LEAD, 8, 4),      # Lead cube (8 rows)
        (BALLOON_TYPE_WHITE, 10, 4),    # White cube (10 rows)
        (BALLOON_TYPE_BLACK, 10, 4),    # Black cube (10 rows)
    ]

    # Add special balloon cubes
    for balloon_type, rows, tier in layers:
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = current_y - row * spacing_y

                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    balloon_type=balloon_type,
                )
                balloons.append(balloon)

        current_y -= rows * spacing_y + 120  # Gap between layers

    # Add normal balloon cubes (existing tier system)
    # Tiers: pink(0), yellow(1), green(2), blue(3), red(4)
    tiers = [0, 1, 2, 3, 4]  # Pink to Red (largest to smallest)

    for tier in tiers:
        for row in range(rows_per_type):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = current_y - row * spacing_y

                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                )
                balloons.append(balloon)

        current_y -= rows_per_type * spacing_y + 100

    return balloons


def get_total_balloons() -> int:
    # Ceramic: 8*15 = 120
    # Rainbow: 8*15 = 120
    # Zebra: 8*15 = 120
    # Lead: 8*15 = 120
    # White: 10*15 = 150
    # Black: 10*15 = 150
    # Pink/Yellow/Green/Blue/Red: 5*15*15 = 1125
    # Total: 1905
    return 1905
