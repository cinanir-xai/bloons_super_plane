"""Level 4 - Black and White Balloons with All Previous Types."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon,
    BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 4
LEVEL_NAME = "Shadow & Light"
BALLOON_TIER = 4  # Base tier

def create_balloons() -> List[Balloon]:
    """Wave 1: Yin-Yang symbol with black and white balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Outer circle (alternating black and white)
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        x = center_x + math.cos(angle) * 140
        y = center_y + math.sin(angle) * 120
        btype = BALLOON_TYPE_BLACK if i < 12 else BALLOON_TYPE_WHITE
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Black half (left side)
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * math.pi  # Half circle
            radius = ring * 30 + 30
            x = center_x - 40 + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.8
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # White half (right side)
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * math.pi
            radius = ring * 30 + 30
            x = center_x + 40 + math.cos(angle + math.pi) * radius
            y = center_y + math.sin(angle + math.pi) * radius * 0.8
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Small dots (white in black area, black in white area)
    # White dot in black area
    for ring in range(2):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 10 + 15
            x = center_x - 40 + math.cos(angle) * radius
            y = center_y - 40 + math.sin(angle) * radius
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Black dot in white area
    for ring in range(2):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 10 + 15
            x = center_x + 40 + math.cos(angle) * radius
            y = center_y + 40 + math.sin(angle) * radius
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # Colorful border (all previous types)
    for i in range(30):
        angle = (i / 30) * 2 * math.pi
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.8
        tier = i % 5  # Pink, yellow, green, blue, red
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Piano keys pattern (7s)
    balloons2 = []
    center_y = -150
    
    # White keys (longer)
    for i in range(8):
        x = 80 + i * 70
        for j in range(4):
            y = center_y - j * 40
            balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Black keys (shorter, between white keys)
    for i in range(7):
        if i != 2 and i != 6:  # Skip some positions like real piano
            x = 115 + i * 70
            for j in range(2):
                y = center_y - j * 40
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # Colorful accents
    for i in range(8):
        x = 80 + i * 70
        y = center_y + 40
        tier = [0, 1, 2, 3, 4, 0, 1, 2][i]
        balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Black/White spiral with colorful core (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Black spiral arm
    for i in range(25):
        angle = i * 0.4
        radius = 30 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # White spiral arm (opposite)
    for i in range(25):
        angle = i * 0.4 + math.pi
        radius = 30 + i * 8
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Colorful center
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 20 + 15
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            tier = (ring + i) % 5
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed wave with all balloon types (21s)
    balloons4 = []
    for row in range(8):
        for col in range(14):
            x = 50 + col * 50
            y = -60 - row * 50
            
            # Mix all types
            pattern = (row + col) % 8
            if pattern == 0:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 1:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                tier = pattern - 2  # 0-5 for regular tiers
                balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Skull pattern (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # Skull outline (white)
    for i in range(20):
        angle = (i / 20) * 2 * math.pi
        x = center_x + math.cos(angle) * 100
        y = center_y + math.sin(angle) * 80
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Eye sockets (black)
    for eye_x in [-35, 35]:
        for ring in range(2):
            count = 4 + ring * 4
            for i in range(count):
                angle = (i / count) * 2 * math.pi
                radius = ring * 12 + 15
                x = center_x + eye_x + math.cos(angle) * radius
                y = center_y - 15 + math.sin(angle) * radius
                balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # Nose (black)
    for i in range(3):
        x = center_x - 10 + i * 10
        y = center_y + 20
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
    
    # Teeth (white with black gaps)
    for row in range(2):
        for col in range(6):
            x = center_x - 50 + col * 20
            y = center_y + 50 + row * 20
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
    
    # Colorful accents around skull
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        radius = 150
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.9
        tier = i % 5
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 96 + 53 + 81 + 112 + 67  # 409
