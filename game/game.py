"""Main game engine and loop."""

import pygame
import sys

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    BALLOON_SPEED, BALLOON_SPAWN_DELAY, BALLOON_WAVE_DELAY
)
from .background import Background
from .player import Player
from .effects import Vignette
from .enemies import BalloonManager
from .orbs import OrbManager


class Game:
    """Main game class with retro visuals."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SKY DEFENDER")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.vignette = Vignette(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.orb_manager = OrbManager()
        self.balloon_manager = BalloonManager(self.orb_manager)
        
        # State
        self.running = True
        self.paused = False
        
        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
            
            elif event.type == pygame.MOUSEMOTION:
                self.player.handle_mouse(event.pos)

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused:
            return
        
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
                    # Pop balloon
                    self.balloon_manager.pop_balloon(balloon, dart.x, dart.y)
                    self.player.dart_manager.remove_dart(dart)
                    break

    def _check_collision(self, dart, balloon) -> bool:
        """Check if dart collides with balloon."""
        from .projectiles import Dart
        from .enemies import Balloon
        if isinstance(dart, Dart) and isinstance(balloon, Balloon):
            if balloon.popped: return False
            dx = dart.x - balloon.x
            dy = dart.y - balloon.y
            dist = (dx * dx + dy * dy) ** 0.5
            return dist < balloon.radius + 5
        return False

    def draw(self) -> None:
        """Draw everything with clean retro style."""
        self.background.draw(self.screen)
        self.orb_manager.draw(self.screen)
        self.balloon_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.vignette.draw(self.screen)
        
        pygame.display.flip()

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
