"""Level 7 - First MOAB Encounter."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_MOAB, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 7
LEVEL_NAME = "Titan Rising"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Lead balloons in airplane shape."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Airplane fuselage (lead)
    for i in range(8):
        balloons.append(Balloon(x=center_x, y=center_y - 80 + i * 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Wings (lead)
    for i in range(6):
        balloons.append(Balloon(x=center_x - 60 - i * 20, y=center_y + 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons.append(Balloon(x=center_x + 60 + i * 20, y=center_y + 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Tail (lead)
    balloons.append(Balloon(x=center_x - 40, y=center_y + 160, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    balloons.append(Balloon(x=center_x + 40, y=center_y + 160, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Nose (ceramic)
    balloons.append(Balloon(x=center_x, y=center_y - 120, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Colorful contrails
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 120
        tier = i % 5
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-6 with proper spacing."""
    delayed = []
    
    # Wave 2: Ceramic spiral (10s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    for i in range(25):
        angle = i * 0.5
        radius = 30 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    delayed.append((10.0, balloons2))
    
    # Wave 3: Mixed assault grid (20s)
    balloons3 = []
    for row in range(5):
        for col in range(10):
            x = 80 + col * 60
            y = -80 - row * 50
            pattern = (row + col) % 8
            if pattern == 0:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 3:
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons3.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((20.0, balloons3))
    
    # Wave 4: Zebra and rainbow rings (30s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # Inner zebra ring
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = center_x + math.cos(angle) * 80
        y = center_y + math.sin(angle) * 50
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Outer rainbow ring
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 150
        y = center_y + math.sin(angle) * 90
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((30.0, balloons4))
    
    # Wave 5: Lead fortress (40s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Lead wall
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 100
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Inner ceramics
    for ring in range(2):
        count = 6 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 30 + 30
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    delayed.append((40.0, balloons5))
    
    # Wave 6: THE MOAB - First encounter (55s)
    balloons6 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -350
    
    # MOAB in center
    balloons6.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic honor guard
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 150
        y = center_y + math.sin(angle) * 100
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead escort wings
    for i in range(6):
        balloons6.append(Balloon(x=center_x - 200 - i * 25, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons6.append(Balloon(x=center_x + 200 + i * 25, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Support balloons
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 250
        y = center_y + math.sin(angle) * 150
        tier = i % 5
        balloons6.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((55.0, balloons6))
    
    return delayed


def get_total_balloons() -> int:
    return 29 + 25 + 50 + 24 + 28 + 35  # 191
