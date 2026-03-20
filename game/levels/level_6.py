"""Level 6 - MOAB and BFB Boss Battle."""

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
    BALLOON_TYPE_BFB,
    MOAB_WIDTH,
    MOAB_HEIGHT,
    MOAB_HP,
    BFB_WIDTH,
    BFB_HEIGHT,
    BFB_HP,
)
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Boss Battle"
BALLOON_TIER = 0  # Mixed

# MOAB moves much slower than regular balloons
MOAB_SPEED = BALLOON_SPEED * 0.25  # 25% of normal speed
# BFB moves 50% slower than MOAB
BFB_SPEED = MOAB_SPEED * 0.5  # 12.5% of normal speed


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
    - BFB spawns 30 seconds after MOAB
    - The layered balloon cubes spawn 60 seconds after BFB (90 seconds total)
    """
    delayed: List[Tuple[float, List[Balloon]]] = []
    
    # BFB spawns 30 seconds after MOAB
    bfb = Balloon(
        x=SCREEN_WIDTH / 2,
        y=-BFB_HEIGHT / 2 - 20,
        tier=4,
        speed=BFB_SPEED,
        balloon_type=BALLOON_TYPE_BFB,
    )
    delayed.append((30.0, [bfb]))
    
    # Create the layered balloon cubes that spawn 90 seconds after MOAB (60s after BFB)
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
    
    # 90 second delay before the balloon cubes spawn (60s after BFB)
    delayed.append((90.0, balloons))
    
    return delayed


def get_total_balloons() -> int:
    # MOAB: 1
    # BFB: 1
    # Ceramic: 8*15 = 120
    # Rainbow: 8*15 = 120
    # Zebra: 8*15 = 120
    # Lead: 8*15 = 120
    # White: 10*15 = 150
    # Black: 10*15 = 150
    # Pink/Yellow/Green/Blue/Red: 5*15*15 = 1125
    # Total: 1907
    return 1907
