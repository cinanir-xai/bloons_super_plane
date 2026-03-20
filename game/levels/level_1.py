"""Level 1 - Introduction to Red and Blue Balloons."""

from typing import List, Tuple
import math
from ..enemies import Balloon
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 1
LEVEL_NAME = "First Flight"
BALLOON_TIER = 4  # Red base

def create_balloons() -> List[Balloon]:
    """Wave 1: Red balloons in a smiley face pattern."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Face outline (circle)
    for i in range(28):
        angle = (i / 28) * 2 * math.pi
        x = center_x + math.cos(angle) * 130
        y = center_y + math.sin(angle) * 110
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Left eye (filled circle)
    for ring in range(3):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 12 + 8
            x = center_x - 50 + math.cos(angle) * radius
            y = center_y - 25 + math.sin(angle) * radius
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Right eye (filled circle)
    for ring in range(3):
        count = 4 + ring * 4
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 12 + 8
            x = center_x + 50 + math.cos(angle) * radius
            y = center_y - 25 + math.sin(angle) * radius
            balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Smile (arc) - wider and happier
    for i in range(16):
        angle = math.pi * 0.15 + (i / 15) * math.pi * 0.7
        x = center_x + math.cos(angle) * 80
        y = center_y + 35 + math.sin(angle) * 45
        balloons.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room between waves."""
    delayed = []
    
    # Wave 2: Blue balloons in V formation (7s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    for row in range(6):
        for i in range(row + 1):
            x = center_x - row * 35 + i * 70
            y = -70 - row * 50
            balloons2.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    delayed.append((7.0, balloons2))
    
    # Wave 3: Red and Blue alternating diamond (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -180
    for i in range(-6, 7):
        width = 6 - abs(i)
        for j in range(-width, width + 1):
            x = center_x + j * 50
            y = center_y + i * 45
            tier = 4 if (i + j) % 2 == 0 else 3  # Alternate red/blue
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    delayed.append((14.0, balloons3))
    
    # Wave 4: Cloud shapes with mixed red/blue (21s)
    balloons4 = []
    # Cloud 1 - left
    cloud1_x, cloud1_y = 150, -120
    for i in range(6):
        x = cloud1_x + i * 45
        y = cloud1_y
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    for i in range(5):
        x = cloud1_x + 22 + i * 45
        y = cloud1_y - 40
        balloons4.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    for i in range(3):
        x = cloud1_x + 67 + i * 45
        y = cloud1_y - 80
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Cloud 2 - right
    cloud2_x, cloud2_y = 450, -100
    for i in range(7):
        x = cloud2_x + i * 45
        y = cloud2_y
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    for i in range(5):
        x = cloud2_x + 45 + i * 45
        y = cloud2_y - 40
        balloons4.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    for i in range(4):
        x = cloud2_x + 67 + i * 45
        y = cloud2_y - 80
        balloons4.append(Balloon(x=x, y=y, tier=4, speed=BALLOON_SPEED))  # Red
    
    # Cloud 3 - center top
    cloud3_x, cloud3_y = 280, -280
    for i in range(8):
        x = cloud3_x + i * 45
        y = cloud3_y
        tier = 4 if i % 2 == 0 else 3
        balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    for i in range(6):
        x = cloud3_x + 45 + i * 45
        y = cloud3_y - 40
        tier = 3 if i % 2 == 0 else 4
        balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Final spiral with red and blue (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    for i in range(50):
        angle = i * 0.35
        radius = 30 + i * 7
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        tier = 4 if i % 2 == 0 else 3  # Alternate colors
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 66 + 21 + 49 + 40 + 50  # 226
