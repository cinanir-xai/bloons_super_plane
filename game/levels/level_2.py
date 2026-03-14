"""Level 2 - Blue Balloons (10x10 grid)."""

from typing import List
from game.enemies import Balloon, get_balloon_radius
from game.constants import SCREEN_WIDTH, COLOR_BLUE, BALLOON_SPEED

LEVEL_NUMBER = 2
LEVEL_NAME = "Blue Wave"
BALLOON_TIER = 3  # Blue

def create_balloons() -> List[Balloon]:
    """Create 10x10 grid of blue balloons."""
    balloons = []
    cols = 10
    rows = 10
    # Calculate spacing based on balloon radius with 80% reduced gap (almost touching)
    balloon_radius = get_balloon_radius(BALLOON_TIER)
    balloon_diameter = balloon_radius * 2
    gap = balloon_diameter * 0.2  # 20% of diameter (80% reduction from original gap)
    spacing_x = balloon_diameter + gap
    
    # Center the grid horizontally
    grid_width = spacing_x * cols - gap
    start_x = (SCREEN_WIDTH - grid_width) / 2 + balloon_radius
    
    spacing_y = 50
    
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = -100 - (row * spacing_y)
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=BALLOON_TIER,
                speed=BALLOON_SPEED
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 100
