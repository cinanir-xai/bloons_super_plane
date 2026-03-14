"""Level 6 - Mixed Balloons (50 of each type)."""

from typing import List
from ..enemies import Balloon
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Rainbow Rush"
BALLOON_TIER = 0  # Mixed

def create_balloons() -> List[Balloon]:
    """Create 50 of each balloon type (250 total)."""
    balloons = []
    cols = 10
    rows_per_type = 5  # 5 rows of 10 = 50 per type
    spacing_x = SCREEN_WIDTH / (cols + 1)
    spacing_y = 50
    
    # Tiers: red(4), blue(3), green(2), yellow(1), pink(0)
    tiers = [4, 3, 2, 1, 0]
    
    for tier in tiers:
        for row in range(rows_per_type):
            for col in range(cols):
                x = spacing_x * (col + 1)
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
