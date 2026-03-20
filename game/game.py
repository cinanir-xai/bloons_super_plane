"""Main game engine and loop."""

import pygame
import sys
import math

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    BALLOON_SPEED, DART_COOLDOWN
)
from .background import Background
from .player import Player
from .effects import Vignette, ScreenShake
from .enemies import BalloonManager, Balloon
from .orbs import OrbManager
from .level_manager import LevelManager
from .menus import MainMenu, LevelSelect, Shop


class Game:
    """Main game class with retro visuals and level system."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SKY DEFENDER")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Game state: "main_menu", "level_select", "shop", "playing"
        self.game_state = "main_menu"
        
        # Level management
        self.level_manager = LevelManager()
        
        # Create game objects
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.vignette = Vignette(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.orb_manager = OrbManager()
        self.balloon_manager = BalloonManager(self.orb_manager)
        
        # Menu screens
        self.main_menu = MainMenu()
        self.level_select = LevelSelect()
        self.shop = Shop()
        
        # Visual effects
        self.screen_shake = ScreenShake()
        
        # Collision tracking (avoid repeated collision checks)
        self._collision_checked = set()
        
        # State
        self.running = True
        self.paused = False
        
        # Hide mouse cursor (only during gameplay)
        pygame.mouse.set_visible(True)
        
        # Track orbs at level start
        self.level_start_orbs = 0
        
        # Player progress (persists across levels)
        self.unlocked_levels = 1
        self.level_stars = {}
        self.level_perfect = {}
        self.level_total_balloons = 0
        self.debug_unlock_all = False
        
        # Current level being played
        self.current_level = 1
        
        # Level completion state
        self.level_complete_timer = 0.0  # 3 second delay before shop
        self.level_complete_pending = False
        self.level_complete_stars = 0
        self.level_complete_popped = 0
        self.level_complete_total = 0
        self.level_complete_ratio = 0.0

    def _load_level(self, level_num: int) -> None:
        """Load a specific level."""
        balloons = self.level_manager.load_level(level_num)
        self.balloon_manager.balloons = balloons
        self.balloon_manager.off_screen_count = 0
        self.level_start_orbs = self.orb_manager.total_orbs
        self.level_total_balloons = len(balloons)
        pygame.mouse.set_visible(False)
        # Reset completion state
        self.level_complete_timer = 0.0
        self.level_complete_pending = False

    def _handle_debug_menu_input(self, event: pygame.event.Event) -> None:
        """Handle debug shortcuts on the main menu."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_f:
            # Unlock all levels
            self.unlocked_levels = self.level_manager.total_levels
            self.debug_unlock_all = True
            self.level_select.unlocked_levels = self.unlocked_levels
        elif event.key == pygame.K_e:
            # Add 1000 orbs
            self.orb_manager.total_orbs += 1000

    def _on_level_complete(self) -> None:
        """Handle level completion - goes to shop/workshop with next level button."""
        orbs_this_level = self.orb_manager.total_orbs - self.level_start_orbs
        
        # Transition to shop with level complete mode
        self.game_state = "shop"
        pygame.mouse.set_visible(True)
        
        # Create shop with next level button
        self.shop = Shop(
            total_orbs=self.orb_manager.total_orbs,
            dart_speed_level=self.player.dart_manager.dart_speed_level if hasattr(self.player.dart_manager, 'dart_speed_level') else 0,
            dart_pierce_level=self.player.dart_pierce_level,
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
            ice_level=self.player.ice_level,
            wingman_level=self.player.wingman_level,
            orb_magnet_level=self.orb_manager.magnet_level,
            orb_luck_level=self.orb_manager.orb_luck_level,
            show_next_level=True,
            level_num=self.level_manager.current_level_num,
            has_next=self.level_manager.has_next_level(),
            orbs_collected=orbs_this_level
        )

    def _get_level_unlocked(self, level_num: int) -> bool:
        """Return True if the level is unlocked based on stars or debug override."""
        if self.debug_unlock_all:
            return True
        if level_num == 1:
            return True
        return self.level_stars.get(level_num - 1, 0) >= 1

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "main_menu":
                self._handle_debug_menu_input(event)
                result = self.main_menu.handle_event(event)
                if result == 'play':
                    self.game_state = "level_select"
                    pygame.mouse.set_visible(True)
                elif result == 'shop':
                    self._sync_shop_state()
                    self.game_state = "shop"
                    pygame.mouse.set_visible(True)
                elif result == 'quit':
                    self.running = False
            
            elif self.game_state == "level_select":
                result = self.level_select.handle_event(event)
                if result == 'back':
                    self.game_state = "main_menu"
                elif result.startswith('level_'):
                    level_num = int(result.split('_')[1])
                    if self._get_level_unlocked(level_num):
                        self.current_level = level_num
                        self._load_level(level_num)
                        self.game_state = "playing"
                        pygame.mouse.set_visible(False)
            
            elif self.game_state == "shop":
                result = self.shop.handle_event(event)
                if result == 'back':
                    # If we came from level complete, go to main menu
                    self.game_state = "main_menu"
                    self._sync_player_upgrades()
                    pygame.mouse.set_visible(True)
                elif result == 'next_level':
                    # Load next level and start playing
                    next_level = self.level_manager.get_next_level_num()
                    if self._get_level_unlocked(next_level):
                        self.current_level = next_level
                        self._load_level(next_level)
                        self.game_state = "playing"
                        pygame.mouse.set_visible(False)
                    self._sync_player_upgrades()
                elif result == 'retry_level':
                    self.current_level = self.level_manager.current_level_num
                    self._load_level(self.current_level)
                    self.game_state = "playing"
                    pygame.mouse.set_visible(False)
                    self._sync_player_upgrades()
                elif result == 'buy_dart':
                    self.shop.buy_upgrade('dart')
                elif result == 'buy_dart_pierce':
                    self.shop.buy_upgrade('dart_pierce')
                elif result == 'buy_laser':
                    self.shop.buy_upgrade('laser')
                elif result == 'buy_missile':
                    self.shop.buy_upgrade('missile')
                elif result == 'buy_boomerang':
                    self.shop.buy_upgrade('boomerang')
                elif result == 'buy_lightning':
                    self.shop.buy_upgrade('lightning')
                elif result == 'buy_ice':
                    self.shop.buy_upgrade('ice')
                elif result == 'buy_wingman':
                    self.shop.buy_upgrade('wingman')
                elif result == 'buy_orb_magnet':
                    self.shop.buy_upgrade('orb_magnet')
                    self.orb_manager.set_magnet_level(self.shop.orb_magnet_level)
                elif result == 'buy_orb_luck':
                    self.shop.buy_upgrade('orb_luck')
                    self.orb_manager.set_orb_luck_level(self.shop.orb_luck_level)
            
            elif self.game_state == "playing":
                self._handle_playing_events(event)

    def _handle_playing_events(self, event: pygame.event.Event) -> None:
        """Handle events during gameplay."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "main_menu"
                pygame.mouse.set_visible(True)
            elif event.key == pygame.K_p:
                self.paused = not self.paused
        
        elif event.type == pygame.MOUSEMOTION:
            self.player.handle_mouse(event.pos)


    def _sync_shop_state(self) -> None:
        """Sync shop state with player progress."""
        self.shop = Shop(
            total_orbs=self.orb_manager.total_orbs,
            dart_speed_level=self.player.dart_manager.dart_speed_level if hasattr(self.player.dart_manager, 'dart_speed_level') else 0,
            dart_pierce_level=self.player.dart_pierce_level,
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
            ice_level=self.player.ice_level,
            wingman_level=self.player.wingman_level,
            orb_magnet_level=self.orb_manager.magnet_level,
            orb_luck_level=self.orb_manager.orb_luck_level,
            show_next_level=False
        )

    def _sync_player_upgrades(self) -> None:
        """Sync player upgrades from shop."""
        self.orb_manager.total_orbs = self.shop.total_orbs
        self.orb_manager.set_magnet_level(self.shop.orb_magnet_level)
        self.orb_manager.set_orb_luck_level(self.shop.orb_luck_level)
        # Apply any new upgrades
        while self.player.laser_level < self.shop.laser_level:
            self.player.upgrade_laser()
        while self.player.missile_level < self.shop.missile_level:
            self.player.upgrade_missile()
        while self.player.boomerang_level < self.shop.boomerang_level:
            self.player.upgrade_boomerang()
        while self.player.lightning_level < self.shop.lightning_level:
            self.player.upgrade_lightning()
        while self.player.ice_level < self.shop.ice_level:
            self.player.upgrade_ice()
        while self.player.wingman_level < self.shop.wingman_level:
            self.player.upgrade_wingman()
        while self.player.dart_pierce_level < self.shop.dart_pierce_level:
            self.player.upgrade_dart_pierce()
        if hasattr(self.player.dart_manager, 'dart_speed_level'):
            while self.player.dart_manager.dart_speed_level < self.shop.dart_speed_level:
                self.player.dart_manager.dart_speed_level += 1
        else:
            self.player.dart_manager.dart_speed_level = self.shop.dart_speed_level
        # Sync dart pierce level to dart manager
        self.player.dart_manager.dart_pierce_level = self.player.dart_pierce_level

        self.orb_manager.set_magnet_level(self.shop.orb_magnet_level)
        self.orb_manager.set_orb_luck_level(self.shop.orb_luck_level)

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused:
            return
        
        # Update screen shake
        self.screen_shake.update(dt)
        
        if self.game_state == "playing":
            self._update_playing(dt)
        # Menu states (main_menu, level_select, shop) don't need update

    def _update_playing(self, dt: float) -> None:
        """Update gameplay."""
        self.background.update(dt)
        self.player.update(dt)
        
        # Update balloons
        self.balloon_manager.update(dt)
        
        # Check for delayed balloon spawns
        pending_balloons = self.level_manager.get_pending_spawns()
        if pending_balloons:
            self.balloon_manager.balloons.extend(pending_balloons)
        
        # Update orbs with magnet effect towards player
        self.orb_manager.update(dt, self.player.x, self.player.y)
        
        # Check dart collisions with balloons
        darts = self.player.dart_manager.get_darts()
        if darts:
            from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
            balloon_candidates = [b for b in self.balloon_manager.balloons if not b.popped]
            self._collision_checked.clear()
            for dart in darts[:]:
                if not dart.can_hit():
                    continue
                for balloon in balloon_candidates:
                    pair_key = (id(dart), id(balloon))
                    if pair_key in self._collision_checked:
                        continue
                    self._collision_checked.add(pair_key)
                    if self._check_collision(dart, balloon):
                        # Check if balloon will be fully popped (red tier = 4 or MOAB/BFB)
                        will_pop = balloon.tier >= 4 or balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
                        
                        # Pop balloon with subtle screen shake (10% of original)
                        self.balloon_manager.pop_balloon(balloon, dart.x, dart.y, damage_type="physical")
                        self.screen_shake.trigger(intensity=0.8, duration=0.6)
                        
                        # Record the hit and check if dart should be removed
                        dart.record_hit()
                        if not dart.can_hit():
                            self.player.dart_manager.remove_dart(dart)
                        
                        # Track for level completion (only count when fully popped)
                        if will_pop:
                            self.level_manager.balloon_popped()
                        
                        break
        
        # Check laser collisions
        if self.player.has_laser and self.player.laser and self.player.laser.active:
            from .constants import LASER_POP_DELAY
            from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
            laser = self.player.laser
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for balloon in active_balloons:
                # Check collision with laser beam
                laser_hits = False
                if balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                    # MOAB/BFB rectangular collision
                    rect = balloon.get_rect()
                    laser_hits = rect.left <= laser.x <= rect.right and balloon.y < laser.y_start
                else:
                    laser_hits = abs(balloon.x - laser.x) < balloon.radius + 5 and balloon.y < laser.y_start
                
                if laser_hits:
                    b_id = id(balloon)
                    laser.pop_timers[b_id] = laser.pop_timers.get(b_id, 0) + dt * 1000
                    
                    # Visual effect for laser hitting balloon
                    laser.emit_hit_particles(self.screen, balloon.y)
                    
                    if laser.pop_timers[b_id] >= LASER_POP_DELAY:
                        will_pop = balloon.tier >= 4 or balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
                        self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y, damage_type="magic")
                        if will_pop:
                            self.level_manager.balloon_popped()
                        laser.pop_timers[b_id] = 0
        
        # Check missile collisions
        if self.player.has_missile:
            from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
            missile_manager = self.player.missile_manager
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for missile in missile_manager.missiles[:]:
                for balloon in active_balloons:
                    # Check collision with missile
                    missile_hits = False
                    if balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                        rect = balloon.get_rect()
                        missile_hits = rect.collidepoint(missile.x, missile.y)
                    else:
                        dx = missile.x - balloon.x
                        dy = missile.y - balloon.y
                        dist = (dx * dx + dy * dy) ** 0.5
                        missile_hits = dist < balloon.radius + 10
                    
                    if missile_hits:
                        # Explode!
                        missile_manager.trigger_explosion(missile.x, missile.y, missile.aoe_radius)
                        
                        # AoE damage (explosive)
                        for b in active_balloons:
                            bdx = missile.x - b.x
                            bdy = missile.y - b.y
                            bdist = (bdx * bdx + bdy * bdy) ** 0.5
                            # For MOAB/BFB, check if explosion center is within aoe_radius + half of size
                            if b.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                                in_aoe = bdist < missile.aoe_radius + max(b.width, b.height) / 2
                            else:
                                in_aoe = bdist < missile.aoe_radius
                            
                            if in_aoe:
                                will_pop = b.tier >= 4 or b.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
                                self.balloon_manager.pop_balloon(b, b.x, b.y, damage_type="explosive")
                                if will_pop:
                                    self.level_manager.balloon_popped()
                        
                        if missile in missile_manager.missiles:
                            missile_manager.missiles.remove(missile)
                        break
        
        # Check boomerang collisions
        if self.player.has_boomerang:
            from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
            bm = self.player.boomerang_manager
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for boomerang in bm.boomerangs:
                for balloon in active_balloons:
                    # Check collision with boomerang
                    boomerang_hits = False
                    if balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                        rect = balloon.get_rect()
                        boomerang_hits = rect.collidepoint(boomerang.x, boomerang.y)
                    else:
                        dx = boomerang.x - balloon.x
                        dy = boomerang.y - balloon.y
                        dist = (dx * dx + dy * dy) ** 0.5
                        boomerang_hits = dist < balloon.radius + 15
                    
                    if boomerang_hits:
                        # Damage balloon (physical)
                        will_pop = balloon.tier >= 4 or balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
                        self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y, damage_type="physical")
                        if will_pop:
                            self.level_manager.balloon_popped()
                        # Boomerang pierces, so no break here

        # Check ice (Chilling Wind) effects
        if self.player.has_ice:
            from .enemies import BALLOON_TYPE_WHITE, BALLOON_TYPE_ZEBRA, BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
            ice_manager = self.player.ice_manager
            ice_radius = ice_manager.get_radius()
            ice_slow = ice_manager.get_slow_amount()
            ice_damage_interval = ice_manager.get_damage_interval()
            
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for balloon in active_balloons:
                # Calculate distance from player
                dx = balloon.x - self.player.x
                dy = balloon.y - self.player.y
                dist = (dx * dx + dy * dy) ** 0.5
                
                # Check if balloon is in ice radius
                # MOAB/BFB have larger hitboxes
                if balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                    effective_radius = ice_radius + max(balloon.width, balloon.height) / 2
                else:
                    effective_radius = ice_radius + balloon.radius
                
                if dist < effective_radius:
                    # White and Zebra balloons are immune to ice
                    if balloon.balloon_type in (BALLOON_TYPE_WHITE, BALLOON_TYPE_ZEBRA):
                        continue
                    
                    # Apply slow effect
                    balloon.slow_amount = ice_slow
                    
                    # Apply damage over time
                    balloon.ice_damage_timer += dt
                    if balloon.ice_damage_timer >= ice_damage_interval:
                        balloon.ice_damage_timer = 0
                        # Apply ice damage
                        will_pop = balloon.tier >= 4 or balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
                        self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y, damage_type="ice")
                        if will_pop:
                            self.level_manager.balloon_popped()

        # Check lightning strikes
        if self.player.has_lightning and self.player.lightning_manager.can_strike():
            target = self._get_closest_balloon(self.player.x, self.player.y)
            if target:
                self._trigger_lightning_strike(target)

        # Update wingmen attacks
        if self.player.has_wingman:
            self._update_wingmen(dt)

        # Check if level complete (all balloons popped or off-screen, no delayed spawns)
        remaining = self.balloon_manager.get_remaining_count()
        delayed_remaining = len(self.level_manager.delayed_spawns)
        
        if remaining <= 0 and delayed_remaining == 0:
            if not self.level_complete_pending:
                # Start the completion timer
                self.level_complete_pending = True
                self.level_complete_timer = 0.0
                # Calculate stars now
                self._calculate_level_completion()
        
        # Handle completion timer
        if self.level_complete_pending:
            self.level_complete_timer += dt
            if self.level_complete_timer >= 3.0:
                self._handle_level_complete_flow()
    
    def _calculate_level_completion(self) -> None:
        """Calculate stars and stats for level completion."""
        total = max(1, self.level_total_balloons)
        popped = total - self.balloon_manager.get_total_off_screen()
        popped = max(0, min(total, popped))
        ratio = popped / total
        
        if ratio >= 0.9:
            stars = 3
        elif ratio >= 0.5:
            stars = 2
        elif ratio >= 0.25:
            stars = 1
        else:
            stars = 0
        
        self.level_complete_stars = stars
        self.level_complete_popped = popped
        self.level_complete_total = total
        self.level_complete_ratio = ratio

    def _handle_level_complete_flow(self) -> None:
        """Use pre-calculated stars and go to shop."""
        stars = self.level_complete_stars
        popped = self.level_complete_popped
        total = self.level_complete_total
        ratio = self.level_complete_ratio
        perfect = popped == total
        
        previous_stars = self.level_stars.get(self.level_manager.current_level_num, 0)
        best_stars = max(previous_stars, stars)
        if best_stars > previous_stars:
            self.level_stars[self.level_manager.current_level_num] = best_stars
        self.level_perfect[self.level_manager.current_level_num] = (
            self.level_perfect.get(self.level_manager.current_level_num, False) or perfect
        )
        
        # Unlock next level only if this level has at least 1 star (or debug unlock)
        if best_stars >= 1 or self.debug_unlock_all:
            self.unlocked_levels = max(self.unlocked_levels, self.level_manager.current_level_num + 1)
        
        orbs_this_level = self.orb_manager.total_orbs - self.level_start_orbs
        self.game_state = "shop"
        pygame.mouse.set_visible(True)
        self.shop = Shop(
            total_orbs=self.orb_manager.total_orbs,
            dart_speed_level=self.player.dart_manager.dart_speed_level if hasattr(self.player.dart_manager, 'dart_speed_level') else 0,
            dart_pierce_level=self.player.dart_pierce_level,
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
            ice_level=self.player.ice_level,
            wingman_level=self.player.wingman_level,
            orb_magnet_level=self.orb_manager.magnet_level,
            orb_luck_level=self.orb_manager.orb_luck_level,
            show_next_level=True,
            level_num=self.level_manager.current_level_num,
            has_next=self.level_manager.has_next_level() and (best_stars >= 1 or self.debug_unlock_all),
            stars_earned=stars,
            perfect=perfect,
            popped_ratio=ratio,
            orbs_collected=orbs_this_level
        )
        self.level_manager.level_complete = False

    def _check_collision(self, dart, balloon) -> bool:
        """Check if dart collides with balloon."""
        from .projectiles import Dart
        from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
        if isinstance(dart, Dart) and isinstance(balloon, Balloon):
            if balloon.popped:
                return False
            
            # MOAB/BFB use rectangular collision
            if balloon.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB):
                rect = balloon.get_rect()
                return rect.collidepoint(dart.x, dart.y)
            
            # Regular circular collision
            dx = dart.x - balloon.x
            dy = dart.y - balloon.y
            dist = (dx * dx + dy * dy) ** 0.5
            return dist < balloon.radius + 5
        return False

    def _get_closest_balloon(self, x: float, y: float) -> Balloon:
        """Find the closest active balloon to a point."""
        closest = None
        closest_dist = float('inf')
        for balloon in self.balloon_manager.balloons:
            if balloon.popped:
                continue
            dx = balloon.x - x
            dy = balloon.y - y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < closest_dist:
                closest = balloon
                closest_dist = dist
        return closest

    def _trigger_lightning_strike(self, target: Balloon) -> None:
        """Trigger lightning strike on target and arc to nearby balloons."""
        from .enemies import BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB
        manager = self.player.lightning_manager
        arc_count = manager.get_arc_count()

        # Primary strike (magic damage)
        manager.trigger_strike((self.player.x, self.player.y - self.player.height // 2), (target.x, target.y))
        will_pop = target.tier >= 4 or target.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
        self.balloon_manager.pop_balloon(target, target.x, target.y, damage_type="magic")
        if will_pop:
            self.level_manager.balloon_popped()

        # Find arc targets sorted by distance to primary target
        candidates = []
        for balloon in self.balloon_manager.balloons:
            if balloon.popped or balloon is target:
                continue
            dx = balloon.x - target.x
            dy = balloon.y - target.y
            dist = (dx * dx + dy * dy) ** 0.5
            candidates.append((dist, balloon))

        candidates.sort(key=lambda item: item[0])
        for _, arc_target in candidates[:arc_count]:
            manager.trigger_strike((target.x, target.y), (arc_target.x, arc_target.y), apply_cooldown=False)
            arc_pop = arc_target.tier >= 4 or arc_target.balloon_type in (BALLOON_TYPE_MOAB, BALLOON_TYPE_BFB)
            self.balloon_manager.pop_balloon(arc_target, arc_target.x, arc_target.y, damage_type="magic")
            if arc_pop:
                self.level_manager.balloon_popped()

    def _get_furthest_balloon(self) -> Balloon:
        """Find balloon closest to bottom of screen (furthest along)."""
        furthest = None
        max_y = -float('inf')
        for balloon in self.balloon_manager.balloons:
            if balloon.popped:
                continue
            if balloon.y > max_y:
                max_y = balloon.y
                furthest = balloon
        return furthest

    def _update_wingmen(self, dt: float) -> None:
        """Update wingman positions and fire darts."""
        # Flight target stays above player (for smooth arcs)
        flight_target = (self.player.x, self.player.y - 200)

        # Find closest balloon for shooting
        target = self._get_closest_balloon(self.player.x, self.player.y)

        self.player.wingman_manager.update(self.player.x, self.player.y, flight_target, dt)
        base_cooldown = DART_COOLDOWN

        for wingman in self.player.wingman_manager.get_wingmen():
            if target and wingman.can_shoot():
                angle_deg = math.degrees(math.atan2(target.y - wingman.y, target.x - wingman.x)) + 90
                self.player.dart_manager.spawn_single(wingman.x, wingman.y, angle_deg)
                wingman.reset_cooldown(base_cooldown)
            elif not target and wingman.can_shoot():
                wingman.reset_cooldown(base_cooldown)

    def draw(self, dt: float) -> None:
        """Draw everything based on current state."""
        # Get shake offset
        shake_offset = self.screen_shake.apply(self.screen)
        
        if self.game_state == "main_menu":
            self.main_menu.draw(self.screen, dt)
        elif self.game_state == "level_select":
            # Update level select with current unlock progress
            self.level_select.unlocked_levels = self.unlocked_levels
            self.level_select.level_stars = self.level_stars
            self.level_select.level_perfect = self.level_perfect
            self.level_select.draw(self.screen)
        elif self.game_state == "shop":
            self.shop.draw(self.screen)
        elif self.game_state == "playing":
            self._draw_playing(shake_offset)
        
        pygame.display.flip()

    def _draw_playing(self, shake_offset: tuple = (0, 0)) -> None:
        """Draw gameplay with optional screen shake."""
        # Create a temporary surface for shaking
        if shake_offset != (0, 0):
            temp_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            self.background.draw(temp_surface)
            self.orb_manager.draw(temp_surface)
            self.balloon_manager.draw(temp_surface)
            self.player.draw(temp_surface)
            self.vignette.draw(temp_surface)
            # Draw delay countdown if applicable
            self._draw_delay_countdown(temp_surface)
            # Draw completion overlay if pending
            if self.level_complete_pending:
                self._draw_completion_overlay(temp_surface)
            self.screen.blit(temp_surface, shake_offset)
        else:
            self.background.draw(self.screen)
            self.orb_manager.draw(self.screen)
            self.balloon_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.vignette.draw(self.screen)
            # Draw delay countdown if applicable
            self._draw_delay_countdown(self.screen)
            # Draw completion overlay if pending
            if self.level_complete_pending:
                self._draw_completion_overlay(self.screen)

    def _draw_completion_overlay(self, surface: pygame.Surface) -> None:
        """Draw stars and completion message during 3-second delay."""
        import math
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = min(180, int(self.level_complete_timer * 60))  # Fade in
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))
        
        # Draw stars in center
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 - 50
        star_size = 60
        
        # Pulsing effect
        pulse = 1.0 + 0.1 * math.sin(self.level_complete_timer * 5)
        
        for i in range(3):
            x = center_x + (i - 1) * 90
            y = center_y
            
            if i < self.level_complete_stars:
                # Filled star (gold)
                color = (255, 215, 0)  # Gold
                self._draw_star(surface, x, y, int(star_size * pulse), color, filled=True)
            else:
                # Empty star outline
                color = (100, 100, 100)
                self._draw_star(surface, x, y, star_size, color, filled=False)
        
        # Draw "Level Complete!" text
        font_large = pygame.font.Font(None, 72)
        text = font_large.render("Level Complete!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, center_y + 100))
        surface.blit(text, text_rect)
        
        # Draw score info
        font_small = pygame.font.Font(None, 36)
        score_text = f"Popped: {self.level_complete_popped}/{self.level_complete_total}"
        score_surface = font_small.render(score_text, True, (200, 200, 200))
        score_rect = score_surface.get_rect(center=(center_x, center_y + 150))
        surface.blit(score_surface, score_rect)
        
        # Draw countdown
        remaining = max(0, 3.0 - self.level_complete_timer)
        countdown_text = f"Next in {remaining:.1f}s"
        countdown_surface = font_small.render(countdown_text, True, (150, 150, 150))
        countdown_rect = countdown_surface.get_rect(center=(center_x, center_y + 190))
        surface.blit(countdown_surface, countdown_rect)
    
    def _draw_star(self, surface: pygame.Surface, cx: int, cy: int, size: int, color: tuple, filled: bool = True) -> None:
        """Draw a 5-pointed star."""
        import math
        
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            r = size if i % 2 == 0 else size * 0.4
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            points.append((x, y))
        
        if filled:
            pygame.draw.polygon(surface, color, points)
            # Highlight
            pygame.draw.polygon(surface, (255, 255, 200), points, 2)
        else:
            pygame.draw.polygon(surface, color, points, 2)

    def _draw_delay_countdown(self, surface: pygame.Surface) -> None:
        """Draw countdown timer for delayed balloon spawns."""
        delay_remaining = self.level_manager.get_delay_remaining()
        if delay_remaining > 0:
            # Draw warning banner at top of screen
            font = pygame.font.Font(None, 36)
            text = f"Reinforcements arriving in {delay_remaining:.1f}s"
            text_surface = font.render(text, True, (255, 220, 100))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
            
            # Draw background box
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(surface, (40, 40, 60), bg_rect, border_radius=5)
            pygame.draw.rect(surface, (100, 100, 140), bg_rect, 2, border_radius=5)
            
            surface.blit(text_surface, text_rect)

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(0) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw(dt)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()
