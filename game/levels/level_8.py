"""Level 8 - Ceramic Balloons with All Previous Types."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 8
LEVEL_NAME = "Ceramic Storm"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Ceramic balloons in vase shape."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Ceramic vase outline
    # Neck
    for i in range(6):
        x = center_x - 40 + i * 16
        y = center_y - 100
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Body (wider)
    for row in range(5):
        width = 5 + row
        for col in range(width):
            x = center_x - width * 18 + col * 36
            y = center_y - 40 + row * 35
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Base
    for i in range(8):
        x = center_x - 70 + i * 20
        y = center_y + 140
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Decorative flowers (colorful)
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        radius = 180
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        tier = i % 5
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Ceramic rain (7s)
    balloons2 = []
    for row in range(6):
        for col in range(10):
            x = 80 + col * 60
            y = -60 - row * 50
            if (row + col) % 3 == 0:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            else:
                tier = (row + col) % 5
                balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Ceramic and lead duo (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Left side - ceramics
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * math.pi  # Half circle
            radius = ring * 35 + 30
            x = center_x - 100 + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Right side - lead
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * math.pi
            radius = ring * 35 + 30
            x = center_x + 100 + math.cos(angle + math.pi) * radius
            y = center_y + math.sin(angle + math.pi) * radius * 0.7
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Center connector (rainbow)
    for i in range(8):
        x = center_x - 70 + i * 20
        y = center_y
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed assault (21s)
    balloons4 = []
    for row in range(8):
        for col in range(12):
            x = 60 + col * 55
            y = -60 - row * 50
            
            pattern = (row + col) % 10
            if pattern == 0:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            else:
                balloons4.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Ceramic star (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # 5-pointed star of ceramics
    for arm in range(5):
        angle = arm * (2 * math.pi / 5) - math.pi / 2
        for dist in range(6):
            x = center_x + math.cos(angle) * (dist * 35 + 30)
            y = center_y + math.sin(angle) * (dist * 35 + 30)
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Inner cluster (all types)
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 25 + 20
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            pattern = (ring + i) % 8
            if pattern < 4:
                btype = [BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE, BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW][pattern]
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
            else:
                balloons5.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 55 + 60 + 62 + 96 + 78  # 351
