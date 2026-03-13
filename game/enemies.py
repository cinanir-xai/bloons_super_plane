"""Enemy/Balloon classes for the game - BTD-style progression."""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALLOON_SPEED,
    BALLOON_SPAWN_DELAY, BALLOON_WAVE_DELAY,
    COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    COLOR_WHITE, COLOR_BLACK, PARTICLE_SIZE
)
from .effects import ParticleSystem


# Balloon color progression: Pink (tier 0, largest) -> Yellow -> Green -> Blue -> Red (tier 4, smallest)
# When shot: Pink -> Yellow -> Green -> Blue -> Red (popped)
BALLOON_COLORS = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
BALLOON_SIZES = [48, 40, 32, 24, 16]  # Radius for each tier (largest to smallest)


@dataclass
class Balloon:
    """A balloon enemy with color progression."""
    x: float
    y: float
    tier: int  # 0=pink (largest), 4=red (smallest)
    speed: float
    radius: float
    color: Tuple[int, int, int]
    popped: bool = False
    pop_animation: float = 0.0

    def __post_init__(self):
        self.radius = BALLOON_SIZES[self.tier]
        self.color = BALLOON_COLORS[self.tier]

    def take_damage(self) -> bool:
        """Take damage and downgrade. Returns True if should be removed."""
        self.tier += 1
        if self.tier >= len(BALLOON_COLORS):
            self.popped = True
            return True
        self.radius = BALLOON_SIZES[self.tier]
        self.color = BALLOON_COLORS[self.tier]
        return False

    def update(self, dt: float) -> bool:
        """Update balloon position. Returns False if off screen."""
        if self.popped:
            self.pop_animation += dt * 60
            return self.pop_animation < 15  # Animation lasts 15 frames
        self.y += self.speed * dt * 60
        return self.y < SCREEN_HEIGHT + self.radius + 20

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the balloon with retro style."""
        if self.popped:
            self._draw_pop_animation(surface)
            return
        
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        
        # Draw balloon body (circle)
        pygame.draw.circle(surface, self.color, (cx, cy), r)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy), r, 3)
        
        # Draw highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)
        
        # Draw string
        pygame.draw.line(surface, COLOR_BLACK, 
                        (cx, cy + r), (cx, cy + r + 12), 2)

    def _draw_pop_animation(self, surface: pygame.Surface) -> None:
        """Draw popping animation."""
        progress = self.pop_animation / 15
        if progress >= 1:
            return
        
        # Expanding particles
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            dist = progress * self.radius * 1.5
            px = self.x + math.cos(angle) * dist
            py = self.y + math.sin(angle) * dist
            size = max(2, int(6 * (1 - progress)))
            
            # Draw star-like particles
            pygame.draw.circle(surface, self.color, (int(px), int(py)), size)

    def get_rect(self) -> pygame.Rect:
        """Get collision rect."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)


class BalloonManager:
    """Manages all balloons and spawning patterns."""
    
    def __init__(self):
        self.balloons: List[Balloon] = []
        self.particle_system = ParticleSystem()
        
        # Spawning state
        self.spawn_timer = 0.0
        self.wave_timer = 0.0
        self.current_wave = 0  # 0=red, 1=blue, 2=green, 3=yellow, 4=pink
        self.rows_spawned = 0
        self.spawning = True
        
        # Wave order: red, blue, green, yellow, pink
        self.wave_colors = [4, 3, 2, 1, 0]  # tier indices

    def _spawn_row(self, tier: int) -> None:
        """Spawn a row of 10 balloons at the top."""
        num_balloons = 10
        spacing = SCREEN_WIDTH / (num_balloons + 1)
        start_x = spacing
        
        for i in range(num_balloons):
            x = start_x + i * spacing
            # Add slight random offset
            x += random.uniform(-10, 10)
            x = max(30, min(SCREEN_WIDTH - 30, x))
            
            balloon = Balloon(
                x=x,
                y=-30,  # Start above screen
                tier=tier,
                speed=BALLOON_SPEED,
                radius=BALLOON_SIZES[tier],
                color=BALLOON_COLORS[tier]
            )
            self.balloons.append(balloon)

    def _start_next_wave(self) -> None:
        """Start the next color wave."""
        if self.current_wave < len(self.wave_colors):
            self.rows_spawned = 0
            self.spawn_timer = 0
        else:
            self.spawning = False

    def update(self, dt: float) -> None:
        """Update all balloons and spawning."""
        # Update existing balloons
        self.balloons = [b for b in self.balloons if b.update(dt)]
        
        # Update particles
        self.particle_system.update(dt)
        
        if not self.spawning:
            return
        
        # Handle wave spawning
        if self.current_wave < len(self.wave_colors):
            tier = self.wave_colors[self.current_wave]
            
            # Spawn rows with delay
            self.spawn_timer += dt * 1000
            
            if self.rows_spawned < 5:
                if self.spawn_timer >= BALLOON_SPAWN_DELAY:
                    self.spawn_timer = 0
                    self._spawn_row(tier)
                    self.rows_spawned += 1
            else:
                # Wait for wave delay
                self.wave_timer += dt * 1000
                if self.wave_timer >= BALLOON_WAVE_DELAY:
                    self.wave_timer = 0
                    self.current_wave += 1
                    self._start_next_wave()

    def pop_balloon(self, balloon: Balloon, x: float, y: float) -> None:
        """Pop a balloon with animation and particles."""
        # Emit particles
        self.particle_system.emit(x, y, balloon.color, count=12, speed=4.0, size=PARTICLE_SIZE)
        
        # Downgrade or remove
        if not balloon.take_damage():
            # Balloon downgraded, not fully popped
            pass

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all balloons and particles."""
        # Draw balloons
        for balloon in self.balloons:
            balloon.draw(surface)
        
        # Draw particles
        self.particle_system.draw(surface)
