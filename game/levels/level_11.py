"""Level 11 - Box Patterns with Different Speeds.
Balloons spawn in nested box and rectangle formations,
each box moves at different speeds with multiple colors.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
from typing import List
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 11
LEVEL_NAME = "The Box"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in box patterns with different speeds."""
    balloons = []
    
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    center_x = SCREEN_WIDTH / 2
    
    # Wave 1: Box corners (50 balloons)
    for wave in range(5):
        wave_y = -100 - (wave * 180)
        for box in range(5):
            size = 40 + box * 25
            for corner in range(4):
                if corner == 0:
                    x, y = center_x - size, wave_y - size
                elif corner == 1:
                    x, y = center_x + size, wave_y - size
                elif corner == 2:
                    x, y = center_x - size, wave_y + size
                else:
                    x, y = center_x + size, wave_y + size
                
                tier = colors[(wave + box + corner) % 5]
                speed_mult = 0.5 + box * 0.3
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="circular",
                    pattern_data={
                        'radius': 15,
                        'frequency': 0.025,
                        'phase': corner * math.pi / 2
                    }
                )
                balloons.append(balloon)
    
    # Wave 2: Rectangle rings (50 balloons)
    for wave in range(5):
        wave_y = -1000 - (wave * 180)
        for ring in range(5):
            for i in range(2):
                angle = (i / 2) * 2 * math.pi
                x = center_x + (60 + ring * 30) * math.cos(angle)
                y = wave_y + (40 + ring * 20) * math.sin(angle)
                tier = colors[(wave + ring + i) % 5]
                speed_mult = 0.75 + ring * 0.25
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="circular",
                    pattern_data={
                        'radius': 20,
                        'frequency': 0.03,
                        'phase': angle
                    }
                )
                balloons.append(balloon)
    
    # Wave 3: Concentric boxes (50 balloons)
    for wave in range(5):
        wave_y = -1900 - (wave * 180)
        for layer in range(5):
            for i in range(2):
                angle = (i / 2) * 2 * math.pi
                size = 40 + layer * 30
                x = center_x + size * math.cos(angle)
                y = wave_y + size * math.sin(angle) * 0.5
                tier = colors[(wave + layer + i) % 5]
                speed_mult = 0.5 + (layer % 3) * 0.5
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="circular",
                    pattern_data={
                        'radius': 15 + layer * 4,
                        'frequency': 0.035,
                        'phase': angle
                    }
                )
                balloons.append(balloon)
    
    # Wave 4: Stacked boxes (50 balloons)
    for wave in range(5):
        wave_y = -2800 - (wave * 180)
        for i in range(10):
            x = center_x - 100 + (i % 5) * 50
            y = wave_y - (i // 5) * 50
            tier = colors[i % 5]
            speed_mult = random.choice([0.5, 1.0, 1.5, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="vertical"
            )
            balloons.append(balloon)
    
    # Wave 5: Final boxes (50 balloons)
    for wave in range(5):
        wave_y = -3700 - (wave * 160)
        for i in range(10):
            x = 150 + (i % 5) * 100
            y = wave_y - (i // 5) * 40
            tier = colors[i % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="zigzag",
                pattern_data={
                    'amplitude': 25,
                    'frequency': 0.04,
                    'phase': i * 0.2
                }
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 300
