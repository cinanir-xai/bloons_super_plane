"""Projectile classes for the game - Retro Atari Inspired."""

import pygame
from typing import List
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DART_SPEED, DART_WIDTH, DART_HEIGHT,
    DART_LIFETIME, COLOR_WHITE, COLOR_YELLOW
)
from .effects import DartTrail


@dataclass
class Dart:
    """A clean rectangular dart pointing forward (up)."""
    x: float
    y: float
    vx: float
    vy: float
    life: float
    trail: DartTrail

    def update(self, dt: float) -> bool:
        """Update dart position. Returns False if dart should be removed."""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt * 1000
        
        # Update trail
        self.trail.add(self.x, self.y)
        self.trail.update(dt)
        
        return self.life > 0 and -20 < self.x < SCREEN_WIDTH + 20 and -20 < self.y < SCREEN_HEIGHT + 20

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - DART_WIDTH // 2, self.y - DART_HEIGHT // 2,
                          DART_WIDTH, DART_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the dart with trail."""
        # Draw trail first
        self.trail.draw(surface)
        
        # Draw clean rectangular dart pointing UP
        # Main body
        pygame.draw.rect(surface, COLOR_WHITE, 
                        (self.x - DART_WIDTH // 2, self.y - DART_HEIGHT // 2, 
                         DART_WIDTH, DART_HEIGHT))
        # Tip highlight
        pygame.draw.rect(surface, COLOR_YELLOW,
                        (self.x - DART_WIDTH // 2, self.y - DART_HEIGHT // 2,
                         DART_WIDTH, 4))

    @classmethod
    def create_from_wing(cls, x: float, y: float) -> 'Dart':
        """Create a dart from a wing position."""
        return cls(
            x=x, y=y,
            vx=0,
            vy=-DART_SPEED,
            life=DART_LIFETIME,
            trail=DartTrail()
        )


class DartManager:
    """Manages all dart projectiles."""
    
    def __init__(self):
        self.darts: List[Dart] = []

    def spawn_from_player(self, left_wing_x: float, left_wing_y: float,
                         right_wing_x: float, right_wing_y: float) -> None:
        """Spawn darts from both wings."""
        self.darts.append(Dart.create_from_wing(left_wing_x, left_wing_y))
        self.darts.append(Dart.create_from_wing(right_wing_x, right_wing_y))

    def update(self, dt: float) -> None:
        """Update all darts."""
        self.darts = [d for d in self.darts if d.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all darts."""
        for dart in self.darts:
            dart.draw(surface)

    def get_darts(self) -> List[Dart]:
        """Get all active darts."""
        return self.darts

    def remove_dart(self, dart: Dart) -> None:
        """Remove a specific dart."""
        if dart in self.darts:
            self.darts.remove(dart)
