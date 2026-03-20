"""Level 11 - BFB Introduction with All Previous Types."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_BFB, BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 11
LEVEL_NAME = "BFB Arrival"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: First BFB with MOAB escort."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # BFB in center
    balloons.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOAB escort (4 around BFB)
    for i in range(4):
        angle = (i / 4) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 120
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 280
        y = center_y + math.sin(angle) * 170
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead outer
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 350
        y = center_y + math.sin(angle) * 200
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Heavy assault (7s)
    balloons2 = []
    # MOABs
    for i in range(3):
        x = 150 + i * 200
        balloons2.append(Balloon(x=x, y=-100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Support
    for row in range(4):
        for col in range(12):
            x = 60 + col * 55
            y = -180 - row * 50
            pattern = (row + col) % 6
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: BFB and MOAB combo (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # BFB
    balloons3.append(Balloon(x=center_x, y=center_y - 50, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOABs flanking
    balloons3.append(Balloon(x=center_x - 180, y=center_y + 50, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x + 180, y=center_y + 50, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # All type support
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        pattern = i % 8
        if pattern < 6:
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
        else:
            balloons3.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Massive mixed wave (21s)
    balloons4 = []
    for row in range(8):
        for col in range(14):
            x = 45 + col * 52
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
            elif pattern == 4:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 5:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons4.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Double BFB finale (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Two BFBs
    balloons5.append(Balloon(x=center_x - 150, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons5.append(Balloon(x=center_x + 150, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOAB support
    for i in range(4):
        x = 120 + i * 160
        balloons5.append(Balloon(x=x, y=center_y - 120, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive support wave
    for row in range(5):
        for col in range(12):
            x = 60 + col * 55
            y = center_y + 80 - row * 50
            pattern = (row + col) % 6
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 33 + 51 + 23 + 112 + 66  # 285
