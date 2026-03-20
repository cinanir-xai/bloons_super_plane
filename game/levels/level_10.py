"""Level 10 - BFB Arrival."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_BFB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 10
LEVEL_NAME = "Titan's Breath"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Plane shape made of balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Fuselage (lead)
    for i in range(10):
        balloons.append(Balloon(x=center_x, y=center_y - 100 + i * 25, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Wings (ceramic)
    for i in range(8):
        balloons.append(Balloon(x=center_x - 50 - i * 18, y=center_y + 50, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
        balloons.append(Balloon(x=center_x + 50 + i * 18, y=center_y + 50, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Tail (zebra/rainbow)
    for i in range(4):
        balloons.append(Balloon(x=center_x - 30, y=center_y + 150 + i * 20, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
        balloons.append(Balloon(x=center_x + 30, y=center_y + 150 + i * 20, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Nose (black/white)
    balloons.append(Balloon(x=center_x, y=center_y - 130, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    for i in range(3):
        balloons.append(Balloon(x=center_x - 20 + i * 20, y=center_y - 150, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Contrails (colorful)
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 220
        y = center_y + math.sin(angle) * 140
        balloons.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 building up to the BFB finale."""
    delayed = []
    
    # Wave 2: Ceramic spiral (12s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    for i in range(30):
        angle = i * 0.4
        radius = 30 + i * 7
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead core
    for ring in range(2):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = ring * 25 + 20
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * r
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    delayed.append((12.0, balloons2))
    
    # Wave 3: Mixed grid (25s)
    balloons3 = []
    for row in range(6):
        for col in range(10):
            x = 80 + col * 60
            y = -80 - row * 50
            pattern = (row + col) % 8
            if pattern == 0:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif pattern == 4:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 5:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons3.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((25.0, balloons3))
    
    # Wave 4: Star formation (40s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -320
    
    # 5-pointed star
    for arm in range(5):
        angle = arm * (2 * math.pi / 5) - math.pi / 2
        for dist in range(8):
            x = center_x + math.cos(angle) * (dist * 30 + 30)
            y = center_y + math.sin(angle) * (dist * 30 + 30)
            btype = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                     BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK][arm]
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Inner rings
    for ring in range(3):
        count = 8 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = ring * 30 + 25
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * r
            pattern = (ring + i) % 4
            btypes = [BALLOON_TYPE_WHITE, BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK]
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((40.0, balloons4))
    
    # Wave 5: THE BFB - Final boss (60s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -400
    
    # BFB in center
    balloons5.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # Ceramic honor guard - inner ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 90
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead second ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 130
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Mixed outer ring
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 270
        y = center_y + math.sin(angle) * 170
        pattern = i % 4
        btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    # Support balloons
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 330
        y = center_y + math.sin(angle) * 210
        balloons5.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((60.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 59 + 38 + 60 + 55 + 73  # 285
