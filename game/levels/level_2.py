"""Level 2 - Green and Yellow Balloons with Creative Patterns."""

from typing import List, Tuple
import math
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 2
LEVEL_NAME = "Green & Yellow"
BALLOON_TIER = 2  # Green base

def create_balloons() -> List[Balloon]:
    """Wave 1: Yellow balloons in spiral pattern."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Spiral of yellow balloons (tier 1)
    for i in range(40):
        angle = i * 0.4
        radius = 20 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        
        balloons.append(Balloon(x=x, y=y, tier=1, speed=BALLOON_SPEED))  # Yellow
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Green balloons in diamond (7s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -150
    
    for i in range(8):
        # Diamond points
        balloons2.append(Balloon(x=center_x, y=center_y - i*30, tier=2, speed=BALLOON_SPEED))  # Green
        balloons2.append(Balloon(x=center_x, y=center_y + i*30, tier=2, speed=BALLOON_SPEED))
        balloons2.append(Balloon(x=center_x - i*30, y=center_y, tier=2, speed=BALLOON_SPEED))
        balloons2.append(Balloon(x=center_x + i*30, y=center_y, tier=2, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Green/Yellow checkerboard (14s)
    balloons3 = []
    for row in range(8):
        for col in range(10):
            x = 120 + col * 55
            y = -80 - row * 55
            tier = 2 if (row + col) % 2 == 0 else 1  # Alternate green/yellow
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Green starburst with yellow center (21s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Center cluster
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        for dist in [0, 40, 80]:
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist
            tier = 1 if dist == 0 else 2
            balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 40 + 32 + 80 + 24  # 176
