"""Background rendering for the game - Clean top-down view with layered scenery."""

import pygame
import math
import random
from typing import List, Tuple
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCENERY_SPEED,
    RIVER_WIDTH, COLOR_BG_GRASS, COLOR_BG_RIVER, COLOR_WHITE,
    COLOR_GREEN, COLOR_BG_SAND, COLOR_BLACK
)

# Ground layer speed (all ground items move at same speed)
GROUND_SPEED = SCENERY_SPEED
# Cloud layer speed (slower, all same)
CLOUD_SPEED = 0.5


@dataclass
class Cloud:
    """Simple puffy cloud."""
    x: float
    y: float
    size: float

    def update(self, dt: float) -> None:
        self.y += CLOUD_SPEED * dt * 60
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size - 20
            self.x = random.randint(int(self.size), int(SCREEN_WIDTH - self.size))

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        s = int(self.size)
        # Puffy cloud - multiple overlapping circles
        pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), s)
        pygame.draw.circle(surface, COLOR_WHITE, (cx - s//2, cy + s//4), s * 2//3)
        pygame.draw.circle(surface, COLOR_WHITE, (cx + s//2, cy + s//4), s * 2//3)
        pygame.draw.circle(surface, COLOR_WHITE, (cx, cy - s//3), s * 2//3)
        pygame.draw.circle(surface, (230, 230, 230), (cx, cy + s//4), s//2)


@dataclass
class RiverSegment:
    """A segment of the winding river."""
    x: float
    y: float
    width: float

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + 50

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        w = self.width
        h = 32
        
        # Draw sand banks
        bank_w = 14
        pygame.draw.rect(surface, COLOR_BG_SAND, (cx - w//2 - bank_w, cy - h//2, bank_w, h + 4))
        pygame.draw.rect(surface, COLOR_BG_SAND, (cx + w//2, cy - h//2, bank_w, h + 4))
        
        # Draw river
        pygame.draw.rect(surface, COLOR_BG_RIVER, (cx - w//2, cy - h//2, w, h + 4))


@dataclass
class Tree:
    """Simple tree sprite."""
    x: float
    y: float
    tree_type: int  # 0=pine, 1=oak, 2=bush
    size: float

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + self.size + 10

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        s = int(self.size)
        
        if self.tree_type == 0:  # Pine
            # Trunk
            pygame.draw.rect(surface, (100, 60, 30), (cx - 4, cy, 8, s//3))
            # Triangles
            for i in range(3):
                offset = i * s//4
                w = s * (0.6 - i * 0.1)
                h = s//3
                pygame.draw.polygon(surface, (30, 120, 30), [
                    (cx, cy - offset - h),
                    (cx - w//2, cy - offset),
                    (cx + w//2, cy - offset)
                ])
                pygame.draw.polygon(surface, COLOR_BLACK, [
                    (cx, cy - offset - h),
                    (cx - w//2, cy - offset),
                    (cx + w//2, cy - offset)
                ], 1)
                
        elif self.tree_type == 1:  # Oak
            # Trunk
            pygame.draw.rect(surface, (80, 50, 20), (cx - 5, cy, 10, s//2))
            # Canopy (multiple circles)
            pygame.draw.circle(surface, (40, 140, 40), (cx, cy - s//3), s//2)
            pygame.draw.circle(surface, (30, 120, 30), (cx - s//4, cy - s//4), s//3)
            pygame.draw.circle(surface, (50, 150, 50), (cx + s//4, cy - s//4), s//3)
            pygame.draw.circle(surface, COLOR_BLACK, (cx, cy - s//3), s//2, 1)
            
        else:  # Bush
            pygame.draw.circle(surface, (60, 160, 60), (cx, cy - s//4), s//3)
            pygame.draw.circle(surface, (50, 150, 50), (cx - s//4, cy - s//6), s//4)
            pygame.draw.circle(surface, (70, 170, 70), (cx + s//4, cy - s//6), s//4)
            pygame.draw.circle(surface, COLOR_BLACK, (cx, cy - s//4), s//3, 1)


@dataclass
class Forest:
    """Cluster of trees (forest)."""
    x: float
    y: float
    size: float
    trees: List[Tuple[float, float, int]]

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + self.size

    def draw(self, surface: pygame.Surface) -> None:
        for ox, oy, ttype in self.trees:
            tree = Tree(self.x + ox, self.y + oy, ttype, 30)
            tree.draw(surface)


@dataclass
class Farmland:
    """Farmland with rows."""
    x: float
    y: float
    size: float

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + self.size

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        s = int(self.size)
        
        # Brown rectangle
        pygame.draw.rect(surface, (139, 90, 43), (cx - s//2, cy - s//2, s, s))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - s//2, cy - s//2, s, s), 2)
        
        # Rows
        for i in range(4):
            row_y = cy - s//2 + 8 + i * (s//4)
            pygame.draw.line(surface, (100, 70, 30), (cx - s//2 + 4, row_y), (cx + s//2 - 4, row_y), 2)


@dataclass
class FlowerPatch:
    """Patch of flowers."""
    x: float
    y: float
    size: float
    flower_colors: List[Tuple[int, int, int]] = field(default_factory=list)

    def __post_init__(self):
        if not self.flower_colors:
            base_colors = [(255, 100, 150), (255, 255, 100), (200, 100, 255), (255, 150, 50)]
            self.flower_colors = [random.choice(base_colors) for _ in range(6)]

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + self.size

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        s = int(self.size)
        
        # Green base
        pygame.draw.circle(surface, (60, 180, 60), (cx, cy), s//2)
        
        # Flowers (fixed colors per patch)
        for i in range(6):
            angle = i * (2 * math.pi / 6)
            fx = cx + math.cos(angle) * s * 0.25
            fy = cy + math.sin(angle) * s * 0.25
            pygame.draw.circle(surface, self.flower_colors[i], (int(fx), int(fy)), 4)
            pygame.draw.circle(surface, (255, 255, 200), (int(fx), int(fy)), 2)


@dataclass
class House:
    """Simple house sprite."""
    x: float
    y: float
    size: float
    color: Tuple[int, int, int]

    def update(self, dt: float) -> None:
        self.y += GROUND_SPEED * dt * 60

    def is_off_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT + self.size

    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        s = int(self.size)
        
        # Body
        pygame.draw.rect(surface, self.color, (cx - s//2, cy - s//4, s, s//2))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - s//2, cy - s//4, s, s//2), 2)
        
        # Roof
        pygame.draw.polygon(surface, (150, 50, 50), [
            (cx, cy - s//2 - s//4),
            (cx - s//2 - 5, cy - s//4),
            (cx + s//2 + 5, cy - s//4)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx, cy - s//2 - s//4),
            (cx - s//2 - 5, cy - s//4),
            (cx + s//2 + 5, cy - s//4)
        ], 2)
        
        # Door
        pygame.draw.rect(surface, (80, 40, 20), (cx - 5, cy, 10, s//4))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 5, cy, 10, s//4), 1)
        
        # Windows
        pygame.draw.rect(surface, (200, 220, 255), (cx - s//3, cy - s//8, 8, 8))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - s//3, cy - s//8, 8, 8), 1)
        pygame.draw.rect(surface, (200, 220, 255), (cx + s//3 - 8, cy - s//8, 8, 8))
        pygame.draw.rect(surface, COLOR_BLACK, (cx + s//3 - 8, cy - s//8, 8, 8), 1)


class Background:
    """Main background manager with clean layered scenery."""
    
    def __init__(self):
        self.clouds: List[Cloud] = []
        self.river_segments: List[RiverSegment] = []
        self.ground_items: List = []
        
        self._generate_background()

    def _generate_background(self) -> None:
        # Generate clouds (all same speed)
        for _ in range(8):
            self.clouds.append(Cloud(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(-100, SCREEN_HEIGHT),
                size=random.uniform(25, 45)
            ))
        
        # Generate river segments (many for smooth winding)
        num_segments = 80
        segment_h = 25
        for i in range(num_segments):
            y = i * segment_h - segment_h * 3  # Start above screen
            offset = math.sin(i * 0.4) * 60 + math.sin(i * 0.2) * 30
            x = SCREEN_WIDTH // 2 + offset
            self.river_segments.append(RiverSegment(x=x, y=y, width=RIVER_WIDTH))
        
        # Generate ground items on both sides
        self._generate_ground_items()

    def _generate_ground_items(self) -> None:
        """Generate ground layer items."""
        self.ground_items = []
        
        # Helper to ensure items stay out of river area
        def get_safe_x(base_x: float, spread: float) -> float:
            while True:
                x = base_x + random.uniform(-spread, spread)
                # Keep items away from river center band
                if x < SCREEN_WIDTH // 2 - RIVER_WIDTH // 2 - 40 or x > SCREEN_WIDTH // 2 + RIVER_WIDTH // 2 + 40:
                    return x
        
        for side in [-1, 1]:  # Left and right of river
            base_x = SCREEN_WIDTH // 4 if side == -1 else SCREEN_WIDTH * 3 // 4
            
            # Trees
            for _ in range(18):
                x = get_safe_x(base_x, SCREEN_WIDTH // 6)
                y = random.uniform(-300, SCREEN_HEIGHT + 300)
                tree_type = random.randint(0, 2)
                size = random.uniform(35, 55)
                self.ground_items.append(Tree(x, y, tree_type, size))
            
            # Forests
            for _ in range(4):
                x = get_safe_x(base_x, SCREEN_WIDTH // 8)
                y = random.uniform(-300, SCREEN_HEIGHT + 300)
                forest = Forest(x, y, 80, [])
                for _ in range(10):
                    ox = random.uniform(-45, 45)
                    oy = random.uniform(-45, 45)
                    ttype = random.randint(0, 1)
                    forest.trees.append((ox, oy, ttype))
                self.ground_items.append(forest)
            
            # Farmland
            for _ in range(5):
                x = get_safe_x(base_x, SCREEN_WIDTH // 8)
                y = random.uniform(-300, SCREEN_HEIGHT + 300)
                self.ground_items.append(Farmland(x, y, random.uniform(40, 60)))
            
            # Flower patches
            for _ in range(6):
                x = get_safe_x(base_x, SCREEN_WIDTH // 8)
                y = random.uniform(-300, SCREEN_HEIGHT + 300)
                self.ground_items.append(FlowerPatch(x, y, random.uniform(25, 40)))
            
            # Houses
            for _ in range(3):
                x = get_safe_x(base_x, SCREEN_WIDTH // 10)
                y = random.uniform(-300, SCREEN_HEIGHT + 300)
                colors = [(200, 180, 160), (180, 160, 140), (220, 200, 180)]
                self.ground_items.append(House(x, y, random.uniform(35, 50), random.choice(colors)))

    def update(self, dt: float) -> None:
        # Update clouds
        for cloud in self.clouds:
            cloud.update(dt)
        
        # Update river segments
        for seg in self.river_segments:
            seg.update(dt)
        
        # Recycle river segments (despawn only when completely off screen)
        for seg in self.river_segments:
            if seg.y > SCREEN_HEIGHT + 60:
                # Find highest segment and continue from there
                min_y = min(s.y for s in self.river_segments)
                seg.y = min_y - 25
                # Continue winding
                idx = self.river_segments.index(seg)
                if idx > 0:
                    prev = self.river_segments[idx - 1]
                    seg.x = prev.x + random.uniform(-12, 12)
                else:
                    seg.x = SCREEN_WIDTH // 2
        
        # Update ground items
        for item in self.ground_items:
            item.update(dt)
        
        # Recycle ground items (despawn only when completely off screen)
        for item in self.ground_items:
            if item.is_off_screen():
                item.y = random.uniform(-400, -150)
                # Keep on correct side and out of river
                if item.x < SCREEN_WIDTH // 2:
                    item.x = random.uniform(20, SCREEN_WIDTH//2 - RIVER_WIDTH//2 - 40)
                else:
                    item.x = random.uniform(SCREEN_WIDTH//2 + RIVER_WIDTH//2 + 40, SCREEN_WIDTH - 20)

    def draw(self, surface: pygame.Surface) -> None:
        # 1. Solid green background
        surface.fill(COLOR_BG_GRASS)
        
        # 2. Draw river (behind everything)
        self._draw_river(surface)
        
        # 3. Draw ground items (sorted by y for depth)
        sorted_items = self._get_sorted_ground_items()
        for item in sorted_items:
            item.draw(surface)
        
        # 4. Draw clouds (on top layer)
        for cloud in self.clouds:
            cloud.draw(surface)

    def _get_sorted_ground_items(self) -> List:
        """Get ground items sorted by y with caching for performance."""
        if not hasattr(self, "_sorted_items_cache"):
            self._sorted_items_cache = []
            self._sort_timer = 0
        self._sort_timer += 1
        if self._sort_timer % 5 == 0 or not self._sorted_items_cache:
            self._sorted_items_cache = sorted(self.ground_items, key=lambda i: i.y)
        return self._sorted_items_cache

    def _draw_river(self, surface: pygame.Surface) -> None:
        """Draw connected river segments."""
        if len(self.river_segments) < 2:
            return
        
        sorted_segs = sorted(self.river_segments, key=lambda s: s.y)
        
        for i, seg in enumerate(sorted_segs):
            if seg.y > -60 and seg.y < SCREEN_HEIGHT + 60:
                cx, cy = int(seg.x), int(seg.y)
                w = seg.width
                h = 32
                
                # Draw sand banks
                bank_w = 14
                pygame.draw.rect(surface, COLOR_BG_SAND, (cx - w//2 - bank_w, cy - h//2, bank_w, h + 4))
                pygame.draw.rect(surface, COLOR_BG_SAND, (cx + w//2, cy - h//2, bank_w, h + 4))
                
                # Draw river
                pygame.draw.rect(surface, COLOR_BG_RIVER, (cx - w//2, cy - h//2, w, h + 4))
        
        # Shimmer lines
        for seg in sorted_segs:
            if seg.y > -60 and seg.y < SCREEN_HEIGHT + 60:
                pygame.draw.line(surface, (100, 200, 255),
                               (seg.x - seg.width//4, seg.y),
                               (seg.x + seg.width//4, seg.y), 1)
