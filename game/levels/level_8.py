"""Level 8 - Twin MOABs."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 8
LEVEL_NAME = "Twin Titans"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Ceramic balloons in butterfly shape."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Left wing
    for ring in range(3):
        count = 8 + ring * 4
        for i in range(count):
            angle = (i / count) * math.pi  # Half circle
            radius = ring * 30 + 40
            x = center_x - 80 + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Right wing
    for ring in range(3):
        count = 8 + ring * 4
        for i in range(count):
            angle = (i / count) * math.pi
            radius = ring * 30 + 40
            x = center_x + 80 - math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Body (lead)
    for i in range(5):
        balloons.append(Balloon(x=center_x, y=center_y - 60 + i * 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Antennae (colorful)
    for i in range(4):
        balloons.append(Balloon(x=center_x - 20, y=center_y - 100 - i * 20, tier=i % 5, speed=BALLOON_SPEED))
        balloons.append(Balloon(x=center_x + 20, y=center_y - 100 - i * 20, tier=(i + 2) % 5, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-6 with 2 MOABs in separate waves."""
    delayed = []
    
    # Wave 2: Mixed assault (10s)
    balloons2 = []
    for row in range(5):
        for col in range(10):
            x = 80 + col * 60
            y = -80 - row * 50
            pattern = (row + col) % 8
            if pattern == 0:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            else:
                balloons2.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((10.0, balloons2))
    
    # Wave 3: First MOAB (25s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # MOAB
    balloons3.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic escort
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 90
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead support
    for i in range(6):
        balloons3.append(Balloon(x=center_x - 180 - i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons3.append(Balloon(x=center_x + 180 + i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    delayed.append((25.0, balloons3))
    
    # Wave 4: Heavy mixed wave (40s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Black and white diamond
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 100
        y = center_y + math.sin(angle) * 60
        btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Zebra and rainbow outer
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 180
        y = center_y + math.sin(angle) * 110
        btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Support grid
    for row in range(4):
        for col in range(8):
            x = 120 + col * 70
            y = center_y - 100 - row * 50
            balloons4.append(Balloon(x=x, y=y, tier=(row + col) % 5, speed=BALLOON_SPEED))
    
    delayed.append((40.0, balloons4))
    
    # Wave 5: Lead and ceramic wall (55s)
    balloons5 = []
    for row in range(6):
        for col in range(12):
            x = 60 + col * 55
            y = -80 - row * 50
            if row == 0 or row == 5:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif row == 2 or row == 3:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            else:
                pattern = (row + col) % 4
                btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((55.0, balloons5))
    
    # Wave 6: Second MOAB (70s)
    balloons6 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -350
    
    # MOAB
    balloons6.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Rainbow escort ring
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = center_x + math.cos(angle) * 130
        y = center_y + math.sin(angle) * 80
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Zebra second ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 190
        y = center_y + math.sin(angle) * 120
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Lead outer wings
    for i in range(8):
        balloons6.append(Balloon(x=center_x - 220 - i * 20, y=center_y - 50 + i * 10, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons6.append(Balloon(x=center_x + 220 + i * 20, y=center_y - 50 + i * 10, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Support balloons
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        tier = i % 5
        balloons6.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((70.0, balloons6))
    
    return delayed


def get_total_balloons() -> int:
    return 43 + 50 + 21 + 44 + 72 + 49  # 279
