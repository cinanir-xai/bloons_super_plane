"""Level 8 - Spiral Pattern Waves.
Balloons spawn in beautiful spiral patterns that rotate and converge,
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

LEVEL_NUMBER = 8
LEVEL_NAME = "Spiral Galaxy"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in spiral patterns."""
    balloons = []
    
    center_x = SCREEN_WIDTH / 2
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    
    # Wave 1: Outward spirals (50 balloons)
    for arm in range(5):
        arm_angle = (arm / 5) * 2 * math.pi
        for i in range(10):
            radius = 30 + i * 25
            angle = arm_angle + i * 0.5
            x = center_x + radius * math.cos(angle)
            y = -150 - (i * 8) - (arm * 20)
            tier = colors[(arm + i) % 5]
            speed_mult = 0.75 + (i % 3) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="spiral",
                pattern_data={
                    'initial_radius': 30 + i * 20,
                    'frequency': 0.04,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 2: Double helix (40 balloons)
    for helix in range(4):
        helix_y = -700 - (helix * 180)
        for i in range(10):
            for strand in range(2):
                angle = (i / 10) * 4 * math.pi + (strand * math.pi)
                radius = 60 + strand * 40
                x = center_x + radius * math.cos(angle)
                y = helix_y - i * 12
                tier = colors[(helix + strand + i) % 5]
                speed_mult = 0.5 if strand == 0 else 1.5
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="spiral",
                    pattern_data={
                        'initial_radius': 40 + strand * 30,
                        'frequency': 0.035,
                        'phase': angle
                    }
                )
                balloons.append(balloon)
    
    # Wave 3: Tightening spirals (60 balloons)
    for wave in range(6):
        wave_y = -1450 - (wave * 140)
        for i in range(10):
            progress = i / 10
            radius = 100 - progress * 70
            angle = (i / 10) * 6 * math.pi + (wave * 0.3)
            x = center_x + radius * math.cos(angle)
            y = wave_y - i * 10
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
                    'initial_radius': 80 - i * 5,
                    'frequency': 0.05,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 4: Spiral rings (50 balloons)
    for ring in range(5):
        ring_y = -2300 - (ring * 160)
        for i in range(10):
            angle = (i / 10) * 2 * math.pi
            radius = 50 + ring * 20
            x = center_x + radius * math.cos(angle)
            y = ring_y
            tier = colors[(ring + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="spiral",
                pattern_data={
                    'initial_radius': 40 + ring * 10,
                    'frequency': 0.03,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    # Wave 5: Final spirals (50 balloons)
    for wave in range(5):
        wave_y = -3150 - (wave * 150)
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
                pattern="spiral",
                pattern_data={
                    'initial_radius': 50,
                    'frequency': 0.04,
                    'phase': angle
                }
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 290
