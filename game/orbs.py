"""Experience orbs and magnet system - Retro Atari Inspired."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK,
    ORB_SIZE, ORB_SPEED, ORB_MAGNET_RADIUS, ORB_MAGNET_STRENGTH
)

@dataclass
class Orb:
    """A small yellow experience orb."""
    x: float
    y: float
    vx: float = 0.0
    vy: float = ORB_SPEED
    collected: bool = False

    def update(self, dt: float, player_x: float, player_y: float) -> bool:
        """Update orb position with magnet effect."""
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < ORB_MAGNET_RADIUS:
            # Magnet effect
            strength = (1.0 - dist / ORB_MAGNET_RADIUS) * ORB_MAGNET_STRENGTH
            self.vx += (dx / dist) * strength
            self.vy += (dy / dist) * strength
            
            # Dampen velocity slightly to prevent extreme erratic movement
            self.vx *= 0.95
            self.vy *= 0.95
        else:
            # Normal drift down
            self.vx *= 0.9
            self.vy = (self.vy * 0.9) + (ORB_SPEED * 0.1)

        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Check if collected
        if dist < 20:
            self.collected = True
            return False

        return self.y < SCREEN_HEIGHT + 20

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        # Small yellow square with black outline
        pygame.draw.rect(surface, COLOR_YELLOW, (cx - ORB_SIZE//2, cy - ORB_SIZE//2, ORB_SIZE, ORB_SIZE))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - ORB_SIZE//2, cy - ORB_SIZE//2, ORB_SIZE, ORB_SIZE), 1)

class OrbManager:
    """Manages all experience orbs and currency."""
    
    def __init__(self):
        self.orbs: List[Orb] = []
        self.total_orbs = 0

    def spawn_orbs(self, x: float, y: float, count: int = 2) -> None:
        """Spawn orbs at a position."""
        for _ in range(count):
            self.orbs.append(Orb(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vx=random.uniform(-2, 2),
                vy=random.uniform(-1, 1)
            ))

    def update(self, dt: float, player_x: float, player_y: float) -> None:
        """Update all orbs and track collection."""
        new_orbs = []
        for orb in self.orbs:
            if orb.update(dt, player_x, player_y):
                new_orbs.append(orb)
            elif orb.collected:
                self.total_orbs += 1
        self.orbs = new_orbs

    def draw(self, surface: pygame.Surface) -> None:
        for orb in self.orbs:
            orb.draw(surface)
        self._draw_ui(surface)

    def _draw_ui(self, surface: pygame.Surface) -> None:
        """Draw top-right orb counter with icon."""
        font = pygame.font.Font(None, 36)
        orb_text = font.render(str(self.total_orbs), True, COLOR_YELLOW)
        
        icon_size = 16
        x_pos = SCREEN_WIDTH - 150
        y_pos = 40
        
        # Yellow circle icon
        pygame.draw.circle(surface, COLOR_YELLOW, (x_pos, y_pos), icon_size // 2)
        pygame.draw.circle(surface, COLOR_BLACK, (x_pos, y_pos), icon_size // 2, 2)
        
        # Text
        surface.blit(orb_text, (x_pos + 20, y_pos - orb_text.get_height() // 2))
