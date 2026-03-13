"""Visual effects for the game."""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_WHITE, COLOR_YELLOW, COLOR_ORANGE, COLOR_RED,
    COLOR_BLUE, COLOR_BLUE_LIGHT, COLOR_GRAY, COLOR_GRAY_LIGHT
)


@dataclass
class Particle:
    """A single particle for visual effects."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: Tuple[int, int, int]
    alpha: float
    decay: float
    life: float

    def update(self, dt: float) -> bool:
        """Update particle. Returns False if particle should be removed."""
        self.x += self.vx * dt * FPS
        self.y += self.vy * dt * FPS
        self.size *= 0.95
        self.alpha -= self.decay * dt * FPS
        self.life -= dt * FPS
        return self.alpha > 0 and self.life > 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle."""
        if self.alpha <= 0 or self.size <= 0:
            return
        alpha = max(0, min(255, int(self.alpha)))
        color = (*self.color, alpha)
        
        # Create a surface for the particle with alpha
        size = max(1, int(self.size))
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, color, (size, size), size)
        surface.blit(particle_surf, (self.x - size, self.y - size))


@dataclass
class Trail:
    """Trail effect behind moving objects."""
    points: List[Tuple[float, float, float]] = field(default_factory=list)
    max_points: int = 8
    color: Tuple[int, int, int] = COLOR_WHITE
    width: int = 4

    def add_point(self, x: float, y: float) -> None:
        """Add a new point to the trail."""
        self.points.append((x, y, 255))
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def update(self) -> None:
        """Fade trail points."""
        new_points = []
        for x, y, alpha in self.points:
            new_alpha = alpha - 30
            if new_alpha > 0:
                new_points.append((x, y, new_alpha))
        self.points = new_points

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the trail."""
        if len(self.points) < 2:
            return
        for i in range(len(self.points) - 1):
            x1, y1, a1 = self.points[i]
            x2, y2, a2 = self.points[i + 1]
            alpha = int((a1 + a2) / 2)
            width = max(1, int(self.width * alpha / 255))
            color = (*self.color, alpha)
            
            line_surf = pygame.Surface((abs(x2 - x1) + width * 2 + 10, 
                                       abs(y2 - y1) + width * 2 + 10), pygame.SRCALPHA)
            offset_x = min(x1, x2) - width - 5
            offset_y = min(y1, y2) - width - 5
            pygame.draw.line(line_surf, color,
                           (x1 - offset_x, y1 - offset_y),
                           (x2 - offset_x, y2 - offset_y), width)
            surface.blit(line_surf, (offset_x, offset_y))


class ParticleSystem:
    """Manages multiple particles."""
    
    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x: float, y: float, color: Tuple[int, int, int],
             count: int = 5, speed_range: Tuple[float, float] = (1, 4),
             size_range: Tuple[float, float] = (2, 6),
             life_range: Tuple[float, float] = (20, 40)) -> None:
        """Emit particles at a position."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                size=random.uniform(*size_range),
                color=color,
                alpha=255,
                decay=random.uniform(3, 8),
                life=random.uniform(*life_range)
            ))

    def emit_burst(self, x: float, y: float, color: Tuple[int, int, int],
                   count: int = 20) -> None:
        """Emit a burst of particles."""
        self.emit(x, y, color, count, (2, 8), (3, 8), (15, 35))

    def update(self, dt: float) -> None:
        """Update all particles."""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)


class EngineGlow:
    """Engine glow effect for the plane."""
    
    def __init__(self):
        self.pulse = 0.0
        self.glow_particles: List[Particle] = []

    def update(self, x: float, y: float, dt: float) -> None:
        """Update the engine glow."""
        self.pulse += dt * 8
        if self.pulse > 2 * math.pi:
            self.pulse = 0

        # Add trailing particles
        if random.random() < 0.3:
            self.glow_particles.append(Particle(
                x=x + random.uniform(-3, 3),
                y=y + random.uniform(-3, 3),
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(2, 5),
                size=random.uniform(3, 8),
                color=random.choice([(255, 200, 50), (255, 150, 30), (255, 100, 20)]),
                alpha=200,
                decay=random.uniform(5, 10),
                life=random.uniform(15, 30)
            ))

        self.glow_particles = [p for p in self.glow_particles if p.update(dt)]

    def draw(self, surface: pygame.Surface, x: float, y: float) -> None:
        """Draw the engine glow."""
        # Draw main glow
        glow_size = 15 + math.sin(self.pulse) * 5
        glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        
        # Gradient glow
        for r in range(int(glow_size), 0, -1):
            alpha = int(100 * (r / glow_size))
            color = (255, 200, 50, alpha)
            pygame.draw.circle(glow_surf, color, (int(glow_size), int(glow_size)), r)
        
        surface.blit(glow_surf, (x - glow_size, y - glow_size), special_flags=pygame.BLEND_ADD)

        # Draw particles
        for particle in self.glow_particles:
            particle.draw(surface)


class MuzzleFlash:
    """Muzzle flash effect for shooting."""
    
    def __init__(self):
        self.active = False
        self.timer = 0.0
        self.duration = 0.05
        self.x = 0.0
        self.y = 0.0

    def trigger(self, x: float, y: float) -> None:
        """Trigger a muzzle flash."""
        self.active = True
        self.timer = self.duration
        self.x = x
        self.y = y

    def update(self, dt: float) -> None:
        """Update the muzzle flash."""
        if self.active:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the muzzle flash."""
        if not self.active:
            return

        flash_size = 15 + random.uniform(0, 10)
        flash_surf = pygame.Surface((int(flash_size * 2), int(flash_size * 2)), pygame.SRCALPHA)
        
        # Bright flash
        color = (255, 255, 200, int(200 * (self.timer / self.duration)))
        pygame.draw.circle(flash_surf, color, (int(flash_size), int(flash_size)), int(flash_size))
        
        # Inner bright core
        core_color = (255, 255, 255, 255)
        pygame.draw.circle(flash_surf, core_color, (int(flash_size), int(flash_size)), int(flash_size * 0.4))
        
        surface.blit(flash_surf, (self.x - flash_size, self.y - flash_size), special_flags=pygame.BLEND_ADD)


class DartTrail:
    """Special trail effect for darts."""
    
    def __init__(self):
        self.particles: List[Particle] = []

    def add(self, x: float, y: float) -> None:
        """Add a trail particle."""
        if random.random() < 0.5:
            self.particles.append(Particle(
                x=x, y=y,
                vx=random.uniform(-0.3, 0.3),
                vy=random.uniform(-0.3, 0.3),
                size=random.uniform(2, 5),
                color=random.choice([(200, 200, 220), (180, 180, 200), (160, 160, 180)]),
                alpha=150,
                decay=random.uniform(8, 15),
                life=random.uniform(10, 20)
            ))

    def update(self, dt: float) -> None:
        """Update trail particles."""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the trail."""
        for particle in self.particles:
            particle.draw(surface)


class AtmosphericHaze:
    """Atmospheric haze effect for depth."""
    
    def __init__(self):
        self.haze_points: List[Tuple[float, float, float, float]] = []
        # Generate haze particles
        for i in range(50):
            self.haze_points.append((
                random.uniform(0, 800),
                random.uniform(0, 1000),
                random.uniform(10, 40),
                random.uniform(5, 20)
            ))

    def update(self, dt: float) -> None:
        """Update haze position."""
        for i, (x, y, size, speed) in enumerate(self.haze_points):
            new_y = y + speed * dt * 60
            if new_y > 1050:
                new_y = -50
                x = random.uniform(0, 800)
            self.haze_points[i] = (x, new_y, size, speed)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw atmospheric haze."""
        for x, y, size, _ in self.haze_points:
            haze_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            for r in range(int(size), 0, -1):
                alpha = int(30 * (r / size))
                pygame.draw.circle(haze_surf, (200, 220, 255, alpha), (int(size), int(size)), r)
            surface.blit(haze_surf, (x - size, y - size), special_flags=pygame.BLEND_ADD)


class Vignette:
    """Screen vignette effect for cinematic look."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.vignette = self._create_vignette()

    def _create_vignette(self) -> pygame.Surface:
        """Create vignette surface using radial gradient."""
        vignette = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Create radial gradient
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Draw multiple ellipses for vignette effect
        for i in range(50):
            radius_x = self.width // 2 - i * (self.width // 100)
            radius_y = self.height // 2 - i * (self.height // 100)
            if radius_x > 0 and radius_y > 0:
                alpha = min(100, i * 2)
                pygame.draw.ellipse(vignette, (0, 0, 0, alpha),
                                  (center_x - radius_x, center_y - radius_y,
                                   radius_x * 2, radius_y * 2))
        
        return vignette

    def draw(self, surface: pygame.Surface) -> None:
        """Draw vignette overlay."""
        surface.blit(self.vignette, (0, 0), special_flags=pygame.BLEND_MULT)
