"""Level 7 - Lead Balloons with All Previous Types."""

import math
from typing import List, Tuple

from ..constants import BALLOON_SPEED, SCREEN_WIDTH
from ..enemies import (
    Balloon, get_balloon_radius,
    BALLOON_TYPE_LEAD, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW
)

LEVEL_NUMBER = 7
LEVEL_NAME = "Heavy Metal"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Lead balloons in shield formation."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Lead shield outline
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 100
        y = center_y + math.sin(angle) * 80
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Inner lead cross
    for i in range(-3, 4):
        balloons.append(Balloon(x=center_x + i * 35, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        if i != 0:
            balloons.append(Balloon(x=center_x, y=center_y + i * 35, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Colorful balloons around (all previous types)
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        radius = 160
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.8
        tier = i % 5
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Lead wall with mixed support (7s)
    balloons2 = []
    for row in range(4):
        for col in range(12):
            x = 80 + col * 60
            y = -80 - row * 50
            if row == 0 or row == 3:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            else:
                tier = (row + col) % 5
                balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Lead anchors with zebra/rainbow (14s)
    balloons3 = []
    # Lead anchors at corners
    for cx, cy in [(100, -150), (540, -150), (100, -350), (540, -350)]:
        for ring in range(2):
            count = 4 + ring * 4
            for i in range(count):
                angle = (i / count) * 2 * math.pi
                radius = ring * 20 + 20
                x = cx + math.cos(angle) * radius
                y = cy + math.sin(angle) * radius
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Zebra and rainbow connectors
    for i in range(10):
        x = 180 + i * 35
        y = -250
        btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Lead spiral with all types (21s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    for i in range(30):
        angle = i * 0.4
        radius = 30 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        if i % 5 == 0:
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        else:
            tier = i % 5
            balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Lead fortress (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Outer lead wall
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 150
        y = center_y + math.sin(angle) * 120
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Inner mixed types
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 35 + 25
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            pattern = (ring + i) % 8
            if pattern == 0:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 1:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            elif pattern == 2:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            else:
                balloons5.append(Balloon(x=x, y=y, tier=pattern - 4, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 43 + 48 + 66 + 30 + 74  # 261
