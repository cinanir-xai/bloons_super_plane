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

    def _load_level(self, level_num: int) -> None:
        """Load a specific level."""
        balloons = self.level_manager.load_level(level_num)
        self.balloon_manager.balloons = balloons
        self.balloon_manager.off_screen_count = 0
        self.level_start_orbs = self.orb_manager.total_orbs
        self.level_total_balloons = len(balloons)
        pygame.mouse.set_visible(False)

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
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
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
                elif result == 'buy_laser':
                    self.shop.buy_upgrade('laser')
                elif result == 'buy_missile':
                    self.shop.buy_upgrade('missile')
                elif result == 'buy_boomerang':
                    self.shop.buy_upgrade('boomerang')
                elif result == 'buy_lightning':
                    self.shop.buy_upgrade('lightning')
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
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
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
        while self.player.wingman_level < self.shop.wingman_level:
            self.player.upgrade_wingman()
        if hasattr(self.player.dart_manager, 'dart_speed_level'):
            while self.player.dart_manager.dart_speed_level < self.shop.dart_speed_level:
                self.player.dart_manager.dart_speed_level += 1
        else:
            self.player.dart_manager.dart_speed_level = self.shop.dart_speed_level

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
        
        # Update orbs with magnet effect towards player
        self.orb_manager.update(dt, self.player.x, self.player.y)
        
        # Check dart collisions with balloons
        darts = self.player.dart_manager.get_darts()
        if darts:
            balloon_candidates = [b for b in self.balloon_manager.balloons if not b.popped]
            self._collision_checked.clear()
            for dart in darts[:]:
                for balloon in balloon_candidates:
                    pair_key = (id(dart), id(balloon))
                    if pair_key in self._collision_checked:
                        continue
                    self._collision_checked.add(pair_key)
                    if self._check_collision(dart, balloon):
                        # Check if balloon will be fully popped (red tier = 4)
                        will_pop = balloon.tier >= 4  # Red is tier 4, pink=0
                        
                        # Pop balloon with subtle screen shake (10% of original)
                        self.balloon_manager.pop_balloon(balloon, dart.x, dart.y)
                        self.screen_shake.trigger(intensity=0.8, duration=0.6)
                        self.player.dart_manager.remove_dart(dart)
                        
                        # Track for level completion (only count when fully popped)
                        if will_pop:
                            self.level_manager.balloon_popped()
                        
                        break
        
        # Check laser collisions
        if self.player.has_laser and self.player.laser and self.player.laser.active:
            from .constants import LASER_POP_DELAY
            laser = self.player.laser
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for balloon in active_balloons:
                if abs(balloon.x - laser.x) < balloon.radius + 5 and balloon.y < laser.y_start:
                    b_id = id(balloon)
                    laser.pop_timers[b_id] = laser.pop_timers.get(b_id, 0) + dt * 1000
                    
                    # Visual effect for laser hitting balloon
                    laser.emit_hit_particles(self.screen, balloon.y)
                    
                    if laser.pop_timers[b_id] >= LASER_POP_DELAY:
                        will_pop = balloon.tier >= 4
                        self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y)
                        if will_pop:
                            self.level_manager.balloon_popped()
                        laser.pop_timers[b_id] = 0
        
        # Check missile collisions
        if self.player.has_missile:
            missile_manager = self.player.missile_manager
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for missile in missile_manager.missiles[:]:
                for balloon in active_balloons:
                    dx = missile.x - balloon.x
                    dy = missile.y - balloon.y
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist < balloon.radius + 10:
                        # Explode!
                        missile_manager.trigger_explosion(missile.x, missile.y, missile.aoe_radius)
                        
                        # AoE damage
                        for b in active_balloons:
                            bdx = missile.x - b.x
                            bdy = missile.y - b.y
                            bdist = (bdx * bdx + bdy * bdy) ** 0.5
                            if bdist < missile.aoe_radius:
                                will_pop = b.tier >= 4
                                self.balloon_manager.pop_balloon(b, b.x, b.y)
                                if will_pop:
                                    self.level_manager.balloon_popped()
                        
                        if missile in missile_manager.missiles:
                            missile_manager.missiles.remove(missile)
                        break
        
        # Check boomerang collisions
        if self.player.has_boomerang:
            bm = self.player.boomerang_manager
            active_balloons = [b for b in self.balloon_manager.balloons if not b.popped]
            for boomerang in bm.boomerangs:
                for balloon in active_balloons:
                    dx = boomerang.x - balloon.x
                    dy = boomerang.y - balloon.y
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist < balloon.radius + 15:
                        # Damage balloon
                        will_pop = balloon.tier >= 4
                        self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y)
                        if will_pop:
                            self.level_manager.balloon_popped()
                        # Boomerang pierces, so no break here

        # Check lightning strikes
        if self.player.has_lightning and self.player.lightning_manager.can_strike():
            target = self._get_closest_balloon(self.player.x, self.player.y)
            if target:
                self._trigger_lightning_strike(target)

        # Update wingmen attacks
        if self.player.has_wingman:
            self._update_wingmen(dt)

        # Check if level complete (all balloons popped or off-screen)
        remaining = self.balloon_manager.get_remaining_count()
        if remaining <= 0:
            self.level_manager.level_complete = True
        
        if self.level_manager.level_complete:
            self._handle_level_complete_flow()

    def _handle_level_complete_flow(self) -> None:
        """Compute stars earned, update unlocks, and show end screen."""
        total = max(1, self.level_total_balloons)
        popped = total - self.balloon_manager.get_remaining_count() - self.balloon_manager.get_total_off_screen()
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
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level,
            boomerang_level=self.player.boomerang_level,
            lightning_level=self.player.lightning_level,
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
        if isinstance(dart, Dart) and isinstance(balloon, Balloon):
            if balloon.popped:
                return False
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
        manager = self.player.lightning_manager
        arc_count = manager.get_arc_count()

        # Primary strike
        manager.trigger_strike((self.player.x, self.player.y - self.player.height // 2), (target.x, target.y))
        will_pop = target.tier >= 4
        self.balloon_manager.pop_balloon(target, target.x, target.y)
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
            arc_pop = arc_target.tier >= 4
            self.balloon_manager.pop_balloon(arc_target, arc_target.x, arc_target.y)
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
            self.screen.blit(temp_surface, shake_offset)
        else:
            self.background.draw(self.screen)
            self.orb_manager.draw(self.screen)
            self.balloon_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.vignette.draw(self.screen)

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
