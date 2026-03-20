"""Level 9 - MOAB Introduction with All Previous Types."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 9
LEVEL_NAME = "MOAB Rising"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: First MOAB with escort."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # MOAB in center
    balloons.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic escort ring
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 150
        y = center_y + math.sin(angle) * 100
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead outer ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 220
        y = center_y + math.sin(angle) * 150
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Colorful support
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 280
        y = center_y + math.sin(angle) * 180
        tier = i % 5
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Heavy assault (7s)
    balloons2 = []
    for row in range(5):
        for col in range(10):
            x = 80 + col * 60
            y = -60 - row * 50
            pattern = (row + col) % 8
            if pattern == 0:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            else:
                balloons2.append(Balloon(x=x, y=y, tier=pattern - 2, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Second MOAB with different escort (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # MOAB
    balloons3.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Zebra and rainbow escort
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 90
        btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Black and white outer
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 130
        btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed chaos (21s)
    balloons4 = []
    for row in range(8):
        for col in range(12):
            x = 50 + col * 55
            y = -60 - row * 50
            
            pattern = (row + col) % 12
            if pattern == 0:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif pattern == 4:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 5:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons4.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Final MOAB wave (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Two MOABs side by side
    balloons5.append(Balloon(x=center_x - 120, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons5.append(Balloon(x=center_x + 120, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic cluster between
    for ring in range(2):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 25 + 20
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # All type outer ring
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.7
        pattern = i % 8
        if pattern < 6:
            btypes = [BALLOON_TYPE_LEAD, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
        else:
            balloons5.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 37 + 50 + 23 + 96 + 32  # 238
