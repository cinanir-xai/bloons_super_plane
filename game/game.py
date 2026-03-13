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


from .effects import Vignette

class Game:
    """Main game class with retro visuals."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SKY DEFENDER - RETRO")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.vignette = Vignette(SCREEN_WIDTH, SCREEN_HEIGHT)
        
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

    def draw(self) -> None:
        """Draw everything with clean retro style."""
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        
        # Clean border
        self.vignette.draw(self.screen)
        
        self._draw_ui()
        pygame.display.flip()

    def _draw_ui(self) -> None:
        """Draw clean retro UI."""
        font = pygame.font.Font(None, 24)
        title = font.render("SKY DEFENDER", True, COLOR_WHITE)
        self.screen.blit(title, (20, 20))
        
        if self.paused:
            pause_text = font.render("PAUSED", True, (255, 255, 0))
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2))

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
