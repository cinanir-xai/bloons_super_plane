"""Level 6 - Rainbow Balloons with All Previous Types."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon,
    BALLOON_TYPE_RAINBOW, BALLOON_TYPE_ZEBRA, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 6
LEVEL_NAME = "Rainbow Storm"
BALLOON_TIER = 4  # Base tier

def create_balloons() -> List[Balloon]:
    """Wave 1: Rainbow arc with all colors underneath."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -100
    
    # Main rainbow arc (rainbow balloons)
    for i in range(40):
        angle = math.pi * 0.1 + (i / 39) * math.pi * 0.8  # Arc
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Inner rainbow arc
    for i in range(35):
        angle = math.pi * 0.15 + (i / 34) * math.pi * 0.7
        radius = 150
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Clouds at base of rainbow (white balloons)
    # Left cloud
    for i in range(5):
        x = 80 + i * 35
        y = center_y + 80
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    for i in range(4):
        x = 97 + i * 35
        y = center_y + 50
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Right cloud
    for i in range(5):
        x = 470 + i * 35
        y = center_y + 80
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    for i in range(4):
        x = 487 + i * 35
        y = center_y + 50
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Colorful balloons under rainbow (all tiers)
    for i in range(20):
        x = 150 + i * 30
        y = center_y + 130
        tier = i % 5
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Rainbow waterfall (7s)
    balloons2 = []
    for col in range(10):
        x = 80 + col * 65
        # Each column is a different "color" type
        for row in range(8):
            y = -60 - row * 50
            
            # Create rainbow effect across columns
            if col < 2:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif col < 4:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif col < 6:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif col < 8:
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                tier = (col + row) % 5
                balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Rainbow flower (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Rainbow petals
    for petal in range(8):
        angle = petal * (math.pi / 4)
        # Outer edge of petal
        for r in range(4):
            x = center_x + math.cos(angle) * (60 + r * 35)
            y = center_y + math.sin(angle) * (50 + r * 30)
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
        # Petal fill
        for offset in [-20, 0, 20]:
            a = angle + math.radians(offset)
            x = center_x + math.cos(a) * 100
            y = center_y + math.sin(a) * 80
            tier = petal % 5
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Center (zebra)
    for ring in range(2):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 20 + 20
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: All types mixed wave (21s)
    balloons4 = []
    for row in range(8):
        for col in range(14):
            x = 50 + col * 50
            y = -60 - row * 50
            
            # Mix all types evenly
            pattern = (row + col) % 12
            if pattern == 0:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
            elif pattern == 1:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 2:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 3:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                tier = pattern - 4
                balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Rainbow galaxy (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    # Central rainbow cluster
    for ring in range(4):
        count = 8 + ring * 8
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 35 + 25
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_RAINBOW))
    
    # Spiral arms (rainbow + zebra)
    for arm in range(4):
        base_angle = arm * (math.pi / 2)
        for i in range(20):
            angle = base_angle + i * 0.2
            radius = 80 + i * 12
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.6
            btype = BALLOON_TYPE_RAINBOW if i % 2 == 0 else BALLOON_TYPE_ZEBRA
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Outer ring of all colors
    for i in range(40):
        angle = (i / 40) * 2 * math.pi
        radius = 250
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.7
        
        # Cycle through all types
        type_cycle = i % 8
        if type_cycle == 0:
            btype = BALLOON_TYPE_RAINBOW
        elif type_cycle == 1:
            btype = BALLOON_TYPE_ZEBRA
        elif type_cycle == 2:
            btype = BALLOON_TYPE_BLACK
        elif type_cycle == 3:
            btype = BALLOON_TYPE_WHITE
        else:
            tier = type_cycle - 4
            balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
            continue
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 78 + 80 + 88 + 112 + 156  # 514
