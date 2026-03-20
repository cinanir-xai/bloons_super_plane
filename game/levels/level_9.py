"""Level 9 - Zigzag Pattern Waves.
Balloons spawn in zigzag and wave patterns that flow across the screen,
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

LEVEL_NUMBER = 9
LEVEL_NAME = "Lightning Strike"
BALLOON_TIER = 0  # Mixed tiers

def create_balloons() -> List[Balloon]:
    """Create balloons in zigzag and wave patterns."""
    balloons = []
    
    colors = [0, 1, 2, 3, 4]  # Pink, Yellow, Green, Blue, Red
    screen_center = SCREEN_WIDTH / 2
    
    # Wave 1: Classic zigzag rows (60 balloons)
    for wave in range(6):
        wave_y = -100 - (wave * 120)
        num_balloons = 10
        for i in range(num_balloons):
            # Zigzag pattern
            offset = 60 if i % 2 == 0 else -60
            x = screen_center + offset
            y = wave_y - i * 15
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 1.5])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="zigzag",
                pattern_data={
                    'amplitude': 80,
                    'frequency': 0.04,
                    'phase': i * 0.5
                }
            )
            balloons.append(balloon)
    
    # Wave 2: Multi-line zigzag (50 balloons)
    for wave in range(5):
        wave_y = -900 - (wave * 150)
        num_lines = 5
        for line in range(num_lines):
            for i in range(2):
                x = 200 + line * 160 + (i * 30)
                y = wave_y - i * 20
                tier = colors[(wave + line + i) % 5]
                speed_mult = 0.75 + (line % 3) * 0.5
                
                balloon = Balloon(
                    x=x,
                    y=y,
                    tier=tier,
                    speed=BALLOON_SPEED,
                    speed_multiplier=speed_mult,
                    pattern="zigzag",
                    pattern_data={
                        'amplitude': 40 + line * 5,
                        'frequency': 0.03 + line * 0.005,
                        'phase': i * math.pi
                    }
                )
                balloons.append(balloon)
    
    # Wave 3: Wave pattern (sine wave) (40 balloons)
    for wave in range(4):
        wave_y = -1700 - (wave * 180)
        for i in range(10):
            # Position along a sine wave
            wave_pos = i / 10
            x = 100 + wave_pos * (SCREEN_WIDTH - 200)
            y = wave_y - i * 8 + math.sin(wave_pos * 4 * math.pi) * 40
            tier = colors[(wave + i) % 5]
            speed_mult = 0.5 + (i % 4) * 0.5
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="wave",
                pattern_data={
                    'amplitude': 50,
                    'frequency': 0.025,
                    'phase': wave_pos * 2 * math.pi
                }
            )
            balloons.append(balloon)
    
    # Wave 4: Diagonal zigzag (40 balloons)
    for wave in range(4):
        wave_y = -2450 - (wave * 160)
        for i in range(10):
            # Diagonal with zigzag
            x = 100 + i * 50 + (wave * 30)
            y = wave_y - i * 12
            tier = colors[(wave * 2 + i) % 5]
            speed_mult = random.choice([0.5, 1.0, 2.0])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="zigzag",
                pattern_data={
                    'amplitude': 35,
                    'frequency': 0.05,
                    'phase': i * 0.3
                }
            )
            balloons.append(balloon)
    
    # Wave 5: Crossing waves (60 balloons)
    for wave in range(6):
        wave_y = -3100 - (wave * 130)
        for i in range(10):
            # Two crossing waves
            if i < 5:
                x = 150 + i * 80
                y = wave_y - i * 10
            else:
                x = SCREEN_WIDTH - 150 - (i - 5) * 80
                y = wave_y - (i - 5) * 10
            tier = colors[(wave + i) % 5]
            speed_mult = random.choice([0.5, 0.75, 1.0, 1.25, 1.5])
            
            balloon = Balloon(
                x=x,
                y=y,
                tier=tier,
                speed=BALLOON_SPEED,
                speed_multiplier=speed_mult,
                pattern="wave",
                pattern_data={
                    'amplitude': 45,
                    'frequency': 0.03,
                    'phase': (i % 5) * 0.4
                }
            )
            balloons.append(balloon)
    
    return balloons

def get_total_balloons() -> int:
    return 250
