"""Enemy/Balloon classes for the game - BTD-style progression."""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALLOON_SPEED,
    BALLOON_BASE_RADIUS,
    COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_PINK,
    COLOR_WHITE, COLOR_BLACK, PARTICLE_SIZE,
    ORB_LUCK_BASE_CHANCE, ORB_LUCK_CHANCE_PER_LEVEL
)
from .effects import ParticleSystem

from .orbs import OrbManager

# Balloon color progression: Pink (tier 0, largest) -> Yellow -> Green -> Blue -> Red (tier 4, smallest)
BALLOON_COLORS = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]

# Special balloon types (BTD-inspired)
BALLOON_TYPE_NORMAL = "normal"
BALLOON_TYPE_BLACK = "black"      # Immune to explosive (missiles)
BALLOON_TYPE_WHITE = "white"      # Immune to ice (future)
BALLOON_TYPE_LEAD = "lead"        # Immune to physical (darts, boomerang, wingman)
BALLOON_TYPE_ZEBRA = "zebra"      # Immune to explosive AND ice
BALLOON_TYPE_RAINBOW = "rainbow"  # No immunities
BALLOON_TYPE_CERAMIC = "ceramic"  # 10 HP, spawns 2 rainbow

# Special balloon colors (BTD-style)
COLOR_BLACK_BALLOON = (30, 30, 30)
COLOR_WHITE_BALLOON = (245, 245, 245)
COLOR_LEAD_BALLOON = (100, 100, 110)
COLOR_ZEBRA_BALLOON = (240, 240, 240)  # Base white with black stripes
COLOR_CERAMIC_BALLOON = (180, 140, 100)  # Tan/brown ceramic

# Rainbow colors for rainbow balloon
RAINBOW_COLORS = [
    (255, 80, 80),    # Red
    (255, 165, 50),   # Orange
    (255, 230, 50),   # Yellow
    (80, 220, 80),    # Green
    (80, 150, 255),   # Blue
    (180, 100, 255),  # Purple
]

# Size scaling tiers (each step is 5% larger than previous)
# From smallest to largest: Red -> Blue -> Green -> Yellow -> Pink -> Black/White -> Lead/Zebra -> Rainbow -> Ceramic
SIZE_TIER_RED = 0
SIZE_TIER_BLUE = 1
SIZE_TIER_GREEN = 2
SIZE_TIER_YELLOW = 3
SIZE_TIER_PINK = 4
SIZE_TIER_BLACK_WHITE = 5
SIZE_TIER_LEAD_ZEBRA = 6
SIZE_TIER_RAINBOW = 7
SIZE_TIER_CERAMIC = 8

def get_balloon_radius(tier: int) -> float:
    """Calculate radius for a tier. Red (4) is base, each tier up +5%."""
    # tiers: 0=pink, 1=yellow, 2=green, 3=blue, 4=red
    steps_above_red = 4 - tier
    return BALLOON_BASE_RADIUS * (1.05 ** steps_above_red)

def get_balloon_radius_by_type(balloon_type: str) -> float:
    """Get radius for special balloon types based on size tier."""
    size_multipliers = {
        BALLOON_TYPE_NORMAL: 0,  # Uses tier-based sizing
        BALLOON_TYPE_BLACK: SIZE_TIER_BLACK_WHITE,
        BALLOON_TYPE_WHITE: SIZE_TIER_BLACK_WHITE,
        BALLOON_TYPE_LEAD: SIZE_TIER_LEAD_ZEBRA,
        BALLOON_TYPE_ZEBRA: SIZE_TIER_LEAD_ZEBRA,
        BALLOON_TYPE_RAINBOW: SIZE_TIER_RAINBOW,
        BALLOON_TYPE_CERAMIC: SIZE_TIER_CERAMIC,
    }
    tier = size_multipliers.get(balloon_type, 0)
    return BALLOON_BASE_RADIUS * (1.05 ** tier)

@dataclass
class Balloon:
    """A balloon enemy with color progression and special types."""
    x: float
    y: float
    tier: int  # 0=pink (largest), 4=red (smallest), 5+=popped
    speed: float
    radius: float = 0.0
    color: Tuple[int, int, int] = (0,0,0)
    popped: bool = False
    pop_animation: float = 0.0
    # Movement pattern support
    speed_multiplier: float = 1.0
    pattern: str = "vertical"  # vertical, zigzag, circular, spiral, wave, drift
    pattern_data: dict = field(default_factory=dict)
    base_x: float = 0.0  # Original x position for patterns
    base_y: float = 0.0  # Original y position for patterns
    time_alive: float = 0.0
    has_entered_screen: bool = False
    # Special balloon type (BTD-inspired)
    balloon_type: str = BALLOON_TYPE_NORMAL
    # HP for ceramic balloons
    hp: int = 1
    max_hp: int = 1

    def __post_init__(self):
        # Set radius based on balloon type
        if self.balloon_type == BALLOON_TYPE_NORMAL:
            self.radius = get_balloon_radius(self.tier)
        else:
            self.radius = get_balloon_radius_by_type(self.balloon_type)

        # Set HP for ceramic
        if self.balloon_type == BALLOON_TYPE_CERAMIC:
            self.hp = 10
            self.max_hp = 10

        self.color = self._get_display_color()
        self.base_x = self.x
        self.base_y = self.y
        # Initialize pattern data
        if not self.pattern_data:
            self.pattern_data = {
                'amplitude': random.uniform(20, 60),  # For zigzag/wave
                'frequency': random.uniform(0.02, 0.05),  # For zigzag/wave/circular
                'phase': random.uniform(0, 2 * math.pi),  # For circular/spiral
                'radius': random.uniform(30, 80),  # For circular
            }

    def _get_display_color(self) -> Tuple[int, int, int]:
        """Get the color to display based on balloon type and tier."""
        if self.balloon_type == BALLOON_TYPE_BLACK:
            return COLOR_BLACK_BALLOON
        elif self.balloon_type == BALLOON_TYPE_WHITE:
            return COLOR_WHITE_BALLOON
        elif self.balloon_type == BALLOON_TYPE_LEAD:
            return COLOR_LEAD_BALLOON
        elif self.balloon_type == BALLOON_TYPE_ZEBRA:
            return COLOR_ZEBRA_BALLOON
        elif self.balloon_type == BALLOON_TYPE_RAINBOW:
            return RAINBOW_COLORS[0]  # Default to red for rainbow
        elif self.balloon_type == BALLOON_TYPE_CERAMIC:
            return COLOR_CERAMIC_BALLOON
        elif 0 <= self.tier < len(BALLOON_COLORS):
            return BALLOON_COLORS[self.tier]
        return COLOR_PINK

    def is_immune_to(self, damage_type: str) -> bool:
        """Check if this balloon is immune to a specific damage type."""
        if damage_type == "explosive":
            if self.balloon_type in (BALLOON_TYPE_BLACK, BALLOON_TYPE_ZEBRA):
                return True
        if damage_type == "ice":
            if self.balloon_type in (BALLOON_TYPE_WHITE, BALLOON_TYPE_ZEBRA):
                return True
        if damage_type == "physical" and self.balloon_type == BALLOON_TYPE_LEAD:
            return True
        return False

    def get_children_on_immune_pop(self) -> List['Balloon']:
        """Get child balloons that spawn when this balloon is hit by immune damage."""
        children: List['Balloon'] = []
        if self.balloon_type == BALLOON_TYPE_BLACK or self.balloon_type == BALLOON_TYPE_WHITE:
            # Black/white balloons spawn 2 pink balloons when "hit" by immune
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=0,  # Pink (largest)
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_NORMAL,
                )
                children.append(child)
        elif self.balloon_type == BALLOON_TYPE_LEAD:
            # Lead balloons spawn 2 black balloons when "hit" by immune
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=4,  # Red (smallest) - but we want black, so we use special handling
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_BLACK,
                )
                children.append(child)
        return children

    def take_damage(self) -> bool:
        """Take damage and downgrade. Returns True if should be removed."""
        # Ceramic balloons have HP
        if self.balloon_type == BALLOON_TYPE_CERAMIC:
            self.hp -= 1
            if self.hp <= 0:
                self.popped = True
                return True
            return False

        # Normal balloons downgrade by tier
        self.tier += 1
        if self.tier >= len(BALLOON_COLORS):
            self.popped = True
            return True
        self.radius = get_balloon_radius(self.tier)
        self.color = self._get_display_color()
        return False

    def spawn_children_on_pop(self, balloon_manager) -> None:
        """Spawn child balloons when this balloon is fully popped."""
        if self.balloon_type == BALLOON_TYPE_BLACK or self.balloon_type == BALLOON_TYPE_WHITE:
            # Spawn 2 pink balloons
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=0,
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_NORMAL,
                )
                balloon_manager.balloons.append(child)
        elif self.balloon_type == BALLOON_TYPE_LEAD:
            # Spawn 2 black balloons
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=4,
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_BLACK,
                )
                balloon_manager.balloons.append(child)
        elif self.balloon_type == BALLOON_TYPE_ZEBRA:
            # Spawn 1 white + 1 black balloon
            for i, btype in enumerate([BALLOON_TYPE_WHITE, BALLOON_TYPE_BLACK]):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=4,
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=btype,
                )
                balloon_manager.balloons.append(child)
        elif self.balloon_type == BALLOON_TYPE_RAINBOW:
            # Spawn 2 zebra balloons
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=4,
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_ZEBRA,
                )
                balloon_manager.balloons.append(child)
        elif self.balloon_type == BALLOON_TYPE_CERAMIC:
            # Spawn 2 rainbow balloons
            for i in range(2):
                offset = -25 + i * 50
                child = Balloon(
                    x=self.x + offset,
                    y=self.y,
                    tier=4,
                    speed=self.speed,
                    speed_multiplier=self.speed_multiplier,
                    pattern=self.pattern,
                    pattern_data=dict(self.pattern_data) if self.pattern_data else {},
                    balloon_type=BALLOON_TYPE_RAINBOW,
                )
                balloon_manager.balloons.append(child)

    def update(self, dt: float) -> bool:
        """Update balloon position. Returns False if off screen."""
        if self.popped:
            self.pop_animation += dt * 60
            return self.pop_animation < 15  # Animation lasts 15 frames
        
        # Update time alive
        self.time_alive += dt * 60
        
        # Calculate effective speed
        effective_speed = self.speed * self.speed_multiplier
        
        # Apply movement pattern
        if self.pattern == "vertical":
            self.y += effective_speed * dt * 60
        elif self.pattern == "zigzag":
            self.y += effective_speed * dt * 60
            amp = self.pattern_data.get('amplitude', 40)
            freq = self.pattern_data.get('frequency', 0.03)
            phase = self.pattern_data.get('phase', 0.0)
            wave = math.asin(math.sin(self.time_alive * freq + phase)) * (2 / math.pi)
            self.x = self.base_x + wave * amp
        elif self.pattern == "wave":
            self.y += effective_speed * dt * 60
            amp = self.pattern_data.get('amplitude', 50)
            freq = self.pattern_data.get('frequency', 0.02)
            phase = self.pattern_data.get('phase', 0.0)
            self.x = self.base_x + math.sin(self.time_alive * freq + phase) * amp
        elif self.pattern == "circular":
            # Move in a circular pattern while progressing downward
            self.y += effective_speed * dt * 60 * 0.5  # Slower vertical
            rad = self.pattern_data.get('radius', 50)
            freq = self.pattern_data.get('frequency', 0.03)
            phase = self.pattern_data.get('phase', 0)
            self.x = self.base_x + math.cos(self.time_alive * freq + phase) * rad
        elif self.pattern == "spiral":
            # Spiral inward while moving down
            self.y += effective_speed * dt * 60 * 0.3
            initial_radius = self.pattern_data.get('initial_radius', 80)
            freq = self.pattern_data.get('frequency', 0.03)
            phase = self.pattern_data.get('phase', 0)
            radius = max(5, initial_radius - self.time_alive * 0.5)
            self.x = self.base_x + math.cos(self.time_alive * freq + phase) * radius
        elif self.pattern == "drift":
            vx = self.pattern_data.get('vx', 0.0)
            vy = self.pattern_data.get('vy', effective_speed)
            self.x = self.base_x + self.time_alive * vx
            self.y = self.base_y + self.time_alive * vy
            sway_amp = self.pattern_data.get('sway_amplitude', 0.0)
            sway_freq = self.pattern_data.get('sway_frequency', 0.0)
            if sway_amp and sway_freq:
                sway_phase = self.pattern_data.get('phase', 0.0)
                self.x += math.sin(self.time_alive * sway_freq + sway_phase) * sway_amp
        else:
            self.y += effective_speed * dt * 60

        if not self.has_entered_screen:
            within_x = -self.radius <= self.x <= SCREEN_WIDTH + self.radius
            within_y = -self.radius <= self.y <= SCREEN_HEIGHT + self.radius
            if within_x and within_y:
                self.has_entered_screen = True

        if self.has_entered_screen:
            horizontal_margin = self.radius + 40
            if self.x < -horizontal_margin or self.x > SCREEN_WIDTH + horizontal_margin:
                return False
        
        return self.y < SCREEN_HEIGHT + self.radius + 20

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the balloon with enhanced visual style (BTD-inspired)."""
        if self.popped:
            self._draw_pop_animation(surface)
            return
        
        cx, cy = int(self.x), int(self.y)
        r = int(self.radius)
        
        # Draw shadow beneath balloon
        shadow_surface = pygame.Surface((r * 3, r // 2 + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 40), (r // 2, 5, r * 2, r // 2))
        surface.blit(shadow_surface, (cx - r, cy + r))
        
        # Draw based on balloon type
        if self.balloon_type == BALLOON_TYPE_BLACK:
            self._draw_black_balloon(surface, cx, cy, r)
        elif self.balloon_type == BALLOON_TYPE_WHITE:
            self._draw_white_balloon(surface, cx, cy, r)
        elif self.balloon_type == BALLOON_TYPE_LEAD:
            self._draw_lead_balloon(surface, cx, cy, r)
        elif self.balloon_type == BALLOON_TYPE_ZEBRA:
            self._draw_zebra_balloon(surface, cx, cy, r)
        elif self.balloon_type == BALLOON_TYPE_RAINBOW:
            self._draw_rainbow_balloon(surface, cx, cy, r)
        elif self.balloon_type == BALLOON_TYPE_CERAMIC:
            self._draw_ceramic_balloon(surface, cx, cy, r)
        else:
            self._draw_normal_balloon(surface, cx, cy, r)

    def _draw_normal_balloon(self, surface, cx, cy, r):
        """Draw standard colored balloon."""
        # Outer glow
        pygame.draw.circle(surface, self.color, (cx, cy), r)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy), r, 3)
        
        # Inner gradient effect (darker bottom)
        inner_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)
        
        # Draw highlight (shiny top-left)
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)
        
        # Secondary highlight for more polish
        if r > 15:
            pygame.draw.circle(surface, (255, 255, 255, 180), (cx - r // 4, cy - r // 4), highlight_r // 2)
        
        # Draw string with slight curve effect
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, COLOR_BLACK, string_start, string_end, 2)
        
        # Small tie knot at top of string
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + r + 2), 2)

    def _draw_black_balloon(self, surface, cx, cy, r):
        """Draw black balloon with explosive immunity pattern (BTD-style)."""
        # Dark body with subtle gray tint
        base_color = COLOR_BLACK_BALLOON
        pygame.draw.circle(surface, base_color, (cx, cy), r)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), r, 4)
        
        # Inner gradient (slightly lighter bottom)
        inner_color = (50, 50, 50)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)
        
        # Explosion-proof pattern: small crosshatch/explosion icons
        if r > 20:
            # Draw small explosion-proof symbol pattern
            for i in range(4):
                angle = i * (math.pi / 2) + 0.3
                px = cx + int(math.cos(angle) * r * 0.5)
                py = cy + int(math.sin(angle) * r * 0.5)
                pygame.draw.circle(surface, (80, 80, 80), (px, py), 3)
            
            # Center skull/explosion icon
            pygame.draw.circle(surface, (120, 120, 120), (cx, cy), max(4, r // 4))
            # X pattern for "no explosion"
            pygame.draw.line(surface, (60, 60, 60), (cx - r//5, cy - r//5), (cx + r//5, cy + r//5), 2)
            pygame.draw.line(surface, (60, 60, 60), (cx + r//5, cy - r//5), (cx - r//5, cy + r//5), 2)
        
        # Subtle highlight (less shiny, dark gray)
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (70, 70, 70), highlight_pos, highlight_r)
        
        # Darker string
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (40, 40, 40), string_start, string_end, 2)
        pygame.draw.circle(surface, (40, 40, 40), (cx, cy + r + 2), 2)

    def _draw_white_balloon(self, surface, cx, cy, r):
        """Draw white balloon with ice immunity pattern (BTD-style)."""
        # Bright white body
        pygame.draw.circle(surface, COLOR_WHITE_BALLOON, (cx, cy), r)
        pygame.draw.circle(surface, (180, 180, 180), (cx, cy), r, 3)
        
        # Soft inner gradient (slightly gray bottom)
        inner_color = (220, 220, 225)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)
        
        # Ice crystal patterns
        if r > 18:
            # Draw crystal spikes
            for i in range(6):
                angle = i * (math.tau / 6) + 0.5
                px = cx + int(math.cos(angle) * r * 0.6)
                py = cy + int(math.sin(angle) * r * 0.6)
                # Crystal shape
                pygame.draw.polygon(surface, (200, 230, 255), [
                    (px, py - 4), (px + 3, py + 2), (px - 3, py + 2)
                ])
            
            # Center snowflake pattern
            pygame.draw.circle(surface, (180, 220, 255), (cx, cy), max(3, r // 5))
            # Snowflake arms
            for i in range(6):
                angle = i * (math.tau / 6)
                ex = cx + int(math.cos(angle) * r * 0.3)
                ey = cy + int(math.sin(angle) * r * 0.3)
                pygame.draw.line(surface, (160, 200, 240), (cx, cy), (ex, ey), 2)
        
        # Bright highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)
        if r > 15:
            pygame.draw.circle(surface, (255, 255, 255, 200), (cx - r // 4, cy - r // 4), highlight_r // 2)
        
        # Light string
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (160, 160, 160), string_start, string_end, 2)
        pygame.draw.circle(surface, (160, 160, 160), (cx, cy + r + 2), 2)

    def _draw_lead_balloon(self, surface, cx, cy, r):
        """Draw lead balloon with metallic seams and bolts (BTD-style)."""
        # Metallic gray body
        pygame.draw.circle(surface, COLOR_LEAD_BALLOON, (cx, cy), r)
        pygame.draw.circle(surface, (50, 50, 60), (cx, cy), r, 4)

        # Metallic seams (horizontal lines across balloon)
        seam_color = (70, 70, 80)
        for i in range(3):
            y_offset = -r // 2 + i * (r // 2) + r // 4
            # Draw seam line
            seam_width = int(r * 0.8 * math.sqrt(1 - ((y_offset) / r) ** 2))
            if seam_width > 4:
                pygame.draw.line(surface, seam_color,
                               (cx - seam_width, cy + y_offset),
                               (cx + seam_width, cy + y_offset), 2)
                # Seam bolts at ends
                pygame.draw.circle(surface, (50, 50, 55), (cx - seam_width, cy + y_offset), 3)
                pygame.draw.circle(surface, (50, 50, 55), (cx + seam_width, cy + y_offset), 3)
                pygame.draw.circle(surface, (140, 140, 150), (cx - seam_width - 1, cy + y_offset - 1), 2)
                pygame.draw.circle(surface, (140, 140, 150), (cx + seam_width - 1, cy + y_offset - 1), 2)

        # Inner gradient (darker bottom)
        inner_color = (70, 70, 80)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)

        # Large bolts around the perimeter
        if r > 18:
            num_bolts = 8
            for i in range(num_bolts):
                angle = i * (math.tau / num_bolts)
                px = cx + int(math.cos(angle) * r * 0.78)
                py = cy + int(math.sin(angle) * r * 0.78)
                # Bolt head (hexagonal-ish)
                pygame.draw.circle(surface, (45, 45, 50), (px, py), 4)
                pygame.draw.circle(surface, (130, 130, 140), (px - 1, py - 1), 2)
                # Bolt slot
                pygame.draw.line(surface, (30, 30, 35), (px - 2, py), (px + 2, py), 1)

        # Center reinforced plate
        plate_r = max(6, r // 3)
        pygame.draw.circle(surface, (80, 80, 90), (cx, cy), plate_r)
        pygame.draw.circle(surface, (60, 60, 70), (cx, cy), plate_r, 2)
        # X pattern on plate (no physical symbol)
        pygame.draw.line(surface, (50, 50, 60), (cx - plate_r + 2, cy - plate_r + 2), (cx + plate_r - 2, cy + plate_r - 2), 2)
        pygame.draw.line(surface, (50, 50, 60), (cx + plate_r - 2, cy - plate_r + 2), (cx - plate_r + 2, cy + plate_r - 2), 2)

        # Metallic highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (160, 160, 170), highlight_pos, highlight_r)
        if r > 15:
            pygame.draw.circle(surface, (200, 200, 210), (cx - r // 4, cy - r // 4), highlight_r // 2)

        # Dark gray string
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (70, 70, 80), string_start, string_end, 2)
        pygame.draw.circle(surface, (70, 70, 80), (cx, cy + r + 2), 2)

    def _draw_zebra_balloon(self, surface, cx, cy, r):
        """Draw zebra balloon with black and white stripes (BTD-style)."""
        # White base
        pygame.draw.circle(surface, COLOR_ZEBRA_BALLOON, (cx, cy), r)
        pygame.draw.circle(surface, (100, 100, 100), (cx, cy), r, 3)

        # Black stripes (diagonal zebra pattern)
        stripe_color = (25, 25, 25)
        num_stripes = 6
        for i in range(num_stripes):
            # Diagonal stripe from top-left to bottom-right
            offset = (i - num_stripes // 2) * (r * 0.4)
            stripe_width = r * 0.25

            # Draw stripe as thick line
            x1 = cx - r + offset
            y1 = cy - r
            x2 = cx + r + offset
            y2 = cy + r

            # Clip to circle by drawing multiple short segments
            for j in range(20):
                t1 = j / 20
                t2 = (j + 1) / 20
                sx1 = x1 + (x2 - x1) * t1
                sy1 = y1 + (y2 - y1) * t1
                sx2 = x1 + (x2 - x1) * t2
                sy2 = y1 + (y2 - y1) * t2

                # Check if within circle
                mid_x = (sx1 + sx2) / 2
                mid_y = (sy1 + sy2) / 2
                dist = math.sqrt((mid_x - cx) ** 2 + (mid_y - cy) ** 2)
                if dist < r - 2:
                    pygame.draw.line(surface, stripe_color, (int(sx1), int(sy1)), (int(sx2), int(sy2)), max(3, int(stripe_width)))

        # Inner gradient
        inner_color = (200, 200, 200)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)

        # Dual immunity symbols (explosion X and ice crystal)
        if r > 18:
            # Small explosion-proof X
            pygame.draw.circle(surface, (180, 180, 180), (cx - r // 4, cy), max(3, r // 6))
            pygame.draw.line(surface, (80, 80, 80), (cx - r // 4 - r // 8, cy - r // 8), (cx - r // 4 + r // 8, cy + r // 8), 2)
            pygame.draw.line(surface, (80, 80, 80), (cx - r // 4 + r // 8, cy - r // 8), (cx - r // 4 - r // 8, cy + r // 8), 2)

            # Small snowflake
            pygame.draw.circle(surface, (200, 220, 255), (cx + r // 4, cy), max(3, r // 6))
            for i in range(6):
                angle = i * (math.tau / 6)
                ex = cx + r // 4 + int(math.cos(angle) * r * 0.12)
                ey = cy + int(math.sin(angle) * r * 0.12)
                pygame.draw.line(surface, (150, 180, 220), (cx + r // 4, cy), (ex, ey), 1)

        # Highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)

        # String
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (100, 100, 100), string_start, string_end, 2)
        pygame.draw.circle(surface, (100, 100, 100), (cx, cy + r + 2), 2)

    def _draw_rainbow_balloon(self, surface, cx, cy, r):
        """Draw rainbow balloon with gradient colors (BTD-style)."""
        # Draw colored segments (pie slices)
        num_colors = len(RAINBOW_COLORS)
        for i in range(num_colors):
            start_angle = i * (math.tau / num_colors) - math.pi / 2
            end_angle = (i + 1) * (math.tau / num_colors) - math.pi / 2

            # Draw pie segment
            points = [(cx, cy)]
            for angle in [start_angle + j * (end_angle - start_angle) / 10 for j in range(11)]:
                px = cx + int(math.cos(angle) * r)
                py = cy + int(math.sin(angle) * r)
                points.append((px, py))

            if len(points) >= 3:
                pygame.draw.polygon(surface, RAINBOW_COLORS[i], points)

        # Black border
        pygame.draw.circle(surface, (50, 50, 50), (cx, cy), r, 3)

        # Inner gradient overlay (slight white tint)
        inner_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(inner_surface, (255, 255, 255, 50), (r, r), r * 2 // 3)
        surface.blit(inner_surface, (cx - r, cy - r))

        # Rainbow shimmer highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, highlight_r)
        if r > 15:
            pygame.draw.circle(surface, (255, 255, 255), (cx - r // 4, cy - r // 4), highlight_r // 2)

        # String (gradient)
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (150, 100, 100), string_start, string_end, 2)
        pygame.draw.circle(surface, (150, 100, 100), (cx, cy + r + 2), 2)

    def _draw_ceramic_balloon(self, surface, cx, cy, r):
        """Draw ceramic balloon with cracks based on HP (BTD-style)."""
        # Ceramic tan/brown body
        base_color = COLOR_CERAMIC_BALLOON
        pygame.draw.circle(surface, base_color, (cx, cy), r)
        pygame.draw.circle(surface, (120, 90, 60), (cx, cy), r, 4)

        # Ceramic texture (subtle lines)
        if r > 15:
            for i in range(4):
                angle = i * (math.tau / 4) + 0.3
                x1 = cx + int(math.cos(angle) * r * 0.3)
                y1 = cy + int(math.sin(angle) * r * 0.3)
                x2 = cx + int(math.cos(angle) * r * 0.8)
                y2 = cy + int(math.sin(angle) * r * 0.8)
                pygame.draw.line(surface, (160, 125, 85), (x1, y1), (x2, y2), 1)

        # Inner gradient
        inner_color = (150, 115, 75)
        pygame.draw.circle(surface, inner_color, (cx, cy + r // 4), r * 2 // 3)

        # Draw cracks based on HP lost
        hp_lost = self.max_hp - self.hp

        # Stage 1: Light cracks (3+ HP lost)
        if hp_lost >= 3:
            crack_color = (80, 60, 40)
            # Small cracks
            crack_points = [
                (cx - r // 3, cy - r // 4),
                (cx - r // 5, cy),
                (cx - r // 4, cy + r // 4),
            ]
            for i in range(len(crack_points) - 1):
                pygame.draw.line(surface, crack_color, crack_points[i], crack_points[i + 1], 2)
                # Branch
                pygame.draw.line(surface, crack_color, crack_points[i + 1],
                               (crack_points[i + 1][0] + 4, crack_points[i + 1][1] - 4), 1)

        # Stage 2: Medium cracks (6+ HP lost)
        if hp_lost >= 6:
            crack_color = (60, 45, 30)
            # More prominent cracks
            crack_points2 = [
                (cx + r // 4, cy - r // 3),
                (cx + r // 5, cy - r // 8),
                (cx + r // 3, cy + r // 5),
                (cx + r // 5, cy + r // 3),
            ]
            for i in range(len(crack_points2) - 1):
                pygame.draw.line(surface, crack_color, crack_points2[i], crack_points2[i + 1], 3)
                # Branches
                pygame.draw.line(surface, crack_color, crack_points2[i + 1],
                               (crack_points2[i + 1][0] - 5, crack_points2[i + 1][1] + 3), 2)

            # Additional crack from top
            pygame.draw.line(surface, crack_color, (cx, cy - r // 2), (cx - r // 6, cy - r // 6), 2)
            pygame.draw.line(surface, crack_color, (cx - r // 6, cy - r // 6), (cx - r // 4, cy - r // 4), 2)
            pygame.draw.line(surface, crack_color, (cx - r // 6, cy - r // 6), (cx - r // 5, cy), 2)

        # Stage 3: Heavy cracks (9+ HP lost)
        if hp_lost >= 9:
            crack_color = (40, 30, 20)
            # Major structural cracks
            # Central crack
            pygame.draw.line(surface, crack_color, (cx - r // 2, cy), (cx + r // 2, cy), 4)
            pygame.draw.line(surface, crack_color, (cx, cy - r // 2), (cx, cy + r // 2), 4)

            # Spider cracks from center
            for i in range(8):
                angle = i * (math.tau / 8) + 0.2
                x1 = cx + int(math.cos(angle) * r * 0.2)
                y1 = cy + int(math.sin(angle) * r * 0.2)
                x2 = cx + int(math.cos(angle) * r * 0.7)
                y2 = cy + int(math.sin(angle) * r * 0.7)
                pygame.draw.line(surface, crack_color, (x1, y1), (x2, y2), 2)

            # Chunks appearing to fall off (dark spots)
            for i in range(4):
                angle = i * (math.tau / 4) + 0.5
                px = cx + int(math.cos(angle) * r * 0.6)
                py = cy + int(math.sin(angle) * r * 0.6)
                pygame.draw.circle(surface, (50, 40, 30), (px, py), 4)

        # Highlight
        highlight_r = r // 3
        highlight_pos = (cx - r // 3, cy - r // 3)
        pygame.draw.circle(surface, (200, 170, 130), highlight_pos, highlight_r)
        if r > 15:
            pygame.draw.circle(surface, (220, 190, 150), (cx - r // 4, cy - r // 4), highlight_r // 2)

        # HP indicator (small dots showing remaining health)
        if self.max_hp > 1:
            dot_spacing = r * 2 // (self.max_hp + 1)
            for i in range(self.hp):
                dot_x = cx - r + dot_spacing * (i + 1)
                dot_y = cy + r + 8
                pygame.draw.circle(surface, (100, 80, 60), (dot_x, dot_y), 3)
                pygame.draw.circle(surface, (180, 150, 110), (dot_x - 1, dot_y - 1), 2)

        # String
        string_start = (cx, cy + r)
        string_end = (cx + 2, cy + r + 14)
        pygame.draw.line(surface, (100, 80, 60), string_start, string_end, 2)
        pygame.draw.circle(surface, (100, 80, 60), (cx, cy + r + 2), 2)

    def _draw_pop_animation(self, surface: pygame.Surface) -> None:
        """Draw popping animation."""
        progress = self.pop_animation / 15
        if progress >= 1:
            return
        
        # Expanding particles
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            dist = progress * self.radius * 1.5
            px = self.x + math.cos(angle) * dist
            py = self.y + math.sin(angle) * dist
            size = max(2, int(6 * (1 - progress)))
            
            # Draw star-like particles
            pygame.draw.circle(surface, self.color, (int(px), int(py)), size)

    def get_rect(self) -> pygame.Rect:
        """Get collision rect."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)


class BalloonManager:
    """Manages all balloons from levels."""
    
    def __init__(self, orb_manager: OrbManager):
        self.balloons: List[Balloon] = []
        self.particle_system = ParticleSystem()
        self.orb_manager = orb_manager
        
        # Track off-screen balloons (for level progression)
        self.off_screen_count = 0

    def update(self, dt: float) -> None:
        """Update all balloons. Handle off-screen balloons."""
        new_balloons = []
        for balloon in self.balloons:
            still_active = balloon.update(dt)
            if still_active:
                new_balloons.append(balloon)
            elif not balloon.popped:
                self.off_screen_count += 1
        self.balloons = new_balloons
        
        # Update particles
        self.particle_system.update(dt)

    def pop_balloon(self, balloon: Balloon, x: float, y: float, damage_type: str = "physical") -> None:
        """Pop a balloon with animation and particles, and spawn orbs.
        
        damage_type: "physical" (darts/boomerang/wingman), "explosive" (missiles),
                     "magic" (laser/lightning), "ice" (future)
        """
        # Check for immunity - immune attacks are wasted, no damage or children
        if balloon.is_immune_to(damage_type):
            # Immune: small visual feedback but no damage
            self.particle_system.emit(x, y, balloon.color, count=8, speed=2.5, size=PARTICLE_SIZE)
            self.particle_system.emit(x, y, (180, 180, 180), count=4, speed=3.0, size=2)
            return

        # Normal damage - emit particles with enhanced effect
        self.particle_system.emit(x, y, balloon.color, count=15, speed=5.0, size=PARTICLE_SIZE)
        
        # Add white burst particles for impact
        self.particle_system.emit(x, y, (255, 255, 255), count=8, speed=6.0, size=3)
        
        # Spawn orbs (2 per layer popped)
        self.orb_manager.spawn_orbs(x, y, count=2)

        # Orb luck bonus drops
        if self.orb_manager.orb_luck_level > 0:
            extra_chance = ORB_LUCK_BASE_CHANCE + ORB_LUCK_CHANCE_PER_LEVEL * (self.orb_manager.orb_luck_level - 1)
            extra_max = self.orb_manager.orb_luck_level
            if random.random() < extra_chance:
                extra_count = random.randint(1, extra_max)
                self.orb_manager.spawn_orbs(x, y, count=extra_count)

        # Downgrade or remove
        was_fully_popped = balloon.tier >= 4  # Will be fully popped after damage
        if not balloon.take_damage():
            # Balloon downgraded, not fully popped
            pass
        elif was_fully_popped or balloon.popped:
            # Balloon fully popped - spawn special children for special types
            balloon.spawn_children_on_pop(self)

    def pop_balloon_no_orbs(self, balloon: Balloon) -> None:
        """Pop a balloon without spawning orbs (for off-screen)."""
        self.particle_system.emit(balloon.x, balloon.y, balloon.color, count=6, speed=2.0, size=PARTICLE_SIZE)
        balloon.take_damage()

    def get_remaining_count(self) -> int:
        """Get count of balloons still in play."""
        return len([b for b in self.balloons if not b.popped])

    def get_total_off_screen(self) -> int:
        """Get count of balloons that went off screen."""
        return self.off_screen_count

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all balloons and particles."""
        # Draw balloons
        for balloon in self.balloons:
            balloon.draw(surface)
        
        # Draw particles
        self.particle_system.draw(surface)
