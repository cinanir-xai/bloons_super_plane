"""Level 5 - Pink Balloons (10x10 grid)."""

from typing import List
from game.enemies import Balloon
from game.constants import SCREEN_WIDTH, COLOR_PINK, BALLOON_SPEED

LEVEL_NUMBER = 5
LEVEL_NAME = "Pink Finale"
BALLOON_TIER = 0  # Pink (largest)

def create_balloons() -> List[Balloon]:
    """Create 10x10 grid of pink balloons."""
    balloons = []
    cols = 10
    rows = 10
    spacing_x = SCREEN_WIDTH / (cols + 1)
    spacing_y = 50
    
    for row in range(rows):
        for col in range(cols):
            x = spacing_x * (col + 1)
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
