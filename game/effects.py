"""Visual effects for the game - Retro Atari Inspired."""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_WHITE, COLOR_YELLOW, COLOR_ORANGE, COLOR_RED,
    COLOR_BLUE, COLOR_BLACK, PARTICLE_SIZE
)


@dataclass
class Particle:
    """A single square particle for retro visual effects."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: Tuple[int, int, int]
    life: float
    max_life: float

    def update(self, dt: float) -> bool:
        """Update particle. Returns False if particle should be removed."""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt * 60
        return self.life > 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the square particle."""
        alpha = int((self.life / self.max_life) * 255)
        if alpha <= 0: return
        
        s = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surface.blit(s, (int(self.x - self.size/2), int(self.y - self.size/2)))


class ParticleSystem:
    """Manages multiple retro square particles."""
    
    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x: float, y: float, color: Tuple[int, int, int],
             count: int = 5, speed: float = 2.0, size: float = PARTICLE_SIZE) -> None:
        """Emit particles at a position."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            s = random.uniform(speed * 0.5, speed * 1.5)
            life = random.uniform(10, 30)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * s,
                vy=math.sin(angle) * s,
                size=size,
                color=color,
                life=life,
                max_life=life
            ))

    def update(self, dt: float) -> None:
        """Update all particles."""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)


class EngineGlow:
    """Retro square exhaust for the plane."""
    
    def __init__(self):
        self.particles: List[Particle] = []
        self.timer = 0

    def update(self, x: float, y: float, dt: float) -> None:
        """Update the engine exhaust."""
        self.timer += dt * 60
        if self.timer >= 2:  # Emit every 2 frames
            self.timer = 0
            self.particles.append(Particle(
                x=x + random.uniform(-4, 4),
                y=y,
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(3, 6),
                size=PARTICLE_SIZE,
                color=random.choice([COLOR_ORANGE, COLOR_YELLOW, COLOR_WHITE]),
                life=15,
                max_life=15
            ))
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface, x: float, y: float) -> None:
        """Draw the engine exhaust."""
        for particle in self.particles:
            particle.draw(surface)


class MuzzleFlash:
    """Simple retro muzzle flash."""
    
    def __init__(self):
        self.active = False
        self.timer = 0
        self.x = 0
        self.y = 0

    def trigger(self, x: float, y: float) -> None:
        self.active = True
        self.timer = 3  # Last for 3 frames
        self.x = x
        self.y = y

    def update(self, dt: float) -> None:
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.active: return
        # Simple yellow square/diamond
        size = 8
        pygame.draw.rect(surface, COLOR_YELLOW, (self.x - size/2, self.y - size/2, size, size))


class DartTrail:
    """Simple square trail for darts."""
    
    def __init__(self):
        self.particles: List[Particle] = []

    def add(self, x: float, y: float) -> None:
        if random.random() < 0.3:
            self.particles.append(Particle(
                x=x, y=y,
                vx=0, vy=random.uniform(0.5, 1.5),
                size=2,
                color=COLOR_WHITE,
                life=10,
                max_life=10
            ))

    def update(self, dt: float) -> None:
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        for particle in self.particles:
            particle.draw(surface)


class AtmosphericHaze:
    """Not used in retro style to keep it clean."""
    def update(self, dt: float) -> None: pass
    def draw(self, surface: pygame.Surface) -> None: pass


class Vignette:
    """Clean retro border instead of vignette."""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw(self, surface: pygame.Surface) -> None:
        # Draw a sharp 4px black border
        pygame.draw.rect(surface, COLOR_BLACK, (0, 0, self.width, self.height), 4)
