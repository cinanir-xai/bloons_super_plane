"""Level 3 - Pink Balloons with All Previous Types."""

from typing import List, Tuple
import math
from ..enemies import Balloon
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 3
LEVEL_NAME = "Pink Paradise"
BALLOON_TIER = 0  # Pink (largest)

def create_balloons() -> List[Balloon]:
    """Wave 1: Pink heart shape with colorful border."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Heart shape using parametric equations (pink)
    t_vals = [i / 60 * 2 * math.pi for i in range(60)]
    for t in t_vals:
        x = center_x + 16 * (math.sin(t)**3) * 10
        y = center_y - (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) * 7
        balloons.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    # Fill the heart with pink balloons
    for ring in range(4):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 25 + 20
            x = center_x + math.cos(angle) * radius * 0.8
            y = center_y + math.sin(angle) * radius * 0.6 - 10
            balloons.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    # Colorful border around heart (red, blue, green, yellow)
    for i in range(24):
        angle = (i / 24) * 2 * math.pi
        radius = 180
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.7
        tier = [4, 3, 2, 1][i % 4]  # Cycle through red, blue, green, yellow
        balloons.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-5 with 7s breathing room."""
    delayed = []
    
    # Wave 2: Pink flowers with colorful centers (7s)
    balloons2 = []
    
    # Flower 1
    cx1, cy1 = 150, -150
    # Pink petals
    for petal in range(6):
        angle = petal * (math.pi / 3)
        for r in range(3):
            x = cx1 + math.cos(angle) * (40 + r * 20)
            y = cy1 + math.sin(angle) * (35 + r * 18)
            balloons2.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    # Yellow center
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = cx1 + math.cos(angle) * 15
        y = cy1 + math.sin(angle) * 12
        balloons2.append(Balloon(x=x, y=y, tier=1, speed=BALLOON_SPEED))  # Yellow
    
    # Flower 2
    cx2, cy2 = 450, -180
    for petal in range(6):
        angle = petal * (math.pi / 3)
        for r in range(3):
            x = cx2 + math.cos(angle) * (40 + r * 20)
            y = cy2 + math.sin(angle) * (35 + r * 18)
            balloons2.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    # Green center
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = cx2 + math.cos(angle) * 15
        y = cy2 + math.sin(angle) * 12
        balloons2.append(Balloon(x=x, y=y, tier=2, speed=BALLOON_SPEED))  # Green
    
    # Flower 3
    cx3, cy3 = 300, -280
    for petal in range(6):
        angle = petal * (math.pi / 3)
        for r in range(3):
            x = cx3 + math.cos(angle) * (40 + r * 20)
            y = cy3 + math.sin(angle) * (35 + r * 18)
            balloons2.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    # Blue center
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = cx3 + math.cos(angle) * 15
        y = cy3 + math.sin(angle) * 12
        balloons2.append(Balloon(x=x, y=y, tier=3, speed=BALLOON_SPEED))  # Blue
    
    delayed.append((7.0, balloons2))
    
    # Wave 3: Pink butterfly shape (14s)
    balloons3 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    
    # Left wing (pink with blue edges)
    for ring in range(4):
        count = 8 + ring * 4
        for i in range(count):
            angle = (i / count) * math.pi  # Half circle
            radius = ring * 30 + 30
            x = center_x - 80 - math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            tier = 0 if ring < 3 else 3  # Pink inside, blue edge
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Right wing
    for ring in range(4):
        count = 8 + ring * 4
        for i in range(count):
            angle = (i / count) * math.pi
            radius = ring * 30 + 30
            x = center_x + 80 + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            tier = 0 if ring < 3 else 3
            balloons3.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Body (green and yellow)
    for i in range(5):
        y = center_y - 60 + i * 30
        tier = 2 if i % 2 == 0 else 1
        balloons3.append(Balloon(x=center_x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Antennae (red)
    for side in [-1, 1]:
        balloons3.append(Balloon(x=center_x + side * 20, y=center_y - 80, tier=4, speed=BALLOON_SPEED))
        balloons3.append(Balloon(x=center_x + side * 30, y=center_y - 100, tier=4, speed=BALLOON_SPEED))
    
    delayed.append((14.0, balloons3))
    
    # Wave 4: Mixed balloon rain (21s)
    balloons4 = []
    for row in range(10):
        for col in range(12):
            x = 70 + col * 55
            y = -60 - row * 50
            # Weighted towards pink but includes all types
            weights = [0, 0, 0, 0, 1, 1, 2, 2, 3, 4]  # Pink appears more
            import random
            tier = weights[(row + col * 7) % len(weights)]
            balloons4.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((21.0, balloons4))
    
    # Wave 5: Pink star with all colors (28s)
    balloons5 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -250
    
    # 5-pointed star outline (pink)
    for arm in range(5):
        angle = arm * (2 * math.pi / 5) - math.pi / 2
        # Outer points
        for dist in range(8):
            x = center_x + math.cos(angle) * (dist * 25 + 20)
            y = center_y + math.sin(angle) * (dist * 25 + 20)
            balloons5.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    # Fill star with all colors
    for ring in range(5):
        count = 5 + ring * 5
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 25 + 30
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            tier = ring % 5  # Cycle through all tiers
            balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    # Outer ring of all colors
    for i in range(30):
        angle = (i / 30) * 2 * math.pi
        radius = 180
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.8
        tier = i % 5
        balloons5.append(Balloon(x=x, y=y, tier=tier, speed=BALLOON_SPEED))
    
    delayed.append((28.0, balloons5))
    
    return delayed


def get_total_balloons() -> int:
    return 108 + 90 + 86 + 120 + 80  # 484
