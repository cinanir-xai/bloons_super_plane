"""Level 4 - Black and White Balloons (BTD special types)."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 4
LEVEL_NAME = "Black & White"
BALLOON_TIER = 4  # Base tier (not used for special types)

def create_balloons() -> List[Balloon]:
    """Wave 1: Black balloons in square formation."""
    balloons = []
    
    # Black balloons in square outline (explosive immune)
    center_x = SCREEN_WIDTH / 2
    center_y = -150
    size = 200
    
    for i in range(12):
        x = center_x - size/2 + (i/11) * size
        y = center_y - size/2
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
        
        y = center_y + size/2
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    for i in range(10):
        x = center_x - size/2
        y = center_y - size/2 + 20 + (i/9) * (size-40)
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
        
        x = center_x + size/2
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with 8s breathing room."""
    delayed = []
    
    # Wave 2: White balloons in cross (8s) - ice immune
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -150
    
    for i in range(-6, 7):
        balloons2.append(Balloon(x=center_x + i*35, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
        balloons2.append(Balloon(x=center_x, y=center_y + i*35, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    delayed.append((8.0, balloons2))
    
    # Wave 3: Black/White checkerboard (16s)
    balloons3 = []
    for row in range(6):
        for col in range(8):
            x = 150 + col * 60
            y = -80 - row * 60
            btype = BALLOON_TYPE_BLACK if (row + col) % 2 == 0 else BALLOON_TYPE_WHITE
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    delayed.append((16.0, balloons3))
    
    # Wave 4: Black circles, White center (24s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Outer black ring
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 150
        y = center_y + math.sin(angle) * 80
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # Inner white cluster
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 30
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.5
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    delayed.append((24.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 44 + 26 + 48 + 38  # 156
