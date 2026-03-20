"""Level 6 - Rainbow Balloons (no immunities, colorful)."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_RAINBOW
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Rainbow Storm"
BALLOON_TIER = 4  # Base tier

def create_balloons() -> List[Balloon]:
    """Wave 1: Rainbow balloons in rainbow arc."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    radius = 250
    
    for i in range(35):
        angle = math.pi * 0.2 + (i / 34) * math.pi * 0.6  # Arc
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.5
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with 9s breathing room."""
    delayed = []
    
    # Wave 2: Rainbow vertical stripes (9s)
    balloons2 = []
    for i in range(8):
        x = 120 + i * 70
        for j in range(10):
            y = -60 - j * 55
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((9.0, balloons2))
    
    # Wave 3: Rainbow concentric circles (18s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -220
    
    for ring in range(5):
        count = 12 + ring * 10
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = 50 + ring * 55
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.5
            
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((18.0, balloons3))
    
    # Wave 4: Rainbow star + center burst (27s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Star arms
    for arm in range(6):
        angle = arm * (2 * math.pi / 6) - math.pi / 2
        for dist in range(0, 250, 40):
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist
            
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Center burst
    for i in range(15):
        angle = (i / 15) * 2 * math.pi
        for dist in [0, 35, 70]:
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist
            
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((27.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 35 + 80 + 110 + 96  # 321
