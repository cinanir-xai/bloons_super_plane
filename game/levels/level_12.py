"""Level 12 - Complex Mixed Pattern Finale.
The ultimate challenge combining all patterns: circles, spirals, zigzags,
straight lines, and boxes all together in an epic finale,
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

LEVEL_NUMBER = 12
LEVEL_NAME = "Grand Finale"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in complex mixed patterns - the grand finale!"""
    balloons = []
    
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    center_x = SCREEN_WIDTH / 2
    
    # Phase 1: Circular opening (80 balloons)
    for wave in range(8):
        wave_y = -100 - (wave * 100)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 60 + (wave % 3) * 30
            x = center_x + radius * math.cos(angle)
            y = wave_y
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 1.5])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="circular",
                pattern_data={
                    'radius': 25,
                    'frequency': 0.03,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Phase 2: Spiral (80 balloons)
    for wave in range(8):
        wave_y = -900 - (wave * 100)
        for i in range(10):
            angle = (i / 10) * 3 * math.pi + (wave * 0.2)
            radius = 80 - i * 5
            x = center_x + radius * math.cos(angle)
            y = wave_y - i * 6
            tier = colors[(wave + i) % 5]
            speed_mult = 0.5 + (i % 4) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="spiral",
                pattern_data={
                    'initial_radius': 70,
                    'frequency': 0.04,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Phase 3: Zigzag (80 balloons)
    for wave in range(8):
        wave_y = -1700 - (wave * 100)
        for i in range(10):
            offset = 60 if i % 2 == 0 else -60
            x = center_x + offset
            y = wave_y - i * 8
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="zigzag",
                pattern_data={
                    'amplitude': 50,
                    'frequency': 0.04,
                    'phase': i * 0.3
                }
            )
            balloons.append(balloon)
    
    # Phase 4: Lines (80 balloons)
    for wave in range(8):
        wave_y = -2500 - (wave * 100)
        for i in range(10):
            x = 100 + i * 55
            y = wave_y
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
    
    # Phase 5: Boxes (80 balloons)
    for wave in range(8):
        wave_y = -3300 - (wave * 100)
        for i in range(10):
            box = i % 4
            size = 40 + box * 25
            if i < 4:
                x, y = center_x - size, wave_y - size
            elif i < 8:
                x, y = center_x + size, wave_y - size
            elif i < 12:
                x, y = center_x - size, wave_y + size
            else:
                x, y = center_x + size, wave_y + size
            
            tier = colors[i % 5]
            speed_mult = 0.5 + box * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="circular",
                pattern_data={
                    'radius': 20,
                    'frequency': 0.035,
                    'phase': (i % 4) * math.pi / 2
                }
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 400
