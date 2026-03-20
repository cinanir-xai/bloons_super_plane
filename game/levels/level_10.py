"""Level 10 - Straight Line Formations.
Balloons spawn in precise straight line formations - vertical, horizontal,
and diagonal lines that shift and change,
with multiple colors and variable speeds.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
from typing import List
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 10
LEVEL_NAME = "Precision Strike"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in straight line formations."""
    balloons = []
    
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    
    # Wave 1: Vertical lines (52 balloons)
    for wave in range(5):
        wave_y = -100 - (wave * 180)
        for i in range(10):
            x = 100 + i * 55
            y = wave_y
            tier = colors[(wave + i) % 5]
            speed_mult = 0.75 + (i % 3) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    # Wave 2: Horizontal lines (52 balloons)
    for wave in range(5):
        wave_y = -1000 - (wave * 180)
        for i in range(10):
            x = 80 + i * 55
            y = wave_y - i * 5
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 1.5])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    # Wave 3: Diagonal lines (52 balloons)
    for wave in range(5):
        wave_y = -1900 - (wave * 180)
        for i in range(10):
            x = 100 + i * 50
            y = wave_y - i * 15
            tier = colors[(wave + i) % 5]
            speed_mult = 0.5 + (i % 4) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    # Wave 4: Cross formation (52 balloons)
    for wave in range(5):
        wave_y = -2800 - (wave * 180)
        center_x = SCREEN_WIDTH / 2
        
        for i in range(10):
            if i < 5:
                x = center_x
                y = wave_y - i * 25
            else:
                x = center_x - 100 + (i - 5) * 50
                y = wave_y - 50
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.75, 1.0, 1.25])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    # Wave 5: Grid formation (52 balloons)
    for wave in range(5):
        wave_y = -3700 - (wave * 160)
        for i in range(10):
            x = 150 + (i % 5) * 100
            y = wave_y - (i // 5) * 40
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 250
