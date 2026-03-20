"""Level 10 - Multiple MOABs with All Previous Types."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 10
LEVEL_NAME = "MOAB Armada"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Triple MOAB formation."""
    balloons = []
    
    # Three MOABs in triangle formation
    positions = [(SCREEN_WIDTH / 2, -150), (200, -280), (SCREEN_WIDTH - 200, -280)]
    for x, y in positions:
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic support
    for i in range(15):
        x = 100 + (i % 5) * 150
        y = -100 - (i // 5) * 80
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead outer
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = SCREEN_WIDTH / 2 + math.cos(angle) * 280
        y = -200 + math.sin(angle) * 150
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: MOAB line with escorts (7s)
    balloons2 = []
    # MOAB line
    for i in range(3):
        x = 150 + i * 200
        balloons2.append(Balloon(x=x, y=-100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Support lines
    for row in range(4):
        for col in range(14):
            x = 50 + col * 50
            y = -180 - row * 50
            pattern = (row + col) % 6
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Diamond of MOABs (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # 4 MOABs in diamond
    balloons3.append(Balloon(x=center_x, y=center_y - 100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x, y=center_y + 100, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x - 150, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x + 150, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Inner ceramic cluster
    for ring in range(2):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 30 + 30
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed heavy assault (21s)
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
            else:
                balloons4.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: MOAB swarm (28s)
    balloons5 = []
    # 5 MOABs in V formation
    for i in range(5):
        x = SCREEN_WIDTH / 2 + (i - 2) * 130
        y = -150 - abs(i - 2) * 80
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive support wave
    for row in range(6):
        for col in range(12):
            x = 60 + col * 55
            y = -280 - row * 50
            pattern = (row + col) % 8
            btypes = [BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, 
                      BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
            if pattern < 6:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
            else:
                balloons5.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 30 + 87 + 16 + 112 + 97  # 342
