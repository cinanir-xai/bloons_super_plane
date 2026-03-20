"""Level 5 - Zebra Balloons (explosive + ice immune)."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_ZEBRA
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 5
LEVEL_NAME = "Zebra Zone"
BALLOON_TIER = 4  # Base tier

def create_balloons() -> List[Balloon]:
    """Wave 1: Zebra balloons in wave pattern."""
    balloons = []
    
    # Zebra balloons in sinusoidal wave
    center_y = -150
    for i in range(30):
        x = 80 + i * 35
        y = center_y + math.sin(i * 0.3) * 60
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Second wave row
    center_y = -280
    for i in range(25):
        x = 120 + i * 35
        y = center_y + math.cos(i * 0.35) * 50
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with 9s breathing room."""
    delayed = []
    
    # Wave 2: Zebra grid (9s)
    balloons2 = []
    for row in range(6):
        for col in range(10):
            x = 100 + col * 60
            y = -80 - row * 60
            
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    delayed.append((9.0, balloons2))
    
    # Wave 3: Zebra circles (18s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    for ring in range(4):
        count = 10 + ring * 8
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = 60 + ring * 55
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.5
            
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    delayed.append((18.0, balloons3))
    
    # Wave 4: Zebra starburst (27s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    for arm in range(8):
        angle = arm * (2 * math.pi / 8)
        for dist in [0, 70, 140, 210]:
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist
            
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    delayed.append((27.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 55 + 60 + 72 + 32  # 219
