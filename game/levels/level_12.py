"""Level 12 - Ultimate Showdown."""

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
    """Wave 1: MOAB shape drawn with blue balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Draw a MOAB outline using blue balloons (tier 3)
    # Main body (oval)
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 100
        y = center_y + math.sin(angle) * 60
        balloons.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))
    
    # Fins (triangular)
    fin_points = [
        (center_x - 80, center_y + 40),
        (center_x - 120, center_y + 100),
        (center_x - 40, center_y + 60),
    ]
    for px, py in fin_points:
        balloons.append(Balloon(x=px, y=py, tier=3, speed=BALLOON_SPEED))
    
    fin_points2 = [
        (center_x + 80, center_y + 40),
        (center_x + 120, center_y + 100),
        (center_x + 40, center_y + 60),
    ]
    for px, py in fin_points2:
        balloons.append(Balloon(x=px, y=py, tier=3, speed=BALLOON_SPEED))
    
    # "MOAB" text area filled with ceramics
    for ring in range(2):
        count = 6 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = ring * 20 + 20
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * r * 0.6
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Surrounding mixed balloons
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 180
        y = center_y + math.sin(angle) * 120
        pattern = i % 4
        btypes = [BALLOON_TYPE_LEAD, BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_CERAMIC]
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-8 with 2 BFBs + 6 MOABs, last wave = 1 BFB + 2 MOABs."""
    delayed = []
    
    # Wave 2: First MOAB (12s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    balloons2.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic escort
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = center_x + math.cos(angle) * 110
        y = center_y + math.sin(angle) * 70
        balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead wings
    for i in range(5):
        balloons2.append(Balloon(x=center_x - 140 - i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons2.append(Balloon(x=center_x + 140 + i * 20, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    delayed.append((12.0, balloons2))
    
    # Wave 3: Twin MOABs (28s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    balloons3.append(Balloon(x=center_x - 130, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons3.append(Balloon(x=center_x + 130, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Mixed escort
    for moab_x in [center_x - 130, center_x + 130]:
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            x = moab_x + math.cos(angle) * 85
            y = center_y + math.sin(angle) * 50
            btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Outer ring
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 220
        y = center_y + math.sin(angle) * 135
        pattern = i % 4
        btypes = [BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE, BALLOON_TYPE_CERAMIC, BALLOON_TYPE_LEAD]
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((28.0, balloons3))
    
    # Wave 4: First BFB (45s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -320
    
    balloons4.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # Heavy ceramic escort
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 130
        y = center_y + math.sin(angle) * 80
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 190
        y = center_y + math.sin(angle) * 115
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Mixed outer
    for i in range(18):
        angle = (i / 18) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        pattern = i % 4
        btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((45.0, balloons4))
    
    # Wave 5: Twin MOABs again (60s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -340
    
    balloons5.append(Balloon(x=center_x - 120, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons5.append(Balloon(x=center_x + 120, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Heavy escort
    for moab_x in [center_x - 120, center_x + 120]:
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = moab_x + math.cos(angle) * 90
            y = center_y + math.sin(angle) * 55
            btype = BALLOON_TYPE_CERAMIC if i % 2 == 0 else BALLOON_TYPE_LEAD
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Outer ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 230
        y = center_y + math.sin(angle) * 140
        balloons5.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((60.0, balloons5))
    
    # Wave 6: Heavy mixed assault (75s)
    balloons6 = []
    for row in range(6):
        for col in range(10):
            x = 80 + col * 60
            y = -80 - row * 55
            pattern = (row + col) % 8
            if pattern == 0:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
            elif pattern == 1:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
            elif pattern == 2:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 3:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif pattern == 4:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 5:
                balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                balloons6.append(Balloon(x=x, y=y, tier=pattern - 6, speed=BALLOON_SPEED))
    
    delayed.append((75.0, balloons6))
    
    # Wave 7: Second BFB (90s)
    balloons7 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -380
    
    balloons7.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # Ceramic rings
    for ring in range(2):
        count = 12 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = 120 + ring * 60
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * (r * 0.6)
            balloons7.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead ring
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        balloons7.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Mixed outer
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 320
        y = center_y + math.sin(angle) * 200
        pattern = i % 4
        btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
        balloons7.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    delayed.append((90.0, balloons7))
    
    # Wave 8: ULTIMATE FINALE - 1 BFB + 2 MOABs (110s)
    balloons8 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -450
    
    # BFB in center
    balloons8.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BFB))
    
    # Two MOABs flanking
    balloons8.append(Balloon(x=center_x - 160, y=center_y - 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons8.append(Balloon(x=center_x + 160, y=center_y - 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive ceramic swarm around BFB
    for ring in range(3):
        count = 16 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = 100 + ring * 50
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * (r * 0.6)
            balloons8.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead escort around each MOAB
    for moab_x in [center_x - 160, center_x + 160]:
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = moab_x + math.cos(angle) * 90
            y = center_y - 30 + math.sin(angle) * 55
            balloons8.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Zebra/Rainbow outer ring
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 300
        y = center_y + math.sin(angle) * 185
        btype = BALLOON_TYPE_ZEBRA if i % 2 == 0 else BALLOON_TYPE_RAINBOW
        balloons8.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Black/White second outer ring
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 360
        y = center_y + math.sin(angle) * 220
        btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
        balloons8.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Colorful support balloons
    for i in range(30):
        angle = (i / 30) * 2 * math.pi
        x = center_x + math.cos(angle) * 420
        y = center_y + math.sin(angle) * 260
        balloons8.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((110.0, balloons8))
    
    return delayed


def get_total_balloons() -> int:
    return 46 + 23 + 32 + 45 + 32 + 60 + 58 + 107  # 403
