"""Level 7 - Circular Pattern Waves.
Balloons spawn in concentric circles that expand and contract,
with multiple colors and variable speeds.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
from typing import List
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED, COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED

LEVEL_NUMBER = 7
LEVEL_NAME = "Circular Symphony"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in circular wave patterns."""
    balloons = []
    
    # Color tiers (all colors for variety)
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    
    # Center of the screen for circles
    center_x = SCREEN_WIDTH / 2
    
    # Wave 1: Circles (40 balloons)
    for wave in range(4):
        wave_y = -200 - (wave * 200)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 60 + (wave % 2) * 40
            x = center_x + radius * math.cos(angle)
            y = wave_y + radius * math.sin(angle) * 0.3
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
                    'radius': 30,
                    'frequency': 0.025,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 2: Double circles (40 balloons)
    for wave in range(4):
        wave_y = -1000 - (wave * 180)
        for layer in range(2):
            for i in range(5):
                angle = (i / 5) * 2 * math.pi + (layer * math.pi / 5)
                radius = 70 + layer * 50
                x = center_x + radius * math.cos(angle)
                y = wave_y + radius * math.sin(angle) * 0.25
                tier = colors[(wave + layer + i) % 5]
                speed_mult = random.choice([0.75, 1.0, 1.25, 2.0])
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="circular",
                    pattern_data={
                        'radius': 35,
                        'frequency': 0.03,
                        'phase': angle
                    }
                )
                balloons.append(balloon)
    
    # Wave 3: Circle rings (40 balloons)
    for wave in range(4):
        wave_y = -1750 - (wave * 160)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 50 + (wave % 3) * 25
            x = center_x + radius * math.cos(angle)
            y = wave_y
            tier = colors[i % 5]
            speed_mult = 0.5 + (i % 4) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="circular",
                pattern_data={
                    'radius': 25,
                    'frequency': 0.035,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 4: Pulsing circles (40 balloons)
    for wave in range(4):
        wave_y = -2400 - (wave * 150)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 80 + (i % 2) * 40
            x = center_x + radius * math.cos(angle)
            y = wave_y + radius * math.sin(angle) * 0.2
            tier = colors[(wave * 2 + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="circular",
                pattern_data={
                    'radius': 20 + (i % 3) * 10,
                    'frequency': 0.04,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 5: Final circles (40 balloons)
    for wave in range(4):
        wave_y = -3050 - (wave * 130)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 60
            x = center_x + radius * math.cos(angle)
            y = wave_y
            tier = colors[i % 5]
            speed_mult = random.choice([0.5, 1.0, 1.5])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="circular",
                pattern_data={
                    'radius': 30,
                    'frequency': 0.03,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 200
