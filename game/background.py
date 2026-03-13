"""Background rendering for the game - top-down scenery view."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCENERY_SPEED,
    CLOUD_COUNT, TREE_COUNT, RIVER_WIDTH,
    COLOR_WHITE, COLOR_GREEN, COLOR_GREEN_DARK, COLOR_GREEN_LIGHT,
    COLOR_BLUE, COLOR_BLUE_LIGHT, COLOR_BROWN, COLOR_BROWN_DARK,
    COLOR_GRAY, COLOR_GRAY_LIGHT, COLOR_GRAY_DARK, COLOR_YELLOW
)
from .effects import AtmosphericHaze


@dataclass
class Cloud:
    """A cloud sprite."""
    x: float
    y: float
    width: float
    height: float
    speed: float
    alpha: int
    puffs: List[Tuple[float, float, float]]  # relative x, y, radius

    def update(self, dt: float) -> None:
        """Update cloud position."""
        self.y += self.speed * dt * 60
        if self.y > SCREEN_HEIGHT + self.height:
            self.y = -self.height - 50
            self.x = random.uniform(0, SCREEN_WIDTH)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the cloud."""
        cloud_surf = pygame.Surface((int(self.width * 2), int(self.height * 2)), pygame.SRCALPHA)
        
        for px, py, pr in self.puffs:
            # Draw puff with gradient
            for r in range(int(pr), 0, -1):
                alpha = int(self.alpha * (0.3 + 0.7 * (r / pr)))
                color = (255, 255, 255, alpha)
                pygame.draw.circle(cloud_surf, color,
                                 (int(self.width + px), int(self.height + py)), r)
        
        surface.blit(cloud_surf, (self.x - self.width, self.y - self.height))


@dataclass
class Tree:
    """A top-down tree sprite."""
    x: float
    y: float
    size: float
    color_variation: int
    shadow_offset: float

    def update(self, dt: float) -> None:
        """Update tree position."""
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size - 50
            self.x = random.uniform(50, SCREEN_WIDTH - 50)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the tree."""
        # Draw shadow
        shadow_surf = pygame.Surface((int(self.size * 2), int(self.size * 1.5)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60),
                          (0, 0, self.size * 2, self.size * 1.5))
        surface.blit(shadow_surf, (self.x - self.size + self.shadow_offset, 
                                   self.y - self.size * 0.7 + self.shadow_offset))
        
        # Draw tree top (circular)
        tree_color = (
            max(0, min(255, COLOR_GREEN[0] + self.color_variation)),
            max(0, min(255, COLOR_GREEN[1] + self.color_variation)),
            max(0, min(255, COLOR_GREEN[2] + self.color_variation))
        )
        
        # Multiple layers for depth
        for i in range(3):
            radius = self.size * (0.8 - i * 0.15)
            offset_y = i * self.size * 0.15
            lighter = (min(255, tree_color[0] + 30 * i),
                      min(255, tree_color[1] + 30 * i),
                      min(255, tree_color[2] + 30 * i))
            pygame.draw.circle(surface, lighter,
                             (int(self.x), int(self.y - offset_y)), int(radius))
        
        # Draw trunk
        trunk_width = self.size * 0.15
        trunk_height = self.size * 0.4
        trunk_color = (COLOR_BROWN[0] + self.color_variation // 2,
                      COLOR_BROWN[1] + self.color_variation // 2,
                      COLOR_BROWN[2] + self.color_variation // 2)
        pygame.draw.rect(surface, trunk_color,
                        (self.x - trunk_width // 2, self.y,
                         trunk_width, trunk_height))


@dataclass
class River:
    """A river flowing through the scenery."""
    x: float
    width: float
    curve_points: List[Tuple[float, float]]  # x offset, y position
    speed: float

    def update(self, dt: float) -> None:
        """Update river animation."""
        for i, (offset, y) in enumerate(self.curve_points):
            new_y = y + SCENERY_SPEED * dt * 60
            if new_y > SCREEN_HEIGHT + 100:
                new_y = -100
                # New curve offset
                offset = random.uniform(-30, 30)
            self.curve_points[i] = (offset, new_y)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the river."""
        # Build river path
        points = []
        for offset, y in self.curve_points:
            points.append((self.x + offset, y))
        
        if len(points) < 2:
            return

        # Draw river with gradient effect
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Wavy width
            wave = math.sin(y1 * 0.02) * 10
            w = self.width + wave
            
            # Draw river segment
            river_surf = pygame.Surface((int(w * 2 + 20), int(abs(y2 - y1) + 10)), pygame.SRCALPHA)
            
            # Gradient from center
            for j in range(int(w), 0, -1):
                alpha = int(180 * (1 - j / w * 0.5))
                color = (COLOR_BLUE[0], COLOR_BLUE[1], COLOR_BLUE[2], alpha)
                pygame.draw.line(river_surf, color,
                               (w + 10, 0),
                               (w + 10 + (j * 0.3), abs(y2 - y1) + 10), j * 2)
            
            surface.blit(river_surf, (x1 - w - 10, min(y1, y2)))


@dataclass
class GrassPatch:
    """A patch of grass detail."""
    x: float
    y: float
    size: float
    rotation: float

    def update(self, dt: float) -> None:
        """Update grass position."""
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size - 30
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.rotation = random.uniform(0, 360)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the grass patch."""
        grass_color = (
            COLOR_GREEN_DARK[0] + random.randint(-10, 10),
            COLOR_GREEN_DARK[1] + random.randint(-10, 10),
            COLOR_GREEN_DARK[2] + random.randint(-10, 10)
        )
        
        # Draw several blades
        for i in range(5):
            angle = math.radians(self.rotation + i * 15)
            length = self.size * (0.5 + random.random() * 0.5)
            end_x = self.x + math.cos(angle) * length
            end_y = self.y + math.sin(angle) * length * 0.5
            
            pygame.draw.line(surface, grass_color,
                           (self.x, self.y),
                           (end_x, end_y), 2)


@dataclass
class SceneryDetail:
    """Generic scenery detail (rocks, flowers, etc)."""
    x: float
    y: float
    detail_type: int  # 0=rock, 1=flower, 2=bush
    size: float
    color: Tuple[int, int, int]

    def update(self, dt: float) -> None:
        """Update position."""
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size - 30
            self.x = random.uniform(0, SCREEN_WIDTH)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the detail."""
        if self.detail_type == 0:  # Rock
            pygame.draw.ellipse(surface, self.color,
                              (self.x - self.size, self.y - self.size * 0.6,
                               self.size * 2, self.size * 1.2))
        elif self.detail_type == 1:  # Flower
            # Stem
            pygame.draw.line(surface, COLOR_GREEN,
                           (self.x, self.y),
                           (self.x, self.y - self.size), 2)
            # Petals
            for i in range(5):
                angle = math.radians(i * 72)
                px = self.x + math.cos(angle) * self.size * 0.4
                py = self.y - self.size + math.sin(angle) * self.size * 0.4
                pygame.draw.circle(surface, self.color, (int(px), int(py)), int(self.size * 0.3))
            # Center
            pygame.draw.circle(surface, COLOR_YELLOW, (int(self.x), int(self.y - self.size)), int(self.size * 0.25))
        else:  # Bush
            for i in range(3):
                offset_x = (i - 1) * self.size * 0.4
                pygame.draw.circle(surface, self.color,
                                 (int(self.x + offset_x), int(self.y - i * self.size * 0.2)),
                                 int(self.size * 0.5))


class Background:
    """Main background manager."""
    
    def __init__(self):
        self.clouds: List[Cloud] = []
        self.trees: List[Tree] = []
        self.rivers: List[River] = []
        self.grass_patches: List[GrassPatch] = []
        self.details: List[SceneryDetail] = []
        self.atmosphere = AtmosphericHaze()
        
        self._generate_background()

    def _generate_background(self) -> None:
        """Generate all background elements."""
        # Generate clouds
        for i in range(CLOUD_COUNT):
            width = random.uniform(60, 150)
            height = random.uniform(30, 60)
            puffs = []
            num_puffs = random.randint(4, 8)
            for j in range(num_puffs):
                px = random.uniform(-width * 0.5, width * 0.5)
                py = random.uniform(-height * 0.3, height * 0.3)
                pr = random.uniform(width * 0.15, width * 0.3)
                puffs.append((px, py, pr))
            
            self.clouds.append(Cloud(
                x=random.uniform(0, SCREEN_WIDTH),
                y=random.uniform(0, SCREEN_HEIGHT),
                width=width,
                height=height,
                speed=random.uniform(0.3, 1.0),
                alpha=random.randint(120, 200),
                puffs=puffs
            ))

        # Generate trees (avoiding river area)
        river_center = SCREEN_WIDTH // 2
        for i in range(TREE_COUNT):
            x = random.uniform(40, SCREEN_WIDTH - 40)
            # Avoid river area
            while river_center - RIVER_WIDTH < x < river_center + RIVER_WIDTH:
                x = random.uniform(40, SCREEN_WIDTH - 40)
            
            self.trees.append(Tree(
                x=x,
                y=random.uniform(0, SCREEN_HEIGHT),
                size=random.uniform(25, 50),
                color_variation=random.randint(-20, 20),
                shadow_offset=random.uniform(3, 8)
            ))

        # Generate river
        self.rivers.append(River(
            x=river_center,
            width=RIVER_WIDTH,
            curve_points=[(random.uniform(-20, 20), y) 
                         for y in range(-50, SCREEN_HEIGHT + 100, 80)],
            speed=0.5
        ))

        # Generate grass patches
        for i in range(40):
            x = random.uniform(0, SCREEN_WIDTH)
            # Avoid river area
            while river_center - RIVER_WIDTH - 10 < x < river_center + RIVER_WIDTH + 10:
                x = random.uniform(0, SCREEN_WIDTH)
            
            self.grass_patches.append(GrassPatch(
                x=x,
                y=random.uniform(0, SCREEN_HEIGHT),
                size=random.uniform(8, 15),
                rotation=random.uniform(0, 360)
            ))

        # Generate scenery details
        for i in range(25):
            x = random.uniform(0, SCREEN_WIDTH)
            while river_center - RIVER_WIDTH - 10 < x < river_center + RIVER_WIDTH + 10:
                x = random.uniform(0, SCREEN_WIDTH)
            
            detail_type = random.randint(0, 2)
            if detail_type == 0:
                color = (COLOR_GRAY[0] + random.randint(-20, 20),
                        COLOR_GRAY[1] + random.randint(-20, 20),
                        COLOR_GRAY[2] + random.randint(-20, 20))
            elif detail_type == 1:
                color = random.choice([
                    (255, 100, 100), (255, 150, 200), (200, 100, 255),
                    (255, 200, 100), (100, 200, 255)
                ])
            else:
                color = (COLOR_GREEN_DARK[0] + random.randint(-20, 20),
                        COLOR_GREEN_DARK[1] + random.randint(-20, 20),
                        COLOR_GREEN_DARK[2] + random.randint(-20, 20))
            
            self.details.append(SceneryDetail(
                x=x,
                y=random.uniform(0, SCREEN_HEIGHT),
                detail_type=detail_type,
                size=random.uniform(5, 12),
                color=color
            ))

    def update(self, dt: float) -> None:
        """Update all background elements."""
        for cloud in self.clouds:
            cloud.update(dt)
        for tree in self.trees:
            tree.update(dt)
        for river in self.rivers:
            river.update(dt)
        for grass in self.grass_patches:
            grass.update(dt)
        for detail in self.details:
            detail.update(dt)
        self.atmosphere.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the entire background."""
        # Draw ground base
        pygame.draw.rect(surface, (50, 150, 60), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw ground texture (darker patches)
        for i in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            w = random.randint(50, 150)
            h = random.randint(30, 80)
            color = (40, 130, 50)
            pygame.draw.ellipse(surface, color, (x, y, w, h))

        # Draw rivers (behind trees)
        for river in self.rivers:
            river.draw(surface)

        # Draw grass patches
        for grass in self.grass_patches:
            grass.draw(surface)

        # Draw details
        for detail in self.details:
            detail.draw(surface)

        # Draw trees
        for tree in self.trees:
            tree.draw(surface)

        # Draw atmospheric haze
        self.atmosphere.draw(surface)

        # Draw clouds (on top)
        for cloud in self.clouds:
            cloud.draw(surface)
