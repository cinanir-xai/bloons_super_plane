"""Main game engine and loop."""

import pygame
import sys
from typing import Optional

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_BLACK, COLOR_WHITE
)
from .background import Background
from .player import Player


class Game:
    """Main game class."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sky Defender - Vertical Shooter")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        # State
        self.running = True
        self.paused = False
        
        # Mouse position
        self.mouse_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Hide mouse cursor (we use a plane instead)
        pygame.mouse.set_visible(True)

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
                self.mouse_pos = event.pos
                self.player.handle_mouse(self.mouse_pos)

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused:
            return
        
        # Update background
        self.background.update(dt)
        
        # Update player (includes shooting)
        self.player.update(dt)

    def draw(self) -> None:
        """Draw everything to screen."""
        # Clear screen
        self.screen.fill(COLOR_BLACK)
        
        # Draw background
        self.background.draw(self.screen)
        
        # Draw player (includes darts)
        self.player.draw(self.screen)
        
        # Draw UI elements
        self._draw_ui()
        
        # Update display
        pygame.display.flip()

    def _draw_ui(self) -> None:
        """Draw UI elements."""
        # Draw a subtle border
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)
        
        # Draw title (subtle)
        font = pygame.font.Font(None, 36)
        title = font.render("SKY DEFENDER", True, (255, 255, 255, 100))
        title.set_alpha(100)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()
