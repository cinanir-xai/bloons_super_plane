"""Projectile classes for the game - Retro Atari Inspired."""

import pygame
from typing import List
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DART_SPEED, DART_WIDTH, DART_HEIGHT,
    DART_LIFETIME, COLOR_WHITE, COLOR_YELLOW, COLOR_CYAN, LASER_WIDTH
)
from .effects import DartTrail, ParticleSystem


@dataclass
class Laser:
    """A thin cyan laser beam."""
    x: float
    y_start: float
    y_end: float
    active: bool
    timer: float
    cooldown_timer: float
    duration: float
    cooldown: float
    
    def __init__(self, x: float, y_start: float, cooldown: float, duration: float):
        self.x = x
        self.y_start = y_start
        self.y_end = 0  # Shoots up to top of screen
        self.active = False
        self.timer = 0
        self.cooldown_timer = cooldown
        self.duration = duration
        self.cooldown = cooldown
        self.pop_timers = {} # balloon_id -> timer

    def update(self, x: float, y: float, dt: float) -> None:
        """Update laser position and state."""
        self.x = x
        self.y_start = y
        
        if self.active:
            self.timer -= dt * 1000
            if self.timer <= 0:
                self.active = False
                self.cooldown_timer = self.cooldown
        else:
            self.cooldown_timer -= dt * 1000
            if self.cooldown_timer <= 0:
                self.active = True
                self.timer = self.duration
                self.pop_timers = {}
            
    def emit_hit_particles(self, surface: pygame.Surface, balloon_y: float) -> None:
        """Emit particles where laser hits a balloon."""
        import random
        for _ in range(2):
            px = self.x + random.uniform(-5, 5)
            py = balloon_y + random.uniform(-5, 5)
            size = random.uniform(2, 5)
            pygame.draw.rect(surface, COLOR_CYAN, (px, py, size, size))
            pygame.draw.rect(surface, COLOR_WHITE, (px + 1, py + 1, size - 2, size - 2))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the laser beam."""
        if not self.active:
            # Draw a small "charging" indicator if close to active
            if self.cooldown_timer < 1000:
                alpha = int(255 * (1 - self.cooldown_timer / 1000))
                s = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(s, (*COLOR_CYAN, alpha), (5, 5), 5)
                surface.blit(s, (int(self.x - 5), int(self.y_start - 5)))
            return
            
        # Outer glow (thicker)
        pygame.draw.line(surface, COLOR_CYAN, (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH + 6)
        # Main beam
        pygame.draw.line(surface, COLOR_CYAN, (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH + 2)
        # Inner core
        pygame.draw.line(surface, COLOR_WHITE, (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH)
        
        # Add some flickering and base effect
        import random
        if random.random() > 0.3:
            # Base flare
            r = random.randint(8, 14)
            pygame.draw.circle(surface, COLOR_CYAN, (int(self.x), int(self.y_start)), r)
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(self.y_start)), r // 2)
            
            # Beam jitter
            off = random.uniform(-1, 1)
            pygame.draw.line(surface, COLOR_WHITE, (self.x + off, self.y_start), (self.x + off, self.y_end), 1)


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
