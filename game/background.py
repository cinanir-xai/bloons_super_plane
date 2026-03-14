"""Background rendering for the game - Retro Atari Inspired."""

import pygame
import random
from typing import List, Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCENERY_SPEED,
    CLOUD_COUNT, TREE_COUNT, RIVER_WIDTH,
    COLOR_BG_GRASS, COLOR_BG_RIVER, COLOR_WHITE, COLOR_GREEN,
    COLOR_BG_SAND, COLOR_YELLOW
)

@dataclass
class Cloud:
    """A clean white rectangular cloud."""
    x: float
    y: float
    width: float
    height: float
    speed: float

    def update(self, dt: float) -> None:
        self.y += self.speed * dt * 60
        if self.y > SCREEN_HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, SCREEN_WIDTH - int(self.width))

    def draw(self, surface: pygame.Surface) -> None:
        # Draw a clean white rectangle with a border
        pygame.draw.rect(surface, COLOR_WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 2)

@dataclass
class Tree:
    """A simple geometric tree."""
    x: float
    y: float
    size: float

    def update(self, dt: float) -> None:
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size
            self.x = random.randint(20, SCREEN_WIDTH - 20)

    def draw(self, surface: pygame.Surface) -> None:
        # Square trunk
        pygame.draw.rect(surface, (139, 69, 19), (self.x - 4, self.y, 8, 12))
        # Triangle top (retro style)
        points = [(self.x, self.y - self.size), (self.x - self.size/2, self.y), (self.x + self.size/2, self.y)]
        pygame.draw.polygon(surface, COLOR_GREEN, points)

class Background:
    """Main background manager with clean Atari scenery."""
    
    def __init__(self):
        self.clouds: List[Cloud] = []
        self.trees: List[Tree] = []
        self.river_x = SCREEN_WIDTH // 2 - RIVER_WIDTH // 2
        
        self._generate_background()

    def _generate_background(self) -> None:
        # Clouds
        for _ in range(CLOUD_COUNT):
            self.clouds.append(Cloud(
                x=random.randint(0, SCREEN_WIDTH),
                y=random.randint(0, SCREEN_HEIGHT),
                width=random.randint(80, 120),
                height=random.randint(40, 60),
                speed=random.uniform(0.5, 1.2)
            ))
        
        # Trees
        for _ in range(TREE_COUNT):
            x = self._get_valid_tree_x()
            self.trees.append(Tree(x=x, y=random.randint(0, SCREEN_HEIGHT), size=40))

    def _get_valid_tree_x(self) -> int:
        """Get an X coordinate that is not on the river."""
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            # Avoid river + banks
            if x < self.river_x - 40 or x > self.river_x + RIVER_WIDTH + 40:
                return x

    def update(self, dt: float) -> None:
        for cloud in self.clouds:
            cloud.update(dt)
        for tree in self.trees:
            tree.update(dt)
            if tree.y < -tree.size + 10: # Just respawned or wrapped
                tree.x = self._get_valid_tree_x()

    def draw(self, surface: pygame.Surface) -> None:
        # 1. Base Grass
        surface.fill(COLOR_BG_GRASS)
        
        # 2. Draw River (Straight and clean)
        pygame.draw.rect(surface, COLOR_BG_RIVER, (self.river_x, 0, RIVER_WIDTH, SCREEN_HEIGHT))
        # River banks
        pygame.draw.rect(surface, COLOR_BG_SAND, (self.river_x - 10, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(surface, COLOR_BG_SAND, (self.river_x + RIVER_WIDTH, 0, 10, SCREEN_HEIGHT))
        
        # 3. Draw Trees
        for tree in self.trees:
            tree.draw(surface)
            
        # 4. Draw Clouds
        for cloud in self.clouds:
            cloud.draw(surface)
