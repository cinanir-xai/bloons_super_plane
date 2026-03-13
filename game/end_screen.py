"""End-of-Level Screen - Separate page shown after completing a level."""

import pygame
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_CYAN, COLOR_ORANGE,
    UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
    LASER_BASE_COST, LASER_COST_MULTIPLIER,
    MISSILE_BASE_COST, MISSILE_UPGRADE_COST
)

class EndScreen:
    """End-of-level screen showing orbs collected, upgrades, and next level option."""
    
    def __init__(self, orbs_collected: int, level_num: int, has_next: bool, 
                 total_orbs: int = 0, dart_speed_level: int = 0, laser_level: int = 0,
                 missile_level: int = 0):
        self.orbs_collected = orbs_collected
        self.level_num = level_num
        self.has_next = has_next
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.missile_level = missile_level
        self.selected_option = 0  # 0 = next level, 1 = quit
        
        # Upgrade state
        self.dart_speed_cost = int(UPGRADE_DART_SPEED_BASE_COST * (UPGRADE_DART_SPEED_COST_MULTIPLIER ** dart_speed_level))
        self.can_buy_dart_speed = self.total_orbs >= self.dart_speed_cost
        
        self.laser_cost = int(LASER_BASE_COST * (LASER_COST_MULTIPLIER ** laser_level))
        self.can_buy_laser = self.total_orbs >= self.laser_cost
        
        self.missile_cost = MISSILE_BASE_COST if missile_level == 0 else MISSILE_UPGRADE_COST
        self.can_buy_missile = self.total_orbs >= self.missile_cost
        
        # Upgrade layout: 2 columns x 3 rows
        self.upgrade_cols = 2
        self.upgrade_rows = 3
        self.upgrade_size = 180 # Larger icons
        self.upgrade_spacing_x = 250
        self.upgrade_spacing_y = 250
        self.upgrade_start_x = (SCREEN_WIDTH - (self.upgrade_cols * self.upgrade_spacing_x)) // 2 + 35
        self.upgrade_start_y = 350
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'next', 'quit', 'buy_dart', 'buy_laser', 'buy_missile', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:
                    return 'next' if self.has_next else 'quit'
                else:
                    return 'quit'
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.selected_option = 1 - self.selected_option
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Check upgrade button clicks
            for i in range(6):
                col = i % self.upgrade_cols
                row = i // self.upgrade_cols
                btn_x = self.upgrade_start_x + col * self.upgrade_spacing_x
                btn_y = self.upgrade_start_y + row * self.upgrade_spacing_y
                
                if btn_x <= mx <= btn_x + self.upgrade_size:
                    if btn_y <= my <= btn_y + self.upgrade_size:
                        if i == 0 and self.can_buy_dart_speed:
                            return 'buy_dart'
                        elif i == 1 and self.can_buy_laser:
                            return 'buy_laser'
                        elif i == 2 and self.can_buy_missile:
                            return 'buy_missile'
                        return 'none'
            
            # Check next/quit buttons
            btn_x = SCREEN_WIDTH // 2 - 100
            btn_y = self.upgrade_start_y + self.upgrade_rows * self.upgrade_spacing_y + 20
            if btn_x <= mx <= btn_x + 200:
                if btn_y <= my <= btn_y + 50:
                    return 'next' if self.has_next else 'quit'
                elif btn_y + 60 <= my <= btn_y + 110:
                    return 'quit'
        
        return 'none'
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the end screen with upgrades."""
        # Clear with dark background
        surface.fill((20, 20, 30))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Title
        title = font_large.render(f"LEVEL {self.level_num} COMPLETE!", True, COLOR_GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)
        
        # Orb count display (top right)
        orb_x = SCREEN_WIDTH - 150
        orb_y = 40
        pygame.draw.circle(surface, COLOR_YELLOW, (orb_x, orb_y), 20)
        pygame.draw.circle(surface, COLOR_BLACK, (orb_x, orb_y), 20, 2)
        pygame.draw.circle(surface, (255, 255, 220), (orb_x - 5, orb_y - 5), 8)
        
        orb_text = font_medium.render(f"x {self.total_orbs}", True, COLOR_YELLOW)
        surface.blit(orb_text, (orb_x + 30, orb_y - 15))
        
        # Orbs collected this level
        orb_label = font_small.render(f"+{self.orbs_collected} this level", True, (200, 200, 200))
        surface.blit(orb_label, (orb_x + 30, orb_y + 15))
        
        # Upgrade section
        upgrade_title = font_medium.render("UPGRADES", True, COLOR_WHITE)
        surface.blit(upgrade_title, (self.upgrade_start_x, self.upgrade_start_y - 60))
        
        # 6 Upgrade buttons in 2x3 layout
        upgrade_info = [
            ("Dart Speed", self.dart_speed_level, self.dart_speed_cost, self.can_buy_dart_speed, self._draw_dart_icon),
            ("Laser Beam", self.laser_level, self.laser_cost, self.can_buy_laser, self._draw_laser_icon),
            ("Missiles", self.missile_level, self.missile_cost, self.can_buy_missile, self._draw_missile_icon),
            ("Locked", 0, 0, False, self._draw_locked_icon),
            ("Locked", 0, 0, False, self._draw_locked_icon),
            ("Locked", 0, 0, False, self._draw_locked_icon)
        ]
        
        for i, (name, level, cost, can_buy, draw_icon) in enumerate(upgrade_info):
            col = i % self.upgrade_cols
            row = i // self.upgrade_cols
            btn_x = self.upgrade_start_x + col * self.upgrade_spacing_x
            btn_y = self.upgrade_start_y + row * self.upgrade_spacing_y
            
            # Button background
            if name == "Locked":
                btn_color = (50, 50, 50)
            elif can_buy:
                btn_color = (80, 80, 120)
            else:
                btn_color = (60, 60, 80)
            
            pygame.draw.rect(surface, btn_color, (btn_x, btn_y, self.upgrade_size, self.upgrade_size))
            pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, self.upgrade_size, self.upgrade_size), 3)
            
            # Draw icon (scaled up)
            draw_icon(surface, btn_x + self.upgrade_size // 2, btn_y + self.upgrade_size // 2, scale=2.0)
            
            if name != "Locked":
                # Name and Level
                name_text = font_tiny.render(f"{name} Lv.{level}", True, COLOR_WHITE)
                surface.blit(name_text, (btn_x + 5, btn_y + 5))
                
                # Cost
                cost_text = font_small.render(f"{cost} Orbs", True, COLOR_YELLOW if can_buy else (100, 100, 100))
                cost_rect = cost_text.get_rect(midbottom=(btn_x + self.upgrade_size // 2, btn_y + self.upgrade_size - 10))
                surface.blit(cost_text, cost_rect)
        
        # Next/Quit buttons
        btn_x = SCREEN_WIDTH // 2 - 100
        btn_y = self.upgrade_start_y + self.upgrade_rows * self.upgrade_spacing_y + 20
        btn_width = 200
        btn_height = 50
        
        # Next Level button
        if self.has_next:
            next_color = COLOR_YELLOW if self.selected_option == 0 else (100, 100, 100)
            pygame.draw.rect(surface, next_color, (btn_x, btn_y, btn_width, btn_height))
            pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, btn_width, btn_height), 3)
            next_text = font_medium.render("NEXT LEVEL", True, COLOR_BLACK)
            text_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, btn_y + 25))
            surface.blit(next_text, text_rect)
            btn_y += 60
        
        # Quit button
        quit_color = COLOR_RED if self.selected_option == 1 else (100, 100, 100)
        pygame.draw.rect(surface, quit_color, (btn_x, btn_y, btn_width, btn_height))
        pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, btn_width, btn_height), 3)
        quit_text = font_medium.render("QUIT", True, COLOR_WHITE)
        text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, btn_y + 25))
        surface.blit(quit_text, text_rect)
        
        # Instructions
        instr = font_small.render("Click upgrade to buy | Arrow keys + ENTER for navigation", True, (150, 150, 150))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(instr, instr_rect)
    
    def _draw_dart_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a dart icon."""
        points = [
            (cx, cy - 20 * scale),
            (cx + 8 * scale, cy),
            (cx + 3 * scale, cy),
            (cx + 3 * scale, cy + 15 * scale),
            (cx - 3 * scale, cy + 15 * scale),
            (cx - 3 * scale, cy),
            (cx - 8 * scale, cy)
        ]
        pygame.draw.polygon(surface, COLOR_WHITE, points)
        pygame.draw.polygon(surface, COLOR_BLACK, points, 2)
    
    def _draw_laser_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a laser icon."""
        pygame.draw.rect(surface, COLOR_CYAN, (cx - 2 * scale, cy - 30 * scale, 4 * scale, 60 * scale))
        pygame.draw.rect(surface, COLOR_WHITE, (cx - 1 * scale, cy - 30 * scale, 2 * scale, 60 * scale))
        pygame.draw.circle(surface, COLOR_CYAN, (cx, cy), int(12 * scale))
        pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), int(6 * scale))

    def _draw_missile_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a missile icon."""
        # Body
        pygame.draw.rect(surface, COLOR_WHITE, (cx - 6 * scale, cy - 15 * scale, 12 * scale, 30 * scale))
        # Tip
        pygame.draw.rect(surface, COLOR_RED, (cx - 6 * scale, cy - 15 * scale, 12 * scale, 8 * scale))
        # Fire glow
        pygame.draw.circle(surface, COLOR_ORANGE, (cx, cy + 20 * scale), int(8 * scale))
        pygame.draw.circle(surface, COLOR_YELLOW, (cx, cy + 20 * scale), int(4 * scale))

    def _draw_locked_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a locked padlock icon."""
        # Lock body
        pygame.draw.rect(surface, (100, 100, 100), (cx - 12 * scale, cy - 5 * scale, 24 * scale, 20 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 12 * scale, cy - 5 * scale, 24 * scale, 20 * scale), 2)
        # Lock shackle
        pygame.draw.arc(surface, (100, 100, 100), (cx - 10 * scale, cy - 20 * scale, 20 * scale, 20 * scale), 0, 3.14, int(3 * scale))
        # Keyhole
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + 5 * scale), int(4 * scale))
