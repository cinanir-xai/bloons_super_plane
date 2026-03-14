"""Player plane class - Retro Atari Inspired."""

import pygame
import math
from typing import Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT,
    DART_COOLDOWN, DART_OFFSET_X,
    COLOR_RED, COLOR_RED_DARK, COLOR_WHITE, COLOR_CYAN, COLOR_BLACK,
    LASER_BASE_COOLDOWN, LASER_BASE_DURATION, LASER_UPGRADE_COOLDOWN_REDUCTION,
    LASER_UPGRADE_DURATION_REDUCTION,
    MISSILE_COOLDOWN, MISSILE_BASE_AOE_RADIUS, MISSILE_UPGRADE_AOE_GROWTH,
    LIGHTNING_BASE_COOLDOWN, LIGHTNING_COOLDOWN_REDUCTION
)
from .effects import EngineGlow, MuzzleFlash
from .projectiles import DartManager, Laser, MissileManager, BoomerangManager, LightningManager, WingmanManager


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
    # Laser state
    has_laser: bool
    laser_level: int
    laser: Laser
    
    # Missile state
    has_missile: bool
    missile_level: int
    missile_manager: MissileManager
    missile_timer: float
    
    # Boomerang state
    has_boomerang: bool
    boomerang_level: int
    boomerang_manager: BoomerangManager

    # Lightning state
    has_lightning: bool
    lightning_level: int
    lightning_manager: LightningManager

    # Wingman state
    has_wingman: bool
    wingman_level: int
    wingman_manager: WingmanManager

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
        
        # Laser initialization
        self.has_laser = False
        self.laser_level = 0
        self.laser = None
        
        # Missile initialization
        self.has_missile = False
        self.missile_level = 0
        self.missile_manager = MissileManager()
        self.missile_timer = 0.0
        
        # Boomerang initialization
        self.has_boomerang = False
        self.boomerang_level = 0
        self.boomerang_manager = BoomerangManager()
        
        # Lightning initialization
        self.has_lightning = False
        self.lightning_level = 0
        self.lightning_manager = LightningManager()

        # Wingman initialization
        self.has_wingman = False
        self.wingman_level = 0
        self.wingman_manager = WingmanManager()

    def upgrade_laser(self) -> None:
        """Upgrade or buy laser."""
        if not self.has_laser:
            self.has_laser = True
            self.laser_level = 1
        else:
            self.laser_level += 1
        
        # Recalculate laser stats
        cooldown = LASER_BASE_COOLDOWN * ((1 - LASER_UPGRADE_COOLDOWN_REDUCTION) ** (self.laser_level - 1))
        duration = LASER_BASE_DURATION * ((1 - LASER_UPGRADE_DURATION_REDUCTION) ** (self.laser_level - 1))
        
        if self.laser is None:
            self.laser = Laser(self.x, self.y - self.height // 2, cooldown, duration)
        else:
            self.laser.cooldown = cooldown
            self.laser.duration = duration

    def upgrade_missile(self) -> None:
        """Upgrade or buy missiles."""
        if not self.has_missile:
            self.has_missile = True
            self.missile_level = 1
        else:
            self.missile_level += 1

    def upgrade_boomerang(self) -> None:
        """Upgrade or buy boomerangs."""
        if not self.has_boomerang:
            self.has_boomerang = True
            self.boomerang_level = 1
        else:
            self.boomerang_level += 1
        
        self.boomerang_manager.set_count(self.boomerang_level)

    def upgrade_lightning(self) -> None:
        """Upgrade or buy lightning strike."""
        if not self.has_lightning:
            self.has_lightning = True
            self.lightning_level = 1
        else:
            self.lightning_level += 1
        
        self.lightning_manager.level = self.lightning_level

    def upgrade_wingman(self) -> None:
        """Upgrade or buy wingman aces."""
        if not self.has_wingman:
            self.has_wingman = True
            self.wingman_level = 1
        else:
            self.wingman_level += 1
        
        self.wingman_manager.set_count(self.wingman_level, self.x, self.y)

    def handle_mouse(self, pos: Tuple[int, int]) -> None:
        self.target_x = pos[0]
        self.target_y = pos[1]

    def update(self, dt: float) -> None:
        # Smooth movement using lerp-like approach (frame-rate independent)
        lerp_factor = 1 - math.pow(1 - PLAYER_SPEED, dt * 60)
        self.x += (self.target_x - self.x) * lerp_factor
        self.y += (self.target_y - self.y) * lerp_factor
        
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
            speed_level = self.dart_manager.dart_speed_level
            self.shoot_timer = DART_COOLDOWN * (0.8 ** speed_level)

        if self.has_laser and self.laser:
            self.laser.update(self.x, self.y - self.height // 2, dt)

        if self.has_missile:
            self.missile_timer -= dt * 1000
            if self.missile_timer <= 0:
                self.shoot_missiles()
                self.missile_timer = MISSILE_COOLDOWN
            self.missile_manager.update(dt)

        if self.has_boomerang:
            self.boomerang_manager.update(self.x, self.y, dt)

        if self.has_lightning:
            self.lightning_manager.update(dt)

        self.dart_manager.update(dt)

    def shoot(self) -> None:
        lx = self.x - DART_OFFSET_X
        rx = self.x + DART_OFFSET_X
        y = self.y - self.height // 4
        
        self.dart_manager.spawn_from_player(lx, y, rx, y)
        self.muzzle_flash_left.trigger(lx, y)
        self.muzzle_flash_right.trigger(rx, y)

    def shoot_missiles(self) -> None:
        """Shoot missiles from wing tips."""
        lx = self.x - self.width // 2
        rx = self.x + self.width // 2
        y = self.y
        aoe_radius = MISSILE_BASE_AOE_RADIUS * (1 + MISSILE_UPGRADE_AOE_GROWTH * (self.missile_level - 1))
        self.missile_manager.spawn(lx, y, rx, y, aoe_radius)

    def draw(self, surface: pygame.Surface) -> None:
        # -2. Boomerangs
        if self.has_boomerang:
            self.boomerang_manager.draw(surface)

        # -1. Missiles
        if self.has_missile:
            self.missile_manager.draw(surface)

        # 0. Laser
        if self.has_laser and self.laser:
            self.laser.draw(surface)

        # 0.5 Lightning
        if self.has_lightning:
            self.lightning_manager.draw(surface)

        # 0.6 Wingmen
        if self.has_wingman:
            self.wingman_manager.draw(surface)

        # 1. Darts
        self.dart_manager.draw(surface)
        
        # 2. Engine Exhaust
        self.engine_glow.draw(surface, self.x, self.y + self.height // 2)
        
        # 3. Muzzle Flashes
        self.muzzle_flash_left.draw(surface)
        self.muzzle_flash_right.draw(surface)
        
        # 4. Plane Body (Detailed with gradients and effects)
        cx, cy = int(self.x), int(self.y)
        hw, hh = self.width // 2, self.height // 2
        
        # Shadow under plane
        shadow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (10, 10, self.width, self.height))
        surface.blit(shadow_surface, (cx - hw - 10, cy - hh - 10))
        
        # Wings with gradient effect
        wing_rect = pygame.Rect(cx - hw, cy - 10, self.width, 20)
        pygame.draw.rect(surface, COLOR_RED, wing_rect)
        # Wing highlights
        pygame.draw.line(surface, (255, 100, 100), (cx - hw + 2, cy - 8), (cx + hw - 2, cy - 8), 3)
        # Wing shadow
        pygame.draw.line(surface, COLOR_RED_DARK, (cx - hw + 2, cy + 8), (cx + hw - 2, cy + 8), 2)
        # Wing border
        pygame.draw.rect(surface, COLOR_BLACK, wing_rect, 2)
        
        # Wing tips with accent
        pygame.draw.rect(surface, (200, 0, 0), (cx - hw, cy - 6, 8, 12))
        pygame.draw.rect(surface, (200, 0, 0), (cx + hw - 8, cy - 6, 8, 12))
        
        # Fuselage (detailed vertical rectangle)
        fuselage_rect = pygame.Rect(cx - 10, cy - hh, 20, self.height)
        pygame.draw.rect(surface, COLOR_RED, fuselage_rect)
        # Fuselage highlight
        pygame.draw.line(surface, (255, 100, 100), (cx - 8, cy - hh + 2), (cx - 8, cy + hh - 2), 2)
        # Fuselage border
        pygame.draw.rect(surface, COLOR_BLACK, fuselage_rect, 2)
        
        # Nose cone (pointed shape)
        nose_points = [
            (cx, cy - hh - 8),
            (cx - 6, cy - hh),
            (cx + 6, cy - hh)
        ]
        pygame.draw.polygon(surface, COLOR_WHITE, nose_points)
        pygame.draw.polygon(surface, COLOR_BLACK, nose_points, 2)
        
        # Cockpit with glass effect
        cockpit_rect = pygame.Rect(cx - 6, cy - 14, 12, 12)
        pygame.draw.rect(surface, (50, 200, 255), cockpit_rect)
        pygame.draw.rect(surface, COLOR_BLACK, cockpit_rect, 2)
        # Cockpit shine
        pygame.draw.line(surface, (200, 255, 255), (cx - 4, cy - 12), (cx + 2, cy - 12), 2)
        
        # Engine vents on wings
        for i in range(3):
            vent_x = cx - hw + 15 + i * 20
            pygame.draw.rect(surface, (60, 60, 60), (vent_x, cy - 6, 8, 12))
            pygame.draw.rect(surface, COLOR_BLACK, (vent_x, cy - 6, 8, 12), 1)
        
        # Tail Fin (detailed)
        tail_rect = pygame.Rect(cx - 14, cy + hh - 10, 28, 12)
        pygame.draw.rect(surface, COLOR_RED_DARK, tail_rect)
        # Tail highlight
        pygame.draw.line(surface, (200, 50, 50), (cx - 12, cy + hh - 8), (cx + 12, cy + hh - 8), 2)
        # Tail border
        pygame.draw.rect(surface, COLOR_BLACK, tail_rect, 2)
        
        # Exhaust ports
        pygame.draw.rect(surface, (40, 40, 40), (cx - 6, cy + hh - 6, 12, 4))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 6, cy + hh - 6, 12, 4), 1)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)

    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle."""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
