"""Level 6 - Mixed Balloons (50 of each type)."""

from typing import List
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Rainbow Rush"
BALLOON_TIER = 0  # Mixed

def create_balloons() -> List[Balloon]:
    """Create 50 of each balloon type (250 total)."""
    balloons = []
    cols = 10
    rows_per_type = 5  # 5 rows of 10 = 50 per type
    
    # Use red balloon (smallest) as base for consistent spacing
    # All balloons will be almost touching or slightly overlapping
    balloon_radius = get_balloon_radius(4)  # Red balloon (smallest)
    balloon_diameter = balloon_radius * 2
    gap = balloon_diameter * 0.2  # 20% of diameter (80% reduction from original gap)
    spacing_x = balloon_diameter + gap
    
    # Center the grid horizontally
    grid_width = spacing_x * cols - gap
    start_x = (SCREEN_WIDTH - grid_width) / 2 + balloon_radius
    
    spacing_y = 50
    
    # Tiers: red(4), blue(3), green(2), yellow(1), pink(0)
    tiers = [4, 3, 2, 1, 0]
    
    for tier in tiers:
        for row in range(rows_per_type):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = -100 - (row * spacing_y) - (tier * 300)  # Stagger by tier
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED
                )
                balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 250
