"""Enemy/Balloon classes for the game - BTD-style progression."""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALLOON_SPEED,
    BALLOON_BASE_RADIUS,
    COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    COLOR_WHITE, COLOR_BLACK, PARTICLE_SIZE
)
from .effects import ParticleSystem

from .orbs import OrbManager

# Balloon color progression: Pink (tier 0, largest) -> Yellow -> Green -> Blue -> Red (tier 4, smallest)
BALLOON_COLORS = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]

def get_balloon_radius(tier: int) -> float:
    """Calculate radius for a tier. Red (4) is base, each tier up +5%."""
    # tiers: 0=pink, 1=yellow, 2=green, 3=blue, 4=red
    steps_above_red = 4 - tier
    return BALLOON_BASE_RADIUS * (1.05 ** steps_above_red)

@dataclass
class Balloon:
    """A balloon enemy with color progression."""
    x: float
    y: float
    tier: int  # 0=pink (largest), 4=red (smallest)
    speed: float
    radius: float = 0.0
    color: Tuple[int, int, int] = (0,0,0)
    popped: bool = False
    pop_animation: float = 0.0

    def __post_init__(self):
        self.radius = get_balloon_radius(self.tier)
        self.color = BALLOON_COLORS[self.tier]

    def take_damage(self) -> bool:
        """Take damage and downgrade. Returns True if should be removed."""
        self.tier += 1
        if self.tier >= len(BALLOON_COLORS):
            self.popped = True
            return True
        self.radius = get_balloon_radius(self.tier)
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
    """Manages all balloons from levels."""
    
    def __init__(self, orb_manager: OrbManager):
        self.balloons: List[Balloon] = []
        self.particle_system = ParticleSystem()
        self.orb_manager = orb_manager
        
        # Track off-screen balloons (for level progression)
        self.off_screen_count = 0

    def update(self, dt: float) -> None:
        """Update all balloons. Handle off-screen balloons."""
        new_balloons = []
        for balloon in self.balloons:
            if balloon.popped:
                if balloon.update(dt):
                    new_balloons.append(balloon)
            else:
                # Check if balloon went off screen (bottom)
                if balloon.y > SCREEN_HEIGHT + balloon.radius:
                    # Count as popped but no orbs
                    self.off_screen_count += 1
                    continue
                if balloon.update(dt):
                    new_balloons.append(balloon)
        self.balloons = new_balloons
        
        # Update particles
        self.particle_system.update(dt)

    def pop_balloon(self, balloon: Balloon, x: float, y: float) -> None:
        """Pop a balloon with animation and particles, and spawn orbs."""
        # Emit particles
        self.particle_system.emit(x, y, balloon.color, count=12, speed=4.0, size=PARTICLE_SIZE)
        
        # Spawn orbs (2 per layer popped)
        self.orb_manager.spawn_orbs(x, y, count=2)

        # Downgrade or remove
        if not balloon.take_damage():
            # Balloon downgraded, not fully popped
            pass

    def pop_balloon_no_orbs(self, balloon: Balloon) -> None:
        """Pop a balloon without spawning orbs (for off-screen)."""
        self.particle_system.emit(balloon.x, balloon.y, balloon.color, count=6, speed=2.0, size=PARTICLE_SIZE)
        balloon.take_damage()

    def get_remaining_count(self) -> int:
        """Get count of balloons still in play."""
        return len([b for b in self.balloons if not b.popped])

    def get_total_off_screen(self) -> int:
        """Get count of balloons that went off screen."""
        return self.off_screen_count

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all balloons and particles."""
        # Draw balloons
        for balloon in self.balloons:
            balloon.draw(surface)
        
        # Draw particles
        self.particle_system.draw(surface)
