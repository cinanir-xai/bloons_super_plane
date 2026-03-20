"""Level 2 - Green and Yellow Balloons with Previous Types."""

from typing import List, Tuple
import math
from ..enemies import Balloon
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 2
LEVEL_NAME = "Forest Canopy"
BALLOON_TIER = 2  # Green base

def create_balloons() -> List[Balloon]:
    """Wave 1: Bee shape made of yellow and green balloons."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Bee body (yellow stripes)
    for row in range(8):
        stripe_width = 5 - abs(row - 4) // 2
        for col in range(-stripe_width, stripe_width + 1):
            x = center_x + col * 35
            y = center_y + row * 40
            # Alternating yellow and green stripes
            tier = 1 if row % 2 == 0 else 2
            balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Bee head (yellow)
    for ring in range(2):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 15 + 20
            x = center_x + math.cos(angle) * radius
            y = center_y - 100 + math.sin(angle) * radius * 0.7
            balloons.append(Balloon(x=x, y=y, tier=1, speed=BALLOON_SPEED))  # Yellow
    
    # Left wing (blue - from previous level)
    wing_x = center_x - 120
    wing_y = center_y - 40
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = wing_x + math.cos(angle) * 50
        y = wing_y + math.sin(angle) * 30
        balloons.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = wing_x + math.cos(angle) * 30
        y = wing_y + math.sin(angle) * 18
        balloons.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    # Right wing (blue)
    wing_x = center_x + 120
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x = wing_x + math.cos(angle) * 50
        y = wing_y + math.sin(angle) * 30
        balloons.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = wing_x + math.cos(angle) * 30
        y = wing_y + math.sin(angle) * 18
        balloons.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Green diamond with red/blue border (7s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -180
    
    # Green diamond center
    for i in range(-5, 6):
        width = 5 - abs(i)
        for j in range(-width, width + 1):
            x = center_x + j * 45
            y = center_y + i * 45
            balloons2.append(Balloon(x=x, y=y, tier=2, speed=BALLOON_SPEED))  # Green
    
    # Red and blue border
    for i in range(-6, 7):
        width = 6 - abs(i)
        for j in [-width - 1, width + 1]:
            x = center_x + j * 45
            y = center_y + i * 45
            tier = 4 if (i + j) % 2 == 0 else 3
            balloons2.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Yellow sun with rays (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Sun center (yellow)
    for ring in range(3):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 25 + 25
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.8
            balloons3.append(Balloon(x=x, y=y, tier=1, speed=BALLOON_SPEED))  # Yellow
    
    # Sun rays (alternating colors)
    for ray in range(12):
        angle = ray * (math.pi / 6)
        for dist in range(3):
            x = center_x + math.cos(angle) * (120 + dist * 35)
            y = center_y + math.sin(angle) * (100 + dist * 28)
            # Mix of red, blue, green
            tier = [4, 3, 2][dist % 3]
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Checkerboard of all four colors (21s)
    balloons4 = []
    for row in range(8):
        for col in range(14):
            x = 60 + col * 50
            y = -80 - row * 50
            # Cycle through all four colors
            tier = (row + col) % 4  # 0=pink, 1=yellow, 2=green, 3=blue
            # Map to our available tiers (no pink yet, use red instead)
            tier_map = {0: 4, 1: 1, 2: 2, 3: 3}  # red, yellow, green, blue
            balloons4.append(Balloon(x=x, y=y, tier=tier_map[tier], speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Tree shape (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    
    # Tree trunk (red/brown - using red)
    for row in range(3):
        for col in range(2):
            x = center_x - 25 + col * 50
            y = -60 - row * 40
            balloons5.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Tree foliage (green with yellow highlights)
    # Bottom layer
    for i in range(9):
        x = center_x - 200 + i * 50
        y = -180
        tier = 2 if i % 3 != 0 else 1
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Middle layer
    for i in range(7):
        x = center_x - 150 + i * 50
        y = -240
        tier = 2 if i % 3 != 1 else 1
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Top layer
    for i in range(5):
        x = center_x - 100 + i * 50
        y = -300
        tier = 2 if i % 2 == 0 else 1
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Top point
    balloons5.append(Balloon(x=center_x, y=-360, tier=1, speed=BALLOON_SPEED))  # Yellow
    
    # Blue ornaments
    for i in range(4):
        x = center_x - 100 + i * 67
        y = -210
        balloons5.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 55 + 72 + 66 + 112 + 34  # 339
