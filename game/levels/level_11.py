"""Level 11 - Titan's Wrath."""

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
LEVEL_NAME = "Titan's Wrath"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Heart shape with mixed balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Heart outline using parametric equations
    for i in range(40):
        t = (i / 40) * 2 * math.pi
        # Heart parametric equations
        x = center_x + 16 * math.sin(t) ** 3
        y = center_y - (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        # Scale up
        x = center_x + (x - center_x) * 8
        y = center_y + (y - center_y) * 5
        
        if i % 4 == 0:
            btype = BALLOON_TYPE_CERAMIC
        elif i % 4 == 1:
            btype = BALLOON_TYPE_LEAD
        elif i % 4 == 2:
            btype = BALLOON_TYPE_ZEBRA
        else:
            btype = BALLOON_TYPE_RAINBOW
        
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Fill the heart with colorful balloons
    for ring in range(3):
        count = 6 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = ring * 25 + 20
            x = center_x + math.cos(angle) * r * 0.8
            y = center_y + math.sin(angle) * r
            balloons.append(Balloon(x=x, y=y, tier=ring % 5, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-6 with 4 MOABs in earlier waves, BFB with ceramics at end."""
    delayed = []
    
    # Wave 2: First MOAB (12s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # MOAB
    balloons2.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic escort
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = center_x + math.cos(angle) * 120
        y = center_y + math.sin(angle) * 75
        balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead wings
    for i in range(5):
        balloons2.append(Balloon(x=center_x - 150 - i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons2.append(Balloon(x=center_x + 150 + i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    delayed.append((12.0, balloons2))
    
    # Wave 3: Twin MOABs (28s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Two MOABs
    balloons3.append(Balloon(x=center_x - 130, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x + 130, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Zebra/rainbow escort
    for moab_x in [center_x - 130, center_x + 130]:
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            x = moab_x + math.cos(angle) * 90
            y = center_y + math.sin(angle) * 55
            btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Mixed outer ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 230
        y = center_y + math.sin(angle) * 140
        pattern = i % 4
        btypes = [BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD]
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((28.0, balloons3))
    
    # Wave 4: Fourth MOAB with heavy escort (44s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -320
    
    # MOAB
    balloons4.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Heavy ceramic ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 130
        y = center_y + math.sin(angle) * 80
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead second ring
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 190
        y = center_y + math.sin(angle) * 115
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Mixed outer
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        pattern = i % 4
        btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((44.0, balloons4))
    
    # Wave 5: Heavy mixed assault (58s)
    balloons5 = []
    for row in range(6):
        for col in range(10):
            x = 80 + col * 60
            y = -80 - row * 55
            pattern = (row + col) % 8
            if pattern == 0:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif pattern == 4:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 5:
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons5.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((58.0, balloons5))
    
    # Wave 6: BFB with massive ceramic swarm (75s)
    balloons6 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -400
    
    # BFB in center
    balloons6.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # Massive ceramic swarm - inner ring
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 90
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Ceramic second ring
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 125
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Ceramic third ring
    for i in range(28):
        angle = (i / 28) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead outer ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 320
        y = center_y + math.sin(angle) * 200
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Support balloons
    for i in range(30):
        angle = (i / 30) * 2 * math.pi
        x = center_x + math.cos(angle) * 380
        y = center_y + math.sin(angle) * 240
        balloons6.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((75.0, balloons6))
    
    return delayed


def get_total_balloons() -> int:
    return 52 + 25 + 34 + 51 + 60 + 118  # 340
