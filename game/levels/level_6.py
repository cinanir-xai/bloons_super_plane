"""Level 6 - MOAB Boss Battle."""

from typing import List, Tuple
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
    BALLOON_TYPE_MOAB,
    MOAB_WIDTH,
    MOAB_HEIGHT,
    MOAB_HP,
)
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "MOAB Arrival"
BALLOON_TIER = 0  # Mixed

# MOAB moves much slower than regular balloons
MOAB_SPEED = BALLOON_SPEED * 0.25  # 25% of normal speed


def create_balloons() -> List[Balloon]:
    """Create the MOAB boss that spawns immediately at the start."""
    balloons: List[Balloon] = []
    
    # Spawn MOAB at center-top of screen
    moab = Balloon(
        x=SCREEN_WIDTH / 2,
        y=-MOAB_HEIGHT / 2 - 20,  # Start just above screen
        tier=4,  # Not used for MOAB but required
        speed=MOAB_SPEED,
        balloon_type=BALLOON_TYPE_MOAB,
    )
    balloons.append(moab)
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Return balloons that spawn after delays.
    
    Returns list of (delay_seconds, balloons) tuples.
    The layered balloon cubes spawn 30 seconds after the MOAB.
    """
    delayed: List[Tuple[float, List[Balloon]]] = []
    
    # Create the layered balloon cubes that spawn 30 seconds later
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
    
    # 30 second delay before the balloon cubes spawn
    delayed.append((30.0, balloons))
    
    return delayed


def get_total_balloons() -> int:
    # MOAB: 1
    # Ceramic: 8*15 = 120
    # Rainbow: 8*15 = 120
    # Zebra: 8*15 = 120
    # Lead: 8*15 = 120
    # White: 10*15 = 150
    # Black: 10*15 = 150
    # Pink/Yellow/Green/Blue/Red: 5*15*15 = 1125
    # Total: 1906
    return 1906
