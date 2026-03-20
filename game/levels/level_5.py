"""Level 5 - Zebra Balloons with All Previous Types."""

from typing import List, Tuple
import math
from ..enemies import (
    Balloon,
    BALLOON_TYPE_ZEBRA, BALLOON_TYPE_BLACK, BALLOON_TYPE_WHITE
)
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 5
LEVEL_NAME = "Zebra Safari"
BALLOON_TIER = 4  # Base tier

def create_balloons() -> List[Balloon]:
    """Wave 1: Zebra pattern - stripes of zebra and colorful balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Zebra body outline (zebra balloons)
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        x = center_x + math.cos(angle) * 120
        y = center_y + math.sin(angle) * 80
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Horizontal stripes inside (alternating zebra and colorful)
    for row in range(6):
        y = center_y - 60 + row * 25
        stripe_width = 4 - abs(row - 2)
        for col in range(-stripe_width, stripe_width + 1):
            x = center_x + col * 40
            if row % 2 == 0:
                balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            else:
                tier = (row + col) % 5
                balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Zebra head (smaller oval)
    head_x = center_x
    head_y = center_y - 120
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        x = head_x + math.cos(angle) * 35
        y = head_y + math.sin(angle) * 25
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Ears
    balloons.append(Balloon(x=head_x - 25, y=head_y - 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    balloons.append(Balloon(x=head_x + 25, y=head_y - 30, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Legs (black and white)
    for leg_x in [-80, -40, 40, 80]:
        for i in range(3):
            y = center_y + 90 + i * 30
            btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
            balloons.append(Balloon(x=center_x + leg_x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    # Tail
    for i in range(4):
        x = center_x + 130 + i * 15
        y = center_y + 20 - i * 20
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Zebra stripes across screen (7s)
    balloons2 = []
    for stripe in range(8):
        y = -80 - stripe * 60
        # Alternate between zebra and colorful rows
        if stripe % 2 == 0:
            for i in range(14):
                x = 60 + i * 50
                balloons2.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
        else:
            for i in range(14):
                x = 60 + i * 50
                tier = (stripe + i) % 5
                balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Zebra herd (multiple zebra shapes) (14s)
    balloons3 = []
    
    # Create 3 smaller zebra silhouettes
    for zebra_idx, base_x in enumerate([150, 400, 550]):
        base_y = -180 - zebra_idx * 80
        
        # Body
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = base_x + math.cos(angle) * 40
            y = base_y + math.sin(angle) * 25
            balloons3.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
        
        # Legs
        for leg_offset in [-25, 25]:
            for i in range(2):
                y = base_y + 35 + i * 25
                btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
                balloons3.append(Balloon(x=base_x + leg_offset, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
        
        # Head
        balloons3.append(Balloon(x=base_x, y=base_y - 45, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
        balloons3.append(Balloon(x=base_x - 15, y=base_y - 55, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
        balloons3.append(Balloon(x=base_x + 15, y=base_y - 55, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Colorful background balloons
    for i in range(20):
        x = 80 + (i % 10) * 60
        y = -100 - (i // 10) * 200
        tier = i % 5
        balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed immunity challenge (21s)
    balloons4 = []
    for row in range(8):
        for col in range(14):
            x = 50 + col * 50
            y = -60 - row * 50
            
            # Mix all special types and regular
            pattern = (row + col) % 10
            if pattern == 0:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
            elif pattern == 1:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_BLACK))
            elif pattern == 2:
                balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_WHITE))
            else:
                tier = pattern - 3
                if tier < 0:
                    tier = 0
                balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Zebra vortex (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -280
    
    # Spiral of zebra balloons
    for i in range(40):
        angle = i * 0.35
        radius = 30 + i * 7
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=BALLOON_TYPE_ZEBRA))
    
    # Colorful inner spiral (opposite direction)
    for i in range(30):
        angle = -i * 0.4
        radius = 20 + i * 6
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        tier = i % 5
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Outer ring of black and white
    for i in range(30):
        angle = (i / 30) * 2 * math.pi
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.7
        btype = BALLOON_TYPE_BLACK if i % 2 == 0 else BALLOON_TYPE_WHITE
        balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED, balloon_type=btype))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 48 + 112 + 71 + 112 + 100  # 443
