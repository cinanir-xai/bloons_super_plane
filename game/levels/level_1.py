"""Level 1 - Red and Blue Balloons with Creative Patterns."""

from typing import List, Tuple
import math
from ..enemies import Balloon, get_balloon_radius, BALLOON_TYPE_NORMAL
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 1
LEVEL_NAME = "Red & Blue"
BALLOON_TIER = 4  # Red base tier

def create_balloons() -> List[Balloon]:
    """Create first wave: Red balloons in a circle pattern."""
    balloons = []
    balloon_radius = get_balloon_radius(4)  # Red tier
    
    # Wave 1: Large circle of red balloons
    center_x = SCREEN_WIDTH / 2
    center_y = -150
    radius = 200
    num_balloons = 24
    
    for i in range(num_balloons):
        angle = (i / num_balloons) * 2 * math.pi
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.5  # Slightly flattened
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))
    
    # Inner circle
    inner_radius = 100
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * inner_radius
        y = center_y + math.sin(angle) * inner_radius * 0.5
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with breathing room."""
    delayed = []
    
    # Wave 2: Blue balloons in V formation (7s delay)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    start_y = -100
    
    for i in range(9):
        offset = (i - 4) * 40
        x = center_x + offset
        y = start_y + abs(offset) * 0.5  # V shape
        balloons2.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    for i in range(7):
        offset = (i - 3) * 40
        x = center_x + offset
        y = start_y + abs(offset) * 0.5 + 50
        balloons2.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Red and Blue alternating lines (14s delay)
    balloons3 = []
    for row in range(6):
        for col in range(12):
            x = 80 + col * 45
            y = -100 - row * 50
            tier = 4 if (row + col) % 2 == 0 else 3  # Alternate red/blue
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Final red star pattern (21s delay)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    for arm in range(5):
        angle = arm * (2 * math.pi / 5) - math.pi / 2
        for dist in [0, 60, 120, 180]:
            x = center_x + math.cos(angle) * dist
            y = center_y + math.sin(angle) * dist
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 36 + 16 + 72 + 20  # All waves: 144
