"""Level 3 - Pink Balloons with Creative Patterns."""

from typing import List, Tuple
import math
from ..enemies import Balloon, get_balloon_radius
from ..constants import SCREEN_WIDTH, BALLOON_SPEED

LEVEL_NUMBER = 3
LEVEL_NAME = "Pink Power"
BALLOON_TIER = 0  # Pink (largest)

def create_balloons() -> List[Balloon]:
    """Wave 1: Pink balloons in tightly packed cluster."""
    balloons = []
    center_x = SCREEN_WIDTH / 2
    center_y = -150
    
    # Tightly packed circle cluster
    for ring in range(5):
        count = 6 + ring * 6
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = ring * 45
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius * 0.7
            
            balloons.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    return balloons


def get_delayed_spawns() -> List[Tuple[float, List[Balloon]]]:
    """Waves 2-4 with 8s breathing room."""
    delayed = []
    
    # Wave 2: Heart shape (8s)
    balloons2 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -200
    t_vals = [i / 50 * 2 * math.pi for i in range(50)]
    for t in t_vals:
        x = center_x + 16 * (math.sin(t)**3) * 8
        y = center_y - (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) * 5
        
        balloons2.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    delayed.append((8.0, balloons2))
    
    # Wave 3: Double triangle (16s)
    balloons3 = []
    for tri in range(2):
        offset_x = -100 if tri == 0 else 100
        base_x = SCREEN_WIDTH / 2 + offset_x
        base_y = -100
        
        for row in range(8):
            for col in range(row + 1):
                x = base_x - row * 25 + col * 50
                y = base_y - row * 40
                
                balloons3.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    delayed.append((16.0, balloons3))
    
    # Wave 4: Pink spiral with density (24s)
    balloons4 = []
    center_x = SCREEN_WIDTH / 2
    center_y = -300
    
    for i in range(60):
        angle = i * 0.3
        radius = 30 + i * 5
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius * 0.6
        
        balloons4.append(Balloon(x=x, y=y, tier=0, speed=BALLOON_SPEED))  # Pink
    
    delayed.append((24.0, balloons4))
    
    return delayed


def get_total_balloons() -> int:
    return 90 + 50 + 72 + 60  # 272
