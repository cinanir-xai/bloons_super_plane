"""Experience orbs and magnet system - Retro Atari Inspired."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK,
    ORB_SIZE, ORB_SPEED, ORB_MAGNET_RADIUS, ORB_MAGNET_STRENGTH,
    ORB_COLLECTION_RADIUS
)

@dataclass
class Orb:
    """A small yellow circular experience orb."""
    x: float
    y: float
    vx: float = 0.0
    vy: float = ORB_SPEED * 2.5  # 2.5x balloon speed
    gravity: float = 0.35  # Gravity acceleration
    collected: bool = False

    def update(self, dt: float, player_x: float, player_y: float) -> bool:
        """Update orb position with gravity and magnet effect."""
        # Apply gravity
        self.vy += self.gravity * dt * 60
        
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < ORB_MAGNET_RADIUS:
            # Magnet effect - stronger pull
            strength = (1.0 - dist / ORB_MAGNET_RADIUS) * ORB_MAGNET_STRENGTH
            self.vx += (dx / dist) * strength * dt * 60
            self.vy += (dy / dist) * strength * dt * 60

        # Clamp velocity
        self.vx = max(-18, min(18, self.vx))
        self.vy = max(-18, min(30, self.vy))

        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Check if collected (larger hitbox)
        if dist < ORB_COLLECTION_RADIUS:
            self.collected = True
            return False

        return self.y < SCREEN_HEIGHT + 30

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        # Larger yellow circle with gradient effect
        # Outer glow
        pygame.draw.circle(surface, (255, 200, 50), (cx, cy), ORB_SIZE + 2)
        # Main orb
        pygame.draw.circle(surface, COLOR_YELLOW, (cx, cy), ORB_SIZE)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy), ORB_SIZE, 1)
        # Inner highlight
        pygame.draw.circle(surface, (255, 255, 220), (cx - 2, cy - 2), ORB_SIZE // 2)
        # Center shine
        pygame.draw.circle(surface, (255, 255, 255), (cx - 3, cy - 3), ORB_SIZE // 3)

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
