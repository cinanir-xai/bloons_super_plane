"""Level 1 - Red Balloons (10x10 grid)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from ..enemies import Balloon
from ..constants import SCREEN_WIDTH, COLOR_RED, BALLOON_SPEED

LEVEL_NUMBER = 1
LEVEL_NAME = "Red Swarm"
BALLOON_TIER = 4  # Red

def create_balloons() -> List[Balloon]:
    """Create 10x10 grid of red balloons."""
    balloons = []
    cols = 10
    rows = 10
    spacing_x = SCREEN_WIDTH / (cols + 1)
    spacing_y = 50  # Vertical spacing between rows
    
    for row in range(rows):
        for col in range(cols):
            x = spacing_x * (col + 1)
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
