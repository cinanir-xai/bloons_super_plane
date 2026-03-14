"""Projectile classes for the game - Retro Atari Inspired."""

import pygame
from typing import List
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DART_SPEED, DART_WIDTH, DART_HEIGHT,
    DART_LIFETIME, COLOR_WHITE, COLOR_YELLOW, COLOR_CYAN, LASER_WIDTH,
    COLOR_RED, MISSILE_SPEED, MISSILE_WIDTH, MISSILE_HEIGHT,
    BOOMERANG_WIDTH, BOOMERANG_HEIGHT, COLOR_BROWN, BOOMERANG_ORBIT_RADIUS,
    BOOMERANG_SPEED, COLOR_BLACK
)
from .effects import DartTrail, ParticleSystem, MissileTrail, Explosion
import math


@dataclass
class Boomerang:
    """A V-shaped brown shape that spins in circles."""
    angle: float # Orbit angle
    spin_angle: float # Self spin angle
    x: float = 0
    y: float = 0

    def update(self, player_x: float, player_y: float, dt: float) -> None:
        """Update boomerang orbit and spin."""
        self.angle += BOOMERANG_SPEED * dt
        self.spin_angle += BOOMERANG_SPEED * dt * 2 # Spins faster than it orbits
        
        rad = math.radians(self.angle)
        self.x = player_x + math.cos(rad) * BOOMERANG_ORBIT_RADIUS
        self.y = player_y + math.sin(rad) * BOOMERANG_ORBIT_RADIUS

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the V-shaped boomerang."""
        # Create a surface for rotation
        size = int(max(BOOMERANG_WIDTH, BOOMERANG_HEIGHT) * 1.5)
        temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw V shape on temp surface
        cx, cy = size // 2, size // 2
        w, h = BOOMERANG_WIDTH // 2, BOOMERANG_HEIGHT // 2
        points = [
            (cx, cy - h), # Top
            (cx + w, cy + h), # Bottom Right
            (cx, cy + h // 2), # Middle Inner
            (cx - w, cy + h) # Bottom Left
        ]
        pygame.draw.polygon(temp_surface, COLOR_BROWN, points)
        pygame.draw.polygon(temp_surface, COLOR_BLACK, points, 2)
        
        # Rotate the surface
        rotated_surface = pygame.transform.rotate(temp_surface, -self.spin_angle)
        rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_surface, rect)


class BoomerangManager:
    """Manages all boomerangs circling the player."""
    
    def __init__(self):
        self.boomerangs: List[Boomerang] = []

    def set_count(self, count: int) -> None:
        """Set the number of boomerangs, evenly spaced."""
        self.boomerangs = []
        for i in range(count):
            angle = i * (360 / count)
            self.boomerangs.append(Boomerang(angle=angle, spin_angle=0))

    def update(self, player_x: float, player_y: float, dt: float) -> None:
        """Update all boomerangs."""
        for b in self.boomerangs:
            b.update(player_x, player_y, dt)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all boomerangs."""
        for b in self.boomerangs:
            b.draw(surface)


@dataclass
class Missile:
    """A white rocket with a red tip."""
    x: float
    y: float
    vx: float
    vy: float
    aoe_radius: float
    trail: MissileTrail

    def update(self, dt: float) -> bool:
        """Update missile position. Returns False if missile should be removed."""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        
        # Update trail
        self.trail.add(self.x, self.y + MISSILE_HEIGHT // 2)
        self.trail.update(dt)
        
        return -50 < self.x < SCREEN_WIDTH + 50 and -50 < self.y < SCREEN_HEIGHT + 50

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - MISSILE_WIDTH // 2, self.y - MISSILE_HEIGHT // 2,
                          MISSILE_WIDTH, MISSILE_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the missile with trail."""
        # Draw trail first
        self.trail.draw(surface)
        
        # White body
        pygame.draw.rect(surface, COLOR_WHITE, 
                        (self.x - MISSILE_WIDTH // 2, self.y - MISSILE_HEIGHT // 2, 
                         MISSILE_WIDTH, MISSILE_HEIGHT))
        # Red tip
        pygame.draw.rect(surface, COLOR_RED,
                        (self.x - MISSILE_WIDTH // 2, self.y - MISSILE_HEIGHT // 2,
                         MISSILE_WIDTH, 8))
        # Fins
        pygame.draw.rect(surface, (150, 150, 150),
                        (self.x - MISSILE_WIDTH // 2 - 4, self.y + MISSILE_HEIGHT // 2 - 6,
                         4, 6))
        pygame.draw.rect(surface, (150, 150, 150),
                        (self.x + MISSILE_WIDTH // 2, self.y + MISSILE_HEIGHT // 2 - 6,
                         4, 6))


class MissileManager:
    """Manages all missile projectiles and explosions."""
    
    def __init__(self):
        self.missiles: List[Missile] = []
        self.explosions: List[Explosion] = []

    def spawn(self, x1: float, y1: float, x2: float, y2: float, aoe_radius: float) -> None:
        """Spawn missiles from wing tips."""
        self.missiles.append(Missile(x1, y1, 0, -MISSILE_SPEED, aoe_radius, MissileTrail()))
        self.missiles.append(Missile(x2, y2, 0, -MISSILE_SPEED, aoe_radius, MissileTrail()))

    def update(self, dt: float) -> None:
        """Update all missiles and explosions."""
        self.missiles = [m for m in self.missiles if m.update(dt)]
        self.explosions = [e for e in self.explosions if e.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all missiles and explosions."""
        for missile in self.missiles:
            missile.draw(surface)
        for explosion in self.explosions:
            explosion.draw(surface)

    def trigger_explosion(self, x: float, y: float, radius: float) -> None:
        """Trigger an explosion at a position."""
        self.explosions.append(Explosion(x, y, radius))


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
