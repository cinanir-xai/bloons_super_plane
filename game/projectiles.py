"""Projectile classes for the game."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DART_SPEED, DART_WIDTH, DART_HEIGHT,
    DART_LIFETIME, COLOR_WHITE, COLOR_GRAY, COLOR_GRAY_LIGHT, COLOR_BLUE_LIGHT
)
from .effects import DartTrail


@dataclass
class Dart:
    """A dart projectile."""
    x: float
    y: float
    vx: float
    vy: float
    rotation: float
    life: float
    trail: DartTrail
    from_left_wing: bool

    def update(self, dt: float) -> bool:
        """Update dart position. Returns False if dart should be removed."""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt * 1000
        
        # Update trail
        self.trail.add(self.x, self.y)
        self.trail.update(dt)
        
        return self.life > 0 and -50 < self.x < SCREEN_WIDTH + 50 and -50 < self.y < SCREEN_HEIGHT + 50

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - DART_WIDTH // 2, self.y - DART_HEIGHT // 2,
                          DART_WIDTH, DART_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the dart with trail."""
        # Draw trail first
        self.trail.draw(surface)
        
        # Create dart surface
        dart_surf = pygame.Surface((DART_WIDTH * 3, DART_HEIGHT * 3), pygame.SRCALPHA)
        center_x = DART_WIDTH * 1.5
        center_y = DART_HEIGHT * 1.5
        
        # Draw dart body (elongated diamond shape)
        points = [
            (center_x, center_y - DART_HEIGHT // 2 - 5),  # Tip
            (center_x + DART_WIDTH // 2, center_y - 2),    # Right
            (center_x + DART_WIDTH // 3, center_y + DART_HEIGHT // 2),  # Right back
            (center_x, center_y + DART_HEIGHT // 2 + 2),   # Back center
            (center_x - DART_WIDTH // 3, center_y + DART_HEIGHT // 2),  # Left back
            (center_x - DART_WIDTH // 2, center_y - 2),    # Left
        ]
        
        # Dart colors - metallic look
        body_color = (220, 220, 230)
        tip_color = (180, 180, 200)
        highlight_color = (255, 255, 255)
        
        # Draw main body
        pygame.draw.polygon(dart_surf, body_color, points)
        
        # Draw tip highlight
        pygame.draw.polygon(dart_surf, tip_color, points[:3])
        
        # Draw shine line
        pygame.draw.line(dart_surf, highlight_color,
                        (center_x - 1, center_y - DART_HEIGHT // 2),
                        (center_x - 1, center_y + DART_HEIGHT // 3), 2)
        
        # Draw fins at back
        fin_color = (150, 150, 160)
        fin_points_left = [
            (center_x - DART_WIDTH // 3, center_y + DART_HEIGHT // 2),
            (center_x - DART_WIDTH, center_y + DART_HEIGHT // 2 + 4),
            (center_x - DART_WIDTH // 3, center_y + DART_HEIGHT // 2 + 8),
        ]
        fin_points_right = [
            (center_x + DART_WIDTH // 3, center_y + DART_HEIGHT // 2),
            (center_x + DART_WIDTH, center_y + DART_HEIGHT // 2 + 4),
            (center_x + DART_WIDTH // 3, center_y + DART_HEIGHT // 2 + 8),
        ]
        pygame.draw.polygon(dart_surf, fin_color, fin_points_left)
        pygame.draw.polygon(dart_surf, fin_color, fin_points_right)
        
        # Rotate the dart
        rotated = pygame.transform.rotate(dart_surf, -self.rotation)
        
        # Blit to surface
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

    @classmethod
    def create_from_wing(cls, x: float, y: float, from_left_wing: bool) -> 'Dart':
        """Create a dart from a wing position."""
        # Slight spread
        spread = random.uniform(-0.5, 0.5)
        rotation = -90 + spread  # Pointing up
        
        vx = math.cos(math.radians(rotation)) * DART_SPEED + spread * 0.5
        vy = math.sin(math.radians(rotation)) * DART_SPEED - DART_SPEED * 0.98
        
        return cls(
            x=x, y=y,
            vx=vx, vy=vy,
            rotation=rotation,
            life=DART_LIFETIME,
            trail=DartTrail(),
            from_left_wing=from_left_wing
        )


class DartManager:
    """Manages all dart projectiles."""
    
    def __init__(self):
        self.darts: List[Dart] = []

    def spawn_from_player(self, left_wing_x: float, left_wing_y: float,
                         right_wing_x: float, right_wing_y: float) -> None:
        """Spawn darts from both wings."""
        self.darts.append(Dart.create_from_wing(left_wing_x, left_wing_y, True))
        self.darts.append(Dart.create_from_wing(right_wing_x, right_wing_y, False))

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
