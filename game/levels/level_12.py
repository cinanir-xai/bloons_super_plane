"""Level 12 - Final Level with Multiple BFBs and MOABs."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_BFB, BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 12
LEVEL_NAME = "Ultimate Showdown"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Triple BFB formation."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Three BFBs in triangle
    balloons.append(Balloon(x=center_x, y=center_y - 80, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons.append(Balloon(x=center_x - 180, y=center_y + 80, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons.append(Balloon(x=center_x + 180, y=center_y + 80, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOAB ring
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = center_x + math.cos(angle) * 280
        y = center_y + math.sin(angle) * 170
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic outer
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 350
        y = center_y + math.sin(angle) * 200
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room - escalating difficulty."""
    delayed = []
    
    # Wave 2: MOAB swarm (7s)
    balloons2 = []
    # 6 MOABs in two rows
    for i in range(3):
        x = 150 + i * 200
        balloons2.append(Balloon(x=x, y=-100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    for i in range(3):
        x = 150 + i * 200
        balloons2.append(Balloon(x=x, y=-220, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Support wave
    for row in range(5):
        for col in range(12):
            x = 60 + col * 55
            y = -320 - row * 50
            pattern = (row + col) % 6
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: BFB + MOAB combo (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # BFB center
    balloons3.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOABs around
    for i in range(4):
        angle = (i / 4) * 2 * math.pi
        x = center_x + math.cos(angle) * 180
        y = center_y + math.sin(angle) * 110
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # All type outer ring
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        radius = 250
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
    
    # Wave 4: Massive mixed assault (21s)
    balloons4 = []
    # BFBs at corners
    balloons4.append(Balloon(x=150, y=-100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons4.append(Balloon(x=SCREEN_WIDTH - 150, y=-100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # MOAB line
    for i in range(4):
        x = 180 + i * 140
        balloons4.append(Balloon(x=x, y=-200, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive support
    for row in range(8):
        for col in range(14):
            x = 45 + col * 52
            y = -300 - row * 50
            pattern = (row + col) % 8
            if pattern < 6:
                btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                          BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
            else:
                balloons4.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Ultimate finale (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -350
    
    # 4 BFBs in diamond
    balloons5.append(Balloon(x=center_x, y=center_y - 100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons5.append(Balloon(x=center_x, y=center_y + 100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons5.append(Balloon(x=center_x - 200, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    balloons5.append(Balloon(x=center_x + 200, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # 8 MOABs around
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 280
        y = center_y + math.sin(angle) * 170
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive outer wave
    for ring in range(2):
        count = 16 + ring * 8
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = 350 + ring * 50
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.5
            pattern = (ring + i) % 6
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 21 + 72 + 29 + 130 + 68  # 320
