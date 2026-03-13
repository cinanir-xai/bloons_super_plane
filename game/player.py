"""Player plane class."""

import pygame
import math
import random
from typing import Tuple, List
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT,
    DART_COOLDOWN, DART_OFFSET_X,
    COLOR_RED, COLOR_RED_DARK, COLOR_RED_LIGHT, COLOR_WHITE,
    COLOR_GRAY, COLOR_GRAY_LIGHT, COLOR_GRAY_DARK, COLOR_YELLOW
)
from .effects import EngineGlow, MuzzleFlash
from .projectiles import DartManager


@dataclass
class Player:
    """Player plane controlled by mouse."""
    x: float
    y: float
    target_x: float
    target_y: float
    width: int
    height: int
    dart_manager: DartManager
    engine_glow: EngineGlow
    muzzle_flash_left: MuzzleFlash
    muzzle_flash_right: MuzzleFlash
    shoot_timer: float
    tilt: float  # Current tilt angle for visual effect
    target_tilt: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dart_manager = DartManager()
        self.engine_glow = EngineGlow()
        self.muzzle_flash_left = MuzzleFlash()
        self.muzzle_flash_right = MuzzleFlash()
        self.shoot_timer = 0.0
        self.tilt = 0.0
        self.target_tilt = 0.0

    def handle_mouse(self, pos: Tuple[int, int]) -> None:
        """Update target position from mouse."""
        self.target_x = pos[0]
        self.target_y = pos[1]

    def update(self, dt: float) -> None:
        """Update player position and shooting."""
        # Smooth movement towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Calculate tilt based on horizontal movement
        self.target_tilt = max(-20, min(20, dx * 0.1))
        self.tilt += (self.target_tilt - self.tilt) * 0.1
        
        # Move towards target with smooth interpolation
        speed = PLAYER_SPEED * 60 * dt
        self.x += dx * 0.15 * 60 * dt
        self.y += dy * 0.15 * 60 * dt
        
        # Clamp to screen bounds
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))
        self.y = max(self.height // 2, min(SCREEN_HEIGHT - self.height // 2, self.y))
        
        # Update engine glow
        self.engine_glow.update(self.x, self.y + self.height // 2 - 5, dt)
        
        # Update muzzle flashes
        self.muzzle_flash_left.update(dt)
        self.muzzle_flash_right.update(dt)
        
        # Continuous shooting
        self.shoot_timer -= dt * 1000
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = DART_COOLDOWN

        # Update darts
        self.dart_manager.update(dt)

    def shoot(self) -> None:
        """Shoot darts from both wings."""
        # Calculate wing positions based on current position
        wing_offset = self.width // 2 - 8
        
        # Account for tilt in wing positions
        tilt_rad = math.radians(self.tilt)
        offset_x = DART_OFFSET_X + 5
        
        left_wing_x = self.x - offset_x * math.cos(tilt_rad) + 5 * math.sin(tilt_rad)
        left_wing_y = self.y - self.height // 3 + offset_x * math.sin(tilt_rad) * 0.3
        
        right_wing_x = self.x + offset_x * math.cos(tilt_rad) - 5 * math.sin(tilt_rad)
        right_wing_y = self.y - self.height // 3 - offset_x * math.sin(tilt_rad) * 0.3
        
        # Spawn darts
        self.dart_manager.spawn_from_player(left_wing_x, left_wing_y, right_wing_x, right_wing_y)
        
        # Trigger muzzle flashes
        self.muzzle_flash_left.trigger(left_wing_x, left_wing_y)
        self.muzzle_flash_right.trigger(right_wing_x, right_wing_y)

    def get_wing_positions(self) -> Tuple[float, float, float, float]:
        """Get current wing positions for shooting."""
        offset_x = DART_OFFSET_X + 5
        tilt_rad = math.radians(self.tilt)
        
        left_wing_x = self.x - offset_x * math.cos(tilt_rad) + 5 * math.sin(tilt_rad)
        left_wing_y = self.y - self.height // 3 + offset_x * math.sin(tilt_rad) * 0.3
        
        right_wing_x = self.x + offset_x * math.cos(tilt_rad) - 5 * math.sin(tilt_rad)
        right_wing_y = self.y - self.height // 3 - offset_x * math.sin(tilt_rad) * 0.3
        
        return left_wing_x, left_wing_y, right_wing_x, right_wing_y

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player plane."""
        # Draw darts first (behind plane)
        self.dart_manager.draw(surface)
        
        # Create plane surface
        plane_surf = pygame.Surface((self.width * 2, self.height * 2), pygame.SRCALPHA)
        center_x = self.width
        center_y = self.height
        
        # Draw engine glow first (behind plane)
        self.engine_glow.draw(surface, self.x, self.y + self.height // 2 + 5)
        
        # === PLANE BODY ===
        # Main body (fuselage)
        body_color = COLOR_RED
        body_dark = COLOR_RED_DARK
        body_light = COLOR_RED_LIGHT
        
        # Fuselage shape
        fuselage = [
            (center_x, center_y - self.height // 2 - 10),  # Nose
            (center_x + 8, center_y - self.height // 3),   # Right front
            (center_x + 12, center_y),                     # Right middle
            (center_x + 8, center_y + self.height // 3),   # Right back
            (center_x + 6, center_y + self.height // 2),   # Right tail
            (center_x + 4, center_y + self.height // 2 + 8),  # Right fin
            (center_x, center_y + self.height // 2 + 12),  # Tail center
            (center_x - 4, center_y + self.height // 2 + 8),  # Left fin
            (center_x - 6, center_y + self.height // 2),   # Left tail
            (center_x - 8, center_y + self.height // 3),   # Left back
            (center_x - 12, center_y),                     # Left middle
            (center_x - 8, center_y - self.height // 3),   # Left front
        ]
        pygame.draw.polygon(plane_surf, body_color, fuselage)
        
        # Body highlight
        pygame.draw.line(plane_surf, body_light,
                        (center_x - 3, center_y - self.height // 2),
                        (center_x - 2, center_y + self.height // 3), 3)
        
        # === WINGS ===
        wing_y = center_y - 5
        
        # Left wing
        left_wing = [
            (center_x - 15, wing_y),
            (center_x - 25, wing_y - 8),
            (center_x - 35, wing_y - 5),
            (center_x - 38, wing_y),
            (center_x - 35, wing_y + 8),
            (center_x - 25, wing_y + 12),
            (center_x - 15, wing_y + 5),
        ]
        pygame.draw.polygon(plane_surf, body_color, left_wing)
        pygame.draw.polygon(plane_surf, body_dark, left_wing, 2)
        
        # Left wing detail
        pygame.draw.line(plane_surf, body_light,
                        (center_x - 20, wing_y - 3),
                        (center_x - 30, wing_y), 2)
        
        # Right wing
        right_wing = [
            (center_x + 15, wing_y),
            (center_x + 25, wing_y - 8),
            (center_x + 35, wing_y - 5),
            (center_x + 38, wing_y),
            (center_x + 35, wing_y + 8),
            (center_x + 25, wing_y + 12),
            (center_x + 15, wing_y + 5),
        ]
        pygame.draw.polygon(plane_surf, body_color, right_wing)
        pygame.draw.polygon(plane_surf, body_dark, right_wing, 2)
        
        # Right wing detail
        pygame.draw.line(plane_surf, body_light,
                        (center_x + 20, wing_y - 3),
                        (center_x + 30, wing_y), 2)
        
        # === COCKPIT ===
        cockpit_color = (100, 180, 255)
        cockpit_highlight = (180, 220, 255)
        pygame.draw.ellipse(plane_surf, cockpit_color,
                          (center_x - 8, center_y - self.height // 3 - 5, 16, 20))
        pygame.draw.ellipse(plane_surf, cockpit_highlight,
                          (center_x - 5, center_y - self.height // 3 - 3, 6, 10))
        
        # === TAIL FIN ===
        tail_fin = [
            (center_x, center_y + self.height // 2),
            (center_x + 8, center_y + self.height // 2 - 10),
            (center_x + 4, center_y + self.height // 2 + 15),
            (center_x, center_y + self.height // 2 + 18),
            (center_x - 4, center_y + self.height // 2 + 15),
            (center_x - 8, center_y + self.height // 2 - 10),
        ]
        pygame.draw.polygon(plane_surf, body_color, tail_fin)
        pygame.draw.polygon(plane_surf, body_dark, tail_fin, 2)
        
        # Tail stripe
        pygame.draw.line(plane_surf, body_light,
                        (center_x, center_y + self.height // 2),
                        (center_x, center_y + self.height // 2 + 15), 2)
        
        # === ENGINE EXHAUST ===
        exhaust_color = (80, 80, 90)
        pygame.draw.ellipse(plane_surf, exhaust_color,
                          (center_x - 4, center_y + self.height // 2 + 8, 8, 6))
        
        # === ENGINE GLOW PARTICLES (behind) ===
        # Already drawn above
        
        # === MUZZLE FLASHES ===
        self.muzzle_flash_left.draw(surface)
        self.muzzle_flash_right.draw(surface)
        
        # Rotate entire plane surface based on tilt
        rotated = pygame.transform.rotate(plane_surf, self.tilt)
        
        # Blit to main surface
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
