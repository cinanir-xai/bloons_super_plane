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
    COLOR_WHITE, COLOR_BLACK, PARTICLE_SIZE,
    ORB_LUCK_BASE_CHANCE, ORB_LUCK_CHANCE_PER_LEVEL
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
    # Movement pattern support
    speed_multiplier: float = 1.0
    pattern: str = "vertical"  # vertical, zigzag, circular, spiral, wave
    pattern_data: dict = field(default_factory=dict)
    base_x: float = 0.0  # Original x position for patterns
    base_y: float = 0.0  # Original y position for patterns
    time_alive: float = 0.0

    def __post_init__(self):
        self.radius = get_balloon_radius(self.tier)
        self.color = BALLOON_COLORS[self.tier]
        self.base_x = self.x
        self.base_y = self.y
        # Initialize pattern data
        if not self.pattern_data:
            self.pattern_data = {
                'amplitude': random.uniform(20, 60),  # For zigzag/wave
                'frequency': random.uniform(0.02, 0.05),  # For zigzag/wave/circular
                'phase': random.uniform(0, 2 * math.pi),  # For circular/spiral
                'radius': random.uniform(30, 80),  # For circular
            }

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
        
        # Update time alive
        self.time_alive += dt * 60
        
        # Calculate effective speed
        effective_speed = self.speed * self.speed_multiplier
        
        # Apply movement pattern
        if self.pattern == "vertical":
            self.y += effective_speed * dt * 60
        elif self.pattern == "zigzag":
            self.y += effective_speed * dt * 60
            amp = self.pattern_data.get('amplitude', 40)
            freq = self.pattern_data.get('frequency', 0.03)
            self.x = self.base_x + math.sin(self.time_alive * freq) * amp
        elif self.pattern == "wave":
            self.y += effective_speed * dt * 60
            amp = self.pattern_data.get('amplitude', 50)
            freq = self.pattern_data.get('frequency', 0.02)
            self.x = self.base_x + math.sin(self.time_alive * freq) * amp
        elif self.pattern == "circular":
            # Move in a circular pattern while progressing downward
            self.y += effective_speed * dt * 60 * 0.5  # Slower vertical
            rad = self.pattern_data.get('radius', 50)
            freq = self.pattern_data.get('frequency', 0.03)
            phase = self.pattern_data.get('phase', 0)
            self.x = self.base_x + math.cos(self.time_alive * freq + phase) * rad
        elif self.pattern == "spiral":
            # Spiral inward while moving down
            self.y += effective_speed * dt * 60 * 0.3
            initial_radius = self.pattern_data.get('initial_radius', 80)
            freq = self.pattern_data.get('frequency', 0.03)
            phase = self.pattern_data.get('phase', 0)
            radius = max(5, initial_radius - self.time_alive * 0.5)
            self.x = self.base_x + math.cos(self.time_alive * freq + phase) * radius
        else:
            self.y += effective_speed * dt * 60
        
        return self.y < SCREEN_HEIGHT + self.radius + 20

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the balloon with enhanced visual style."""
        if self.popped:
            self._draw_pop_animation(surface)
            return
        
        cx, cy = int(self.x), int(self.y)
        r = int(self.radius)
        
        # Draw shadow beneath balloon
        shadow_surface = pygame.Surface((r * 3, r // 2 + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 40), (r // 2, 5, r * 2, r // 2))
        surface.blit(shadow_surface, (cx - r, cy + r))
        
        # Draw balloon body with gradient effect
        # Outer glow
        pygame.draw.circle(surface, self.color, (cx, cy), r)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy), r, 3)
        
        # Inner gradient effect (darker bottom)
        inner_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)
        
        # Draw highlight (shiny top-left)
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)
        
        # Secondary highlight for more polish
        if r > 15:
            pygame.draw.circle(surface, (255, 255, 255, 180), (cx - r // 4, cy - r // 4), highlight_r // 2)
        
        # Draw string with slight curve effect
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, COLOR_BLACK, string_start, string_end, 2)
        
        # Small tie knot at top of string
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + r + 2), 2)

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
        # Emit particles with enhanced effect
        self.particle_system.emit(x, y, balloon.color, count=15, speed=5.0, size=PARTICLE_SIZE)
        
        # Add white burst particles for impact
        self.particle_system.emit(x, y, (255, 255, 255), count=8, speed=6.0, size=3)
        
        # Spawn orbs (2 per layer popped)
        self.orb_manager.spawn_orbs(x, y, count=2)

        # Orb luck bonus drops
        if self.orb_manager.orb_luck_level > 0:
            extra_chance = ORB_LUCK_BASE_CHANCE + ORB_LUCK_CHANCE_PER_LEVEL * (self.orb_manager.orb_luck_level - 1)
            extra_max = self.orb_manager.orb_luck_level
            if random.random() < extra_chance:
                extra_count = random.randint(1, extra_max)
                self.orb_manager.spawn_orbs(x, y, count=extra_count)

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
