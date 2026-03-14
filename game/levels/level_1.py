"""Level 1 - Red Balloons (10x10 grid)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, COLOR_RED, BALLOON_SPEED

LEVEL_NUMBER = 1
LEVEL_NAME = "Red Swarm"
BALLOON_TIER = 4  # Red

def create_balloons() -> List[Balloon]:
    """Create 10x10 grid of red balloons."""
    balloons = []
    cols = 10
    rows = 10
    # Calculate spacing based on balloon radius with 80% reduced gap (almost touching)
    balloon_radius = get_balloon_radius(BALLOON_TIER)
    balloon_diameter = balloon_radius * 2
    gap = balloon_diameter * 0.2  # 20% of diameter (80% reduction from original gap)
    spacing_x = balloon_diameter + gap
    
    # Center the grid horizontally
    grid_width = spacing_x * cols - gap  # Total width of all balloons and gaps
    start_x = (SCREEN_WIDTH - grid_width) / 2 + balloon_radius
    
    spacing_y = 50  # Vertical spacing between rows
    
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = -100 - (row * spacing_y)  # Start above screen, staggered
            
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
