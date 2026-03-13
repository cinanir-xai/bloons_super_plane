"""Player plane class - Retro Atari Inspired."""

import pygame
from typing import Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT,
    DART_COOLDOWN, DART_OFFSET_X,
    COLOR_RED, COLOR_RED_DARK, COLOR_WHITE, COLOR_CYAN, COLOR_BLACK
)
from .effects import EngineGlow, MuzzleFlash
from .projectiles import DartManager


@dataclass
class Player:
    """Iconic Atari-style red plane."""
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

    def handle_mouse(self, pos: Tuple[int, int]) -> None:
        self.target_x = pos[0]
        self.target_y = pos[1]

    def update(self, dt: float) -> None:
        # Smooth movement using lerp-like approach
        self.x += (self.target_x - self.x) * PLAYER_SPEED
        self.y += (self.target_y - self.y) * PLAYER_SPEED
        
        # Clamp to screen
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))
        self.y = max(self.height // 2, min(SCREEN_HEIGHT - self.height // 2, self.y))
        
        # Update effects
        self.engine_glow.update(self.x, self.y + self.height // 2, dt)
        self.muzzle_flash_left.update(dt)
        self.muzzle_flash_right.update(dt)
        
        # Shooting
        self.shoot_timer -= dt * 1000
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = DART_COOLDOWN

        self.dart_manager.update(dt)

    def shoot(self) -> None:
        lx = self.x - DART_OFFSET_X
        rx = self.x + DART_OFFSET_X
        y = self.y - self.height // 4
        
        self.dart_manager.spawn_from_player(lx, y, rx, y)
        self.muzzle_flash_left.trigger(lx, y)
        self.muzzle_flash_right.trigger(rx, y)

    def draw(self, surface: pygame.Surface) -> None:
        # 1. Darts
        self.dart_manager.draw(surface)
        
        # 2. Engine Exhaust
        self.engine_glow.draw(surface, self.x, self.y + self.height // 2)
        
        # 3. Muzzle Flashes
        self.muzzle_flash_left.draw(surface)
        self.muzzle_flash_right.draw(surface)
        
        # 4. Plane Body (Sharp geometric shapes)
        cx, cy = int(self.x), int(self.y)
        hw, hh = self.width // 2, self.height // 2
        
        # Wings (Large rectangle)
        pygame.draw.rect(surface, COLOR_RED, (cx - hw, cy - 8, self.width, 16))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - hw, cy - 8, self.width, 16), 2)
        
        # Fuselage (Long vertical rectangle)
        pygame.draw.rect(surface, COLOR_RED, (cx - 8, cy - hh, 16, self.height))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 8, cy - hh, 16, self.height), 2)
        
        # Nose (Small rectangle)
        pygame.draw.rect(surface, COLOR_WHITE, (cx - 4, cy - hh - 4, 8, 8))
        
        # Cockpit (Cyan square)
        pygame.draw.rect(surface, COLOR_CYAN, (cx - 4, cy - 12, 8, 8))
        
        # Tail Fin
        pygame.draw.rect(surface, COLOR_RED_DARK, (cx - 12, cy + hh - 8, 24, 8))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 12, cy + hh - 8, 24, 8), 2)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
