"""Level 9 - Quad MOAB Challenge."""

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
LEVEL_NAME = "Quad Titan"
BALLOON_TIER = 4

MAX_RADIUS = get_balloon_radius(4)
STEP = MAX_RADIUS * 2 + 12


def create_balloons() -> List[Balloon]:
    """Wave 1: Helix pattern with mixed balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Double helix DNA pattern
    for i in range(40):
        angle = i * 0.3
        # First strand
        x1 = center_x + math.cos(angle) * 100
        y1 = center_y + i * 12
        # Second strand (offset by pi)
        x2 = center_x + math.cos(angle + math.pi) * 100
        y2 = center_y + i * 12
        
        # Alternate balloon types
        if i % 4 == 0:
            btype = BALLOON_TYPE_CERAMIC
        elif i % 4 == 1:
            btype = BALLOON_TYPE_LEAD
        elif i % 4 == 2:
            btype = BALLOON_TYPE_ZEBRA
        else:
            btype = BALLOON_TYPE_RAINBOW
        
        balloons.append(Balloon(x=x1, y=y1, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
        balloons.append(Balloon(x=x2, y=y2, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
        
        # Connectors between strands every few positions
        if i % 5 == 0:
            for cx in range(int(x1), int(x2), 25):
                balloons.append(Balloon(x=cx, y=(y1 + y2) / 2, tier=i % 5, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-6 with 4 MOABs total, max 2 per wave."""
    delayed = []
    
    # Wave 2: First MOAB (12s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # MOAB in center
    balloons2.append(Balloon(x=center_x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic spiral around MOAB
    for i in range(12):
        angle = i * 0.5
        radius = 80 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead support wings
    for i in range(6):
        balloons2.append(Balloon(x=center_x - 160 - i * 25, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
        balloons2.append(Balloon(x=center_x + 160 + i * 25, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    delayed.append((12.0, balloons2))
    
    # Wave 3: Mixed diamond formation (25s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Diamond of zebra/rainbow
    diamond_points = [(0, -80), (100, 0), (0, 80), (-100, 0)]
    for dx, dy in diamond_points:
        for ring in range(3):
            count = 4 + ring * 4
            for i in range(count):
                angle = (i / count) * 2 * math.pi
                r = ring * 20 + 15
                x = center_x + dx + math.cos(angle) * r
                y = center_y + dy + math.sin(angle) * r * 0.7
                btype = BALLOON_TYPE_ZEBRA if (dx + dy) % 2 == 0 else BALLOON_TYPE_RAINBOW
                balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Black/white inner cluster
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = center_x + math.cos(angle) * 50
        y = center_y + math.sin(angle) * 35
        btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Colorful outer ring
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 200
        y = center_y + math.sin(angle) * 130
        balloons3.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((25.0, balloons3))
    
    # Wave 4: Twin MOABs (40s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -320
    
    # Two MOABs side by side
    balloons4.append(Balloon(x=center_x - 140, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons4.append(Balloon(x=center_x + 140, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Ceramic bridge between MOABs
    for i in range(8):
        x = center_x - 100 + i * 30
        balloons4.append(Balloon(x=x, y=center_y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead honor guard around each MOAB
    for moab_x in [center_x - 140, center_x + 140]:
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            x = moab_x + math.cos(angle) * 100
            y = center_y + math.sin(angle) * 60
            balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Rainbow outer rings
    for i in range(14):
        angle = (i / 14) * 2 * math.pi
        x = center_x + math.cos(angle) * 250
        y = center_y + math.sin(angle) * 150
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    delayed.append((40.0, balloons4))
    
    # Wave 5: Heavy mixed assault (55s)
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
    
    delayed.append((55.0, balloons5))
    
    # Wave 6: Final twin MOAB wave (70s)
    balloons6 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -380
    
    # Two MOABs in V formation
    balloons6.append(Balloon(x=center_x - 100, y=center_y - 40, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    balloons6.append(Balloon(x=center_x + 100, y=center_y - 40, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_MOAB))
    
    # Massive ceramic escort
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 180
        y = center_y + math.sin(angle) * 110
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_CERAMIC))
    
    # Lead second ring
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        x = center_x + math.cos(angle) * 130
        y = center_y + math.sin(angle) * 80
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_LEAD))
    
    # Mixed outer ring
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 260
        y = center_y + math.sin(angle) * 160
        pattern = i % 4
        btypes = [BALLOON_TYPE_ZEBRA, BALLOON_TYPE_RAINBOW, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE]
        balloons6.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btypes[pattern]))
    
    # Support balloons
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 320
        y = center_y + math.sin(angle) * 200
        balloons6.append(Balloon(x=x, y=y, tier=i % 5, speed=BALLOON_SPEED))
    
    delayed.append((70.0, balloons6))
    
    return delayed


def get_total_balloons() -> int:
    return 80 + 36 + 66 + 40 + 60 + 76  # 358
