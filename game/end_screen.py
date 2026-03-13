"""End-of-Level Screen - Separate page shown after completing a level."""

import pygame
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_CYAN,
    UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
    LASER_BASE_COST, LASER_COST_MULTIPLIER
)

class EndScreen:
    """End-of-level screen showing orbs collected, upgrades, and next level option."""
    
    def __init__(self, orbs_collected: int, level_num: int, has_next: bool, 
                 total_orbs: int = 0, dart_speed_level: int = 0, laser_level: int = 0):
        self.orbs_collected = orbs_collected
        self.level_num = level_num
        self.has_next = has_next
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.selected_option = 0  # 0 = next level, 1 = quit
        
        # Upgrade state
        self.dart_speed_cost = int(UPGRADE_DART_SPEED_BASE_COST * (UPGRADE_DART_SPEED_COST_MULTIPLIER ** dart_speed_level))
        self.can_buy_dart_speed = self.total_orbs >= self.dart_speed_cost
        
        self.laser_cost = int(LASER_BASE_COST * (LASER_COST_MULTIPLIER ** laser_level))
        self.can_buy_laser = self.total_orbs >= self.laser_cost
        
        # Upgrade button rects
        self.upgrade_y = 450
        self.upgrade_size = 80
        self.upgrade_spacing = 90
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'next', 'quit', 'buy_dart', 'buy_laser', or 'none'."""
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
                btn_x = 80 + i * self.upgrade_spacing
                btn_y = self.upgrade_y
                if btn_x <= mx <= btn_x + self.upgrade_size:
                    if btn_y <= my <= btn_y + self.upgrade_size:
                        if i == 0 and self.can_buy_dart_speed:
                            return 'buy_dart'
                        elif i == 1 and self.can_buy_laser:
                            return 'buy_laser'
                        return 'none'
            
            # Check next/quit buttons
            btn_x = SCREEN_WIDTH // 2 - 100
            if btn_x <= mx <= btn_x + 200:
                if self.upgrade_y + 120 <= my <= self.upgrade_y + 170:
                    return 'next' if self.has_next else 'quit'
                elif self.upgrade_y + 180 <= my <= self.upgrade_y + 230:
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
        surface.blit(upgrade_title, (80, self.upgrade_y - 40))
        
        # 6 Upgrade buttons
        upgrade_names = [
            "Dart Speed +20%",
            "Laser Beam" if self.laser_level == 0 else f"Laser Lv.{self.laser_level}",
            "Locked",
            "Locked",
            "Locked",
            "Locked"
        ]
        upgrade_icons = [
            self._draw_dart_icon,
            self._draw_laser_icon,
            self._draw_locked_icon,
            self._draw_locked_icon,
            self._draw_locked_icon,
            self._draw_locked_icon
        ]
        
        for i in range(6):
            btn_x = 80 + i * self.upgrade_spacing
            btn_y = self.upgrade_y
            
            # Button background
            if i == 0:
                if self.can_buy_dart_speed:
                    btn_color = (80, 80, 120)
                else:
                    btn_color = (60, 60, 80)
            elif i == 1:
                if self.can_buy_laser:
                    btn_color = (80, 80, 120)
                else:
                    btn_color = (60, 60, 80)
            else:
                btn_color = (50, 50, 50)
            
            pygame.draw.rect(surface, btn_color, (btn_x, btn_y, self.upgrade_size, self.upgrade_size))
            pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, self.upgrade_size, self.upgrade_size), 2)
            
            # Draw icon
            if i == 0:
                self._draw_dart_icon(surface, btn_x + self.upgrade_size // 2, btn_y + self.upgrade_size // 2)
            elif i == 1:
                self._draw_laser_icon(surface, btn_x + self.upgrade_size // 2, btn_y + self.upgrade_size // 2)
            else:
                self._draw_locked_icon(surface, btn_x + self.upgrade_size // 2, btn_y + self.upgrade_size // 2)
            
            # Draw cost for upgrades
            if i == 0:
                cost_text = font_tiny.render(f"{self.dart_speed_cost} orbs", True, 
                                            COLOR_YELLOW if self.can_buy_dart_speed else (100, 100, 100))
                surface.blit(cost_text, (btn_x + 5, btn_y + self.upgrade_size + 5))
                
                # Level indicator
                level_text = font_tiny.render(f"Lv.{self.dart_speed_level}", True, COLOR_WHITE)
                surface.blit(level_text, (btn_x + 5, btn_y + self.upgrade_size + 20))
            elif i == 1:
                cost_text = font_tiny.render(f"{self.laser_cost} orbs", True, 
                                            COLOR_YELLOW if self.can_buy_laser else (100, 100, 100))
                surface.blit(cost_text, (btn_x + 5, btn_y + self.upgrade_size + 5))
                
                # Level indicator
                level_text = font_tiny.render(f"Lv.{self.laser_level}", True, COLOR_WHITE)
                surface.blit(level_text, (btn_x + 5, btn_y + self.upgrade_size + 20))
        
        # Next/Quit buttons
        btn_x = SCREEN_WIDTH // 2 - 100
        btn_y = self.upgrade_y + 120
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
    
    def _draw_dart_icon(self, surface: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a dart icon."""
        # Simple dart shape
        pygame.draw.polygon(surface, COLOR_WHITE, [
            (cx, cy - 20),
            (cx + 8, cy),
            (cx + 3, cy),
            (cx + 3, cy + 15),
            (cx - 3, cy + 15),
            (cx - 3, cy),
            (cx - 8, cy)
        ])
        pygame.draw.polygon(surface, COLOR_BLACK, [
            (cx, cy - 20),
            (cx + 8, cy),
            (cx + 3, cy),
            (cx + 3, cy + 15),
            (cx - 3, cy + 15),
            (cx - 3, cy),
            (cx - 8, cy)
        ], 1)
    
    def _draw_laser_icon(self, surface: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a laser icon."""
        # Simple laser shape
        pygame.draw.rect(surface, COLOR_CYAN, (cx - 2, cy - 20, 4, 40))
        pygame.draw.rect(surface, COLOR_WHITE, (cx - 1, cy - 20, 2, 40))
        # Glow
        pygame.draw.circle(surface, COLOR_CYAN, (cx, cy), 8)
        pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), 4)

    def _draw_locked_icon(self, surface: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a locked padlock icon."""
        # Lock body
        pygame.draw.rect(surface, (100, 100, 100), (cx - 12, cy - 5, 24, 20))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 12, cy - 5, 24, 20), 1)
        # Lock shackle
        pygame.draw.arc(surface, (100, 100, 100), (cx - 10, cy - 20, 20, 20), 0, 3.14, 3)
        pygame.draw.arc(surface, COLOR_BLACK, (cx - 10, cy - 20, 20, 20), 0, 3.14, 2)
        # Keyhole
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + 5), 4)
