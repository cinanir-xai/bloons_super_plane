"""Projectile classes for the game - Retro Atari Inspired."""

import pygame
from typing import List, Tuple
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DART_SPEED, DART_WIDTH, DART_HEIGHT,
    DART_LIFETIME, COLOR_WHITE, COLOR_YELLOW, COLOR_CYAN, LASER_WIDTH,
    COLOR_RED, MISSILE_SPEED, MISSILE_WIDTH, MISSILE_HEIGHT,
    BOOMERANG_WIDTH, BOOMERANG_HEIGHT, COLOR_BROWN, BOOMERANG_ORBIT_RADIUS,
    BOOMERANG_SPEED, COLOR_BLACK,
    LIGHTNING_BASE_COOLDOWN, LIGHTNING_COOLDOWN_REDUCTION,
    LIGHTNING_BASE_ARCS, LIGHTNING_ARC_GROWTH,
    LIGHTNING_STRIKE_COLOR, LIGHTNING_GLOW_COLOR
)
from .effects import DartTrail, ParticleSystem, MissileTrail, Explosion
import math
import random


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
        """Draw the boomerang with enhanced visual appeal."""
        # Create a surface for rotation
        size = int(max(BOOMERANG_WIDTH, BOOMERANG_HEIGHT) * 1.8)
        temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw boomerang on temp surface
        cx, cy = size // 2, size // 2
        w, h = BOOMERANG_WIDTH // 2, BOOMERANG_HEIGHT // 2
        
        # Main V shape with curved wings
        points = [
            (cx, cy - h), # Top point
            (cx + w, cy + h), # Bottom Right
            (cx, cy + h // 2), # Middle Inner
            (cx - w, cy + h) # Bottom Left
        ]
        
        # Outer glow
        pygame.draw.polygon(temp_surface, (139, 69, 19, 100), 
                           [(p[0]+2, p[1]+2) for p in points])
        
        # Main shape
        pygame.draw.polygon(temp_surface, COLOR_BROWN, points)
        
        # Wood grain lines
        for i in range(4):
            pygame.draw.line(temp_surface, (100, 50, 20),
                           (cx - w//2 + i * 5, cy),
                           (cx + w//2 - i * 5, cy), 1)
        
        # Black border
        pygame.draw.polygon(temp_surface, COLOR_BLACK, points, 2)
        
        # Highlight on top
        pygame.draw.line(temp_surface, (180, 100, 60),
                        (cx - w//2 + 2, cy - h + 2),
                        (cx + w//2 - 2, cy - h + 2), 2)
        
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
        """Draw the missile with enhanced visual appeal."""
        # Draw trail first
        self.trail.draw(surface)
        
        cx, cy = int(self.x), int(self.y)
        w, h = MISSILE_WIDTH, MISSILE_HEIGHT
        
        # Outer glow for rocket
        glow_surface = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (255, 255, 255, 30), (5, 5, w, h))
        surface.blit(glow_surface, (cx - w//2 - 5, cy - h//2 - 5))
        
        # Main body (white with gradient)
        pygame.draw.rect(surface, COLOR_WHITE, (cx - w//2, cy - h//2, w, h))
        
        # Metallic shine on left side
        pygame.draw.rect(surface, (230, 230, 230), (cx - w//2, cy - h//2, w//3, h))
        
        # Red tip (nose cone)
        pygame.draw.polygon(surface, COLOR_RED, [
            (cx, cy - h//2 - 6),
            (cx - w//2, cy - h//2),
            (cx + w//2, cy - h//2)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx, cy - h//2 - 6),
            (cx - w//2, cy - h//2),
            (cx + w//2, cy - h//2)
        ], 1)
        
        # Body stripes
        for i in range(3):
            stripe_y = cy - h//4 + i * (h//4)
            pygame.draw.line(surface, (200, 200, 200), 
                           (cx - w//2 + 1, stripe_y), (cx + w//2 - 1, stripe_y), 1)
        
        # Black border
        pygame.draw.rect(surface, COLOR_BLACK, (cx - w//2, cy - h//2, w, h), 2)
        
        # Large fins
        fin_color = (180, 50, 50)
        # Left fin
        pygame.draw.polygon(surface, fin_color, [
            (cx - w//2, cy + h//2 - 4),
            (cx - w//2 - 8, cy + h//2 + 8),
            (cx - w//2, cy + h//2)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx - w//2, cy + h//2 - 4),
            (cx - w//2 - 8, cy + h//2 + 8),
            (cx - w//2, cy + h//2)
        ], 1)
        # Right fin
        pygame.draw.polygon(surface, fin_color, [
            (cx + w//2, cy + h//2 - 4),
            (cx + w//2 + 8, cy + h//2 + 8),
            (cx + w//2, cy + h//2)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx + w//2, cy + h//2 - 4),
            (cx + w//2 + 8, cy + h//2 + 8),
            (cx + w//2, cy + h//2)
        ], 1)
        
        # Exhaust glow
        pygame.draw.circle(surface, (255, 200, 50), (cx, cy + h//2 + 4), 6)
        pygame.draw.circle(surface, (255, 255, 200), (cx, cy + h//2 + 4), 3)


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
        """Draw the laser beam with enhanced visual appeal."""
        if not self.active:
            # Draw a pulsing "charging" indicator if close to active
            if self.cooldown_timer < 1000:
                pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.01)
                alpha = int(255 * pulse * (1 - self.cooldown_timer / 1000))
                s = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(s, (*COLOR_CYAN, alpha), (10, 10), 10)
                pygame.draw.circle(s, (*COLOR_WHITE, alpha), (10, 10), 5)
                surface.blit(s, (int(self.x - 10), int(self.y_start - 10)))
            return
            
        import random
        
        # Outer glow (thickest)
        pygame.draw.line(surface, (0, 200, 255, 80), (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH + 10)
        # Medium glow
        pygame.draw.line(surface, (0, 220, 255), (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH + 6)
        # Main beam
        pygame.draw.line(surface, COLOR_CYAN, (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH + 2)
        # Inner bright core
        pygame.draw.line(surface, COLOR_WHITE, (self.x, self.y_start), (self.x, self.y_end), LASER_WIDTH)
        
        # Animated base flare
        if random.random() > 0.2:
            # Base flare with pulse
            pulse_r = random.randint(10, 18)
            pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y_start)), pulse_r)
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(self.y_start)), pulse_r // 2)
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y_start)), pulse_r // 4)
            
            # Beam jitter for energy feel
            for _ in range(2):
                off = random.uniform(-2, 2)
                pygame.draw.line(surface, (200, 255, 255), 
                               (self.x + off, self.y_start), 
                               (self.x + off, self.y_end), 1)
        
        # Energy particles along beam occasionally
        if random.random() > 0.7:
            py = random.uniform(self.y_end, self.y_start)
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(py)), 2)


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
        """Draw the dart with enhanced visual appeal."""
        # Draw trail first
        self.trail.draw(surface)
        
        # Draw dart pointing UP with detailed design
        cx, cy = int(self.x), int(self.y)
        w, h = DART_WIDTH, DART_HEIGHT
        
        # Outer glow
        glow_surface = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 255, 255, 50), (2, 2, w, h))
        surface.blit(glow_surface, (cx - w//2 - 2, cy - h//2 - 2))
        
        # Main body with gradient
        pygame.draw.rect(surface, COLOR_WHITE, (cx - w//2, cy - h//2, w, h))
        
        # Metallic shine gradient
        for i in range(w//2):
            alpha = int(100 * (1 - i / (w//2)))
            pygame.draw.line(surface, (255, 255, 255), 
                           (cx - w//2 + i, cy - h//2), 
                           (cx - w//2 + i, cy + h//2), 1)
        
        # Yellow tip (sharp point)
        pygame.draw.polygon(surface, COLOR_YELLOW, [
            (cx, cy - h//2 - 4),
            (cx - w//2, cy - h//2),
            (cx + w//2, cy - h//2)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx, cy - h//2 - 4),
            (cx - w//2, cy - h//2),
            (cx + w//2, cy - h//2)
        ], 1)
        
        # Black border
        pygame.draw.rect(surface, COLOR_BLACK, (cx - w//2, cy - h//2, w, h), 2)
        
        # Fletching at back
        pygame.draw.rect(surface, (200, 50, 50), (cx - w//2 - 2, cy + h//2 - 4, w + 4, 6))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - w//2 - 2, cy + h//2 - 4, w + 4, 6), 1)

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


@dataclass
class LightningStrike:
    """Lightning strike visual effect."""
    start_pos: Tuple[float, float]
    end_pos: Tuple[float, float]
    duration: float = 0.2  # seconds
    timer: float = 0.0
    segments: List[Tuple[float, float]] = field(default_factory=list)

    def __post_init__(self):
        if not self.segments:
            self._generate_segments()

    def _generate_segments(self):
        """Generate jagged lightning path."""
        self.segments = []
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        
        # Create jagged segments
        num_segments = 8
        for i in range(num_segments + 1):
            t = i / num_segments
            x = sx + (ex - sx) * t
            y = sy + (ey - sy) * t
            
            # Add jitter except for endpoints
            if 0 < i < num_segments:
                x += random.uniform(-12, 12)
                y += random.uniform(-8, 8)
            self.segments.append((x, y))

    def update(self, dt: float) -> bool:
        """Update effect. Returns False when done."""
        self.timer += dt
        return self.timer < self.duration

    def draw(self, surface: pygame.Surface) -> None:
        """Draw lightning strike."""
        if not self.segments or len(self.segments) < 2:
            return
        
        # Flicker intensity
        flicker = 0.6 + 0.4 * math.sin(self.timer * 35)
        glow_width = int(6 + 2 * flicker)
        core_width = max(1, int(2 * flicker))
        
        # Draw glow
        for i in range(len(self.segments) - 1):
            pygame.draw.line(surface, LIGHTNING_GLOW_COLOR, 
                           self.segments[i], self.segments[i+1], glow_width)
        
        # Draw main lightning
        for i in range(len(self.segments) - 1):
            pygame.draw.line(surface, LIGHTNING_STRIKE_COLOR,
                           self.segments[i], self.segments[i+1], 3)
        
        # Inner bright core
        for i in range(len(self.segments) - 1):
            pygame.draw.line(surface, COLOR_WHITE,
                           self.segments[i], self.segments[i+1], core_width)
        
        # Add small sparkles
        if random.random() > 0.6:
            idx = random.randint(0, len(self.segments) - 2)
            sx, sy = self.segments[idx]
            pygame.draw.circle(surface, COLOR_WHITE, (int(sx), int(sy)), 2)


class LightningManager:
    """Manages lightning strikes and cooldown."""
    
    def __init__(self, level: int = 0):
        self.level = level
        self.cooldown_timer = 0
        self.strikes: List[LightningStrike] = []

    def update(self, dt: float) -> None:
        """Update cooldown and active strikes."""
        self.cooldown_timer = max(0, self.cooldown_timer - dt * 1000)
        self.strikes = [s for s in self.strikes if s.update(dt)]

    def can_strike(self) -> bool:
        """Check if lightning can strike."""
        return self.level > 0 and self.cooldown_timer <= 0

    def trigger_strike(self, start_pos: Tuple[float, float], end_pos: Tuple[float, float], apply_cooldown: bool = True) -> None:
        """Trigger a lightning strike effect."""
        self.strikes.append(LightningStrike(start_pos, end_pos))
        if apply_cooldown:
            self.cooldown_timer = self.get_cooldown()

    def get_cooldown(self) -> float:
        """Get current cooldown based on level."""
        if self.level <= 0:
            return LIGHTNING_BASE_COOLDOWN
        # Apply cooldown reduction per level
        return LIGHTNING_BASE_COOLDOWN * ((1 - LIGHTNING_COOLDOWN_REDUCTION) ** (self.level - 1))

    def get_arc_count(self) -> int:
        """Get number of extra targets."""
        if self.level <= 0:
            return 0
        return LIGHTNING_BASE_ARCS + (self.level - 1) * LIGHTNING_ARC_GROWTH

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all active lightning strikes."""
        for strike in self.strikes:
            strike.draw(surface)
