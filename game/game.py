"""Main game engine and loop."""

import pygame
import sys

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    BALLOON_SPEED
)
from .background import Background
from .player import Player
from .effects import Vignette
from .enemies import BalloonManager
from .orbs import OrbManager
from .level_manager import LevelManager
from .end_screen import EndScreen


class Game:
    """Main game class with retro visuals and level system."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SKY DEFENDER")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Game state: "playing", "end_screen"
        self.game_state = "playing"
        
        # Level management
        self.level_manager = LevelManager()
        
        # Create game objects
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.vignette = Vignette(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.orb_manager = OrbManager()
        self.balloon_manager = BalloonManager(self.orb_manager)
        
        # Load first level
        self._load_level(1)
        
        # End screen
        self.end_screen = None
        
        # State
        self.running = True
        self.paused = False
        
        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        
        # Track orbs at level start
        self.level_start_orbs = 0

    def _load_level(self, level_num: int) -> None:
        """Load a specific level."""
        balloons = self.level_manager.load_level(level_num)
        self.balloon_manager.balloons = balloons
        self.level_start_orbs = self.orb_manager.total_orbs
        self.game_state = "playing"
        pygame.mouse.set_visible(False)

    def _on_level_complete(self) -> None:
        """Handle level completion."""
        self.game_state = "end_screen"
        orbs_this_level = self.orb_manager.total_orbs - self.level_start_orbs
        self.end_screen = EndScreen(
            orbs_collected=orbs_this_level,
            level_num=self.level_manager.current_level_num,
            has_next=self.level_manager.has_next_level(),
            total_orbs=self.orb_manager.total_orbs,
            dart_speed_level=self.player.dart_manager.dart_speed_level if hasattr(self.player.dart_manager, 'dart_speed_level') else 0,
            laser_level=self.player.laser_level,
            missile_level=self.player.missile_level
        )
        pygame.mouse.set_visible(True)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "playing":
                self._handle_playing_events(event)
            elif self.game_state == "end_screen":
                self._handle_end_screen_events(event)

    def _handle_playing_events(self, event: pygame.event.Event) -> None:
        """Handle events during gameplay."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_p:
                self.paused = not self.paused
        
        elif event.type == pygame.MOUSEMOTION:
            self.player.handle_mouse(event.pos)

    def _handle_end_screen_events(self, event: pygame.event.Event) -> None:
        """Handle events on end screen."""
        result = self.end_screen.handle_event(event)
        
        if result == 'next':
            # Load next level
            next_level = self.level_manager.get_next_level_num()
            self._load_level(next_level)
        elif result == 'buy_laser':
            if self.orb_manager.total_orbs >= self.end_screen.laser_cost:
                self.orb_manager.total_orbs -= self.end_screen.laser_cost
                self.player.upgrade_laser()
                # Refresh end screen
                self._on_level_complete()
        elif result == 'buy_missile':
            if self.orb_manager.total_orbs >= self.end_screen.missile_cost:
                self.orb_manager.total_orbs -= self.end_screen.missile_cost
                self.player.upgrade_missile()
                # Refresh end screen
                self._on_level_complete()
        elif result == 'buy_dart':
            if self.orb_manager.total_orbs >= self.end_screen.dart_speed_cost:
                self.orb_manager.total_orbs -= self.end_screen.dart_speed_cost
                # Update dart speed level (assuming it's on dart_manager)
                if not hasattr(self.player.dart_manager, 'dart_speed_level'):
                    self.player.dart_manager.dart_speed_level = 0
                self.player.dart_manager.dart_speed_level += 1
                # Refresh end screen
                self._on_level_complete()
        elif result == 'quit':
            self.running = False

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused:
            return
        
        if self.game_state == "playing":
            self._update_playing(dt)
        elif self.game_state == "end_screen":
            pass  # End screen doesn't need update

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
        for dart in darts[:]:
            for balloon in self.balloon_manager.balloons[:]:
                if self._check_collision(dart, balloon):
                    # Check if balloon will be fully popped (red tier = 4)
                    will_pop = balloon.tier >= 4  # Red is tier 4, pink=0
                    
                    # Pop balloon
                    self.balloon_manager.pop_balloon(balloon, dart.x, dart.y)
                    self.player.dart_manager.remove_dart(dart)
                    
                    # Track for level completion (only count when fully popped)
                    if will_pop:
                        self.level_manager.balloon_popped()
                    
                    break
        
        # Check laser collisions
        if self.player.has_laser and self.player.laser and self.player.laser.active:
            from .constants import LASER_POP_DELAY
            laser = self.player.laser
            for balloon in self.balloon_manager.balloons[:]:
                if not balloon.popped and abs(balloon.x - laser.x) < balloon.radius + 5:
                    if balloon.y < laser.y_start: # Laser shoots up
                        b_id = id(balloon)
                        if b_id not in laser.pop_timers:
                            laser.pop_timers[b_id] = 0
                        
                        laser.pop_timers[b_id] += dt * 1000
                        
                        # Visual effect for laser hitting balloon
                        laser.emit_hit_particles(self.screen, balloon.y)
                        
                        if laser.pop_timers[b_id] >= LASER_POP_DELAY:
                            will_pop = balloon.tier >= 4
                            self.balloon_manager.pop_balloon(balloon, balloon.x, balloon.y)
                            if will_pop:
                                self.level_manager.balloon_popped()
                            # Reset timer for this balloon (it might become a lower tier balloon)
                            laser.pop_timers[b_id] = 0
        
        # Check missile collisions
        if self.player.has_missile:
            missile_manager = self.player.missile_manager
            for missile in missile_manager.missiles[:]:
                for balloon in self.balloon_manager.balloons[:]:
                    if not balloon.popped:
                        dx = missile.x - balloon.x
                        dy = missile.y - balloon.y
                        dist = (dx * dx + dy * dy) ** 0.5
                        if dist < balloon.radius + 10:
                            # Explode!
                            missile_manager.trigger_explosion(missile.x, missile.y, missile.aoe_radius)
                            
                            # AoE damage
                            for b in self.balloon_manager.balloons[:]:
                                if not b.popped:
                                    bdx = missile.x - b.x
                                    bdy = missile.y - b.y
                                    bdist = (bdx * bdx + bdy * bdy) ** 0.5
                                    if bdist < missile.aoe_radius:
                                        # Damage balloon
                                        will_pop = b.tier >= 4
                                        self.balloon_manager.pop_balloon(b, b.x, b.y)
                                        if will_pop:
                                            self.level_manager.balloon_popped()
                            
                            if missile in missile_manager.missiles:
                                missile_manager.missiles.remove(missile)
                            break
        
        # Check if level complete (all balloons popped or off-screen)
        remaining = self.balloon_manager.get_remaining_count()
        if remaining <= 0:
            self.level_manager.level_complete = True
        
        if self.level_manager.level_complete:
            self._on_level_complete()

    def _check_collision(self, dart, balloon) -> bool:
        """Check if dart collides with balloon."""
        from .projectiles import Dart
        from .enemies import Balloon
        if isinstance(dart, Dart) and isinstance(balloon, Balloon):
            if balloon.popped:
                return False
            dx = dart.x - balloon.x
            dy = dart.y - balloon.y
            dist = (dx * dx + dy * dy) ** 0.5
            return dist < balloon.radius + 5
        return False

    def draw(self) -> None:
        """Draw everything based on current state."""
        if self.game_state == "playing":
            self._draw_playing()
        elif self.game_state == "end_screen":
            self.end_screen.draw(self.screen)
        
        pygame.display.flip()

    def _draw_playing(self) -> None:
        """Draw gameplay."""
        self.background.draw(self.screen)
        self.orb_manager.draw(self.screen)
        self.balloon_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.vignette.draw(self.screen)

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()
