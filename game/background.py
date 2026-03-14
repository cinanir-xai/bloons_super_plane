"""Background rendering for the game - Top-down view with winding river and scenery."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCENERY_SPEED,
    CLOUD_COUNT, TREE_COUNT, RIVER_WIDTH,
    COLOR_BG_GRASS, COLOR_BG_RIVER, COLOR_WHITE, COLOR_GREEN,
    COLOR_BG_SAND, COLOR_YELLOW, COLOR_BLACK
)

@dataclass
class PuffyCloud:
    """A puffy cloud made of multiple circles."""
    x: float
    y: float
    scale: float
    speed: float
    bubbles: List[Tuple[float, float, float]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.bubbles:
            # Generate random bubble positions for the cloud
            num_bubbles = random.randint(4, 7)
            for _ in range(num_bubbles):
                bx = random.uniform(-20, 20) * self.scale
                by = random.uniform(-10, 10) * self.scale
                br = random.uniform(15, 30) * self.scale
                self.bubbles.append((bx, by, br))

    def update(self, dt: float) -> None:
        self.y += self.speed * dt * 60
        if self.y > SCREEN_HEIGHT + 50:
            self.y = -50
            self.x = random.randint(50, SCREEN_WIDTH - 50)
            self.bubbles = []
            self.__post_init__()

    def draw(self, surface: pygame.Surface) -> None:
        # Draw puffy cloud with multiple overlapping circles
        for bx, by, br in self.bubbles:
            px = self.x + bx
            py = self.y + by
            # Main white circle
            pygame.draw.circle(surface, COLOR_WHITE, (int(px), int(py)), int(br))
            # Slight shading on bottom
            pygame.draw.circle(surface, (220, 220, 220), (int(px), int(py + br * 0.3)), int(br * 0.6))

@dataclass
class TreeSprite:
    """Varied tree sprites for visual diversity."""
    x: float
    y: float
    tree_type: int  # 0-3 for different tree styles
    size: float
    color_variant: Tuple[int, int, int]

    def update(self, dt: float) -> None:
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size
            self.x = self._get_valid_x()

    def _get_valid_x(self) -> int:
        """Get valid x position (not on river)."""
        while True:
            x = random.randint(30, SCREEN_WIDTH - 30)
            # Avoid river area (center third)
            if x < SCREEN_WIDTH // 3 - 30 or x > SCREEN_WIDTH * 2 // 3 + 30:
                return x

    def draw(self, surface: pygame.Surface) -> None:
        if self.tree_type == 0:
            self._draw_pine(surface)
        elif self.tree_type == 1:
            self._draw_oak(surface)
        elif self.tree_type == 2:
            self._draw_palm(surface)
        else:
            self._draw_bush(surface)

    def _draw_pine(self, surface: pygame.Surface):
        # Pine tree - triangular layers
        cx, cy = int(self.x), int(self.y)
        # Trunk
        pygame.draw.rect(surface, (100, 60, 30), (cx - 4, cy, 8, int(self.size * 0.4)))
        # Layers of triangles
        for i in range(3):
            offset = i * self.size * 0.25
            w = self.size * (0.8 - i * 0.15)
            h = self.size * 0.4
            points = [
                (cx, cy - offset - h),
                (cx - w//2, cy - offset),
                (cx + w//2, cy - offset)
            ]
            pygame.draw.polygon(surface, self.color_variant, points)
            pygame.draw.polygon(surface, COLOR_BLACK, points, 1)

    def _draw_oak(self, surface: pygame.Surface):
        # Oak tree - rounded canopy
        cx, cy = int(self.x), int(self.y)
        # Trunk
        pygame.draw.rect(surface, (80, 50, 20), (cx - 5, cy, 10, int(self.size * 0.5)))
        # Canopy (multiple circles)
        for i in range(5):
            angle = i * (2 * math.pi / 5)
            ox = math.cos(angle) * self.size * 0.2
            oy = math.sin(angle) * self.size * 0.15 - self.size * 0.3
            pygame.draw.circle(surface, self.color_variant, (int(cx + ox), int(cy + oy)), int(self.size * 0.25))
        # Center
        pygame.draw.circle(surface, self.color_variant, (cx, cy - int(self.size * 0.35)), int(self.size * 0.3))
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy - int(self.size * 0.35)), int(self.size * 0.3), 1)

    def _draw_palm(self, surface: pygame.Surface):
        # Palm tree - thin trunk with fronds
        cx, cy = int(self.x), int(self.y)
        # Trunk (curved)
        for i in range(int(self.size * 0.6)):
            offset = math.sin(i * 0.2) * 3
            pygame.draw.rect(surface, (100, 70, 40), (cx + int(offset) - 3, cy + i, 6, 2))
        # Fronds
        frond_color = (40, 180, 60)
        for angle_deg in [-60, -30, 0, 30, 60]:
            angle = math.radians(angle_deg)
            fx = cx + math.cos(angle) * self.size * 0.4
            fy = cy - self.size * 0.6 + math.sin(angle) * self.size * 0.3
            pygame.draw.line(surface, frond_color, (cx, cy - self.size * 0.6), (fx, fy), 3)
            pygame.draw.circle(surface, frond_color, (int(fx), int(fy)), 4)

    def _draw_bush(self, surface: pygame.Surface):
        # Bush - low shrub
        cx, cy = int(self.x), int(self.y)
        # Multiple overlapping circles for bushy look
        for i in range(4):
            ox = random.uniform(-self.size * 0.2, self.size * 0.2)
            oy = random.uniform(-self.size * 0.1, self.size * 0.1)
            r = self.size * random.uniform(0.15, 0.25)
            pygame.draw.circle(surface, self.color_variant, (int(cx + ox), int(cy - self.size * 0.3 + oy)), int(r))
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy - int(self.size * 0.3)), int(self.size * 0.25), 1)

@dataclass
class GrassPatch:
    """Small grass/farmland patches for visual detail."""
    x: float
    y: float
    patch_type: int  # 0=grass, 1=farmland, 2=flowers
    size: float

    def update(self, dt: float) -> None:
        self.y += SCENERY_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size
            self.x = self._get_valid_x()

    def _get_valid_x(self) -> int:
        while True:
            x = random.randint(20, SCREEN_WIDTH - 20)
            if x < SCREEN_WIDTH // 3 - 20 or x > SCREEN_WIDTH * 2 // 3 + 20:
                return x

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        if self.patch_type == 0:
            # Grass patch
            for i in range(6):
                gx = cx + random.uniform(-self.size/2, self.size/2)
                gy = cy + random.uniform(-self.size/2, self.size/2)
                pygame.draw.circle(surface, (50, 180, 50), (int(gx), int(gy)), random.randint(3, 6))
        elif self.patch_type == 1:
            # Farmland rows
            pygame.draw.rect(surface, (139, 90, 43), (cx - self.size/2, cy - self.size/2, self.size, self.size))
            # Row lines
            for i in range(3):
                pygame.draw.line(surface, (100, 70, 30), 
                               (cx - self.size/2, cy - self.size/2 + i * self.size/3),
                               (cx + self.size/2, cy - self.size/2 + i * self.size/3), 2)
        else:
            # Flower patch
            pygame.draw.circle(surface, (60, 200, 60), (cx, cy), int(self.size/2))
            for i in range(5):
                angle = i * (2 * math.pi / 5)
                fx = cx + math.cos(angle) * self.size * 0.3
                fy = cy + math.sin(angle) * self.size * 0.3
                pygame.draw.circle(surface, random.choice([(255, 100, 150), (255, 255, 100), (255, 150, 50)]), 
                                 (int(fx), int(fy)), 4)

class Background:
    """Main background manager with top-down scenery."""
    
    def __init__(self):
        self.clouds: List[PuffyCloud] = []
        self.trees: List[TreeSprite] = []
        self.grass_patches: List[GrassPatch] = []
        self.river_points: List[Tuple[float, float]] = []
        
        self._generate_background()

    def _generate_background(self) -> None:
        # Generate winding river points
        self.river_points = []
        num_points = 20
        for i in range(num_points):
            y = (SCREEN_HEIGHT / num_points) * i
            # Winding pattern
            offset = math.sin(i * 0.5) * 80 + math.sin(i * 0.3) * 40
            x = SCREEN_WIDTH // 2 + offset
            self.river_points.append((x, y))
        
        # Clouds
        for _ in range(CLOUD_COUNT):
            self.clouds.append(PuffyCloud(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(-100, SCREEN_HEIGHT),
                scale=random.uniform(0.8, 1.5),
                speed=random.uniform(0.3, 0.8)
            ))
        
        # Trees on both sides
        for _ in range(TREE_COUNT):
            x = random.randint(30, SCREEN_WIDTH - 30)
            # Keep away from center river area
            if SCREEN_WIDTH // 3 - 20 < x < SCREEN_WIDTH * 2 // 3 + 20:
                x = random.choice([random.randint(30, SCREEN_WIDTH//3 - 30), 
                                  random.randint(SCREEN_WIDTH * 2//3 + 30, SCREEN_WIDTH - 30)])
            
            tree_type = random.randint(0, 3)
            colors = [(34, 139, 34), (40, 160, 40), (30, 120, 30), (45, 180, 45)]
            self.trees.append(TreeSprite(
                x=x, y=random.randint(0, SCREEN_HEIGHT),
                tree_type=tree_type,
                size=random.uniform(30, 50),
                color_variant=colors[tree_type]
            ))
        
        # Grass/farmland patches
        for _ in range(15):
            x = random.randint(20, SCREEN_WIDTH - 20)
            if SCREEN_WIDTH // 3 < x < SCREEN_WIDTH * 2 // 3:
                x = random.choice([random.randint(20, SCREEN_WIDTH//3 - 10),
                                  random.randint(SCREEN_WIDTH * 2//3 + 10, SCREEN_WIDTH - 20)])
            self.grass_patches.append(GrassPatch(
                x=x, y=random.randint(0, SCREEN_HEIGHT),
                patch_type=random.randint(0, 2),
                size=random.uniform(20, 35)
            ))

    def update(self, dt: float) -> None:
        for cloud in self.clouds:
            cloud.update(dt)
        for tree in self.trees:
            tree.update(dt)
        for patch in self.grass_patches:
            patch.update(dt)
        
        # Scroll river points
        for i, (x, y) in enumerate(self.river_points):
            new_y = y + SCENERY_SPEED * dt * 60
            if new_y > SCREEN_HEIGHT:
                new_y = -20
                # Re-generate x position at top
                idx = self.river_points.index((x, y))
                if idx > 0:
                    prev_x = self.river_points[idx-1][0]
                    x = prev_x + random.uniform(-20, 20)
                else:
                    x = SCREEN_WIDTH // 2
            self.river_points[i] = (x, new_y)

    def draw(self, surface: pygame.Surface) -> None:
        # 1. Base grass background (top-down view - solid green field)
        surface.fill(COLOR_BG_GRASS)
        
        # 2. Draw winding river
        self._draw_winding_river(surface)
        
        # 3. Draw grass patches and farmland
        for patch in self.grass_patches:
            patch.draw(surface)
        
        # 4. Draw trees
        for tree in self.trees:
            tree.draw(surface)
        
        # 5. Draw clouds (behind player conceptually, but drawn on top for visibility)
        for cloud in self.clouds:
            cloud.draw(surface)

    def _draw_winding_river(self, surface: pygame.Surface) -> None:
        """Draw a winding river with banks."""
        if len(self.river_points) < 2:
            return
        
        # Draw river path
        river_width = RIVER_WIDTH
        bank_width = 15
        
        # Create polygon for river
        left_points = []
        right_points = []
        
        for i, (x, y) in enumerate(self.river_points):
            # Smooth the x position
            if i > 0 and i < len(self.river_points) - 1:
                smooth_x = (self.river_points[i-1][0] + x + self.river_points[i+1][0]) / 3
            else:
                smooth_x = x
            
            left_points.append((smooth_x - river_width//2, y))
            right_points.append((smooth_x + river_width//2, y))
        
        # Draw sand banks
        for i in range(len(left_points) - 1):
            # Left bank
            pygame.draw.polygon(surface, COLOR_BG_SAND, [
                left_points[i], left_points[i+1],
                (left_points[i+1][0] - bank_width, left_points[i+1][1]),
                (left_points[i][0] - bank_width, left_points[i][1])
            ])
            # Right bank
            pygame.draw.polygon(surface, COLOR_BG_SAND, [
                right_points[i], right_points[i+1],
                (right_points[i+1][0] + bank_width, right_points[i+1][1]),
                (right_points[i][0] + bank_width, right_points[i][1])
            ])
        
        # Draw river itself
        for i in range(len(left_points) - 1):
            pygame.draw.polygon(surface, COLOR_BG_RIVER, [
                left_points[i], left_points[i+1],
                right_points[i+1], right_points[i]
            ])
        
        # Draw river shimmer lines
        for i in range(0, len(self.river_points), 3):
            if i < len(self.river_points):
                x, y = self.river_points[i]
                pygame.draw.line(surface, (100, 200, 255), 
                               (x - river_width//3, y), (x + river_width//3, y), 2)
