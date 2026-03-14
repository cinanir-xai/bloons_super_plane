"""Menu screens for the game - Main Menu, Level Select, and Shop."""

import pygame
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_CYAN, COLOR_ORANGE,
    COLOR_BROWN, COLOR_BLUE, COLOR_PINK
)
from game.level_manager import LevelManager


class MainMenu:
    """Main menu screen with Play, Shop, and Quit options."""
    
    def __init__(self):
        self.selected_option = 0  # 0 = Play, 1 = Shop, 2 = Quit
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'play', 'shop', 'quit', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 3
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:
                    return 'play'
                elif self.selected_option == 1:
                    return 'shop'
                else:
                    return 'quit'
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            btn_x = SCREEN_WIDTH // 2 - 150
            btn_y = 400
            btn_width = 300
            btn_height = 60
            
            for i in range(3):
                if btn_x <= mx <= btn_x + btn_width:
                    if btn_y + i * 80 <= my <= btn_y + i * 80 + btn_height:
                        if i == 0:
                            return 'play'
                        elif i == 1:
                            return 'shop'
                        else:
                            return 'quit'
        
        return 'none'
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu."""
        # Dark gradient background
        surface.fill((15, 15, 25))
        
        font_title = pygame.font.Font(None, 120)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Title with glow effect
        title = font_title.render("SKY DEFENDER", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_small.render("Retro Atari-Style Shooter", True, (150, 150, 200))
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 210))
        surface.blit(subtitle, sub_rect)
        
        # Menu buttons
        btn_x = SCREEN_WIDTH // 2 - 150
        btn_y = 400
        btn_width = 300
        btn_height = 60
        
        options = [("PLAY", COLOR_GREEN), ("SHOP", COLOR_YELLOW), ("QUIT", COLOR_RED)]
        
        for i, (text, color) in enumerate(options):
            is_selected = (i == self.selected_option)
            
            # Button background
            if is_selected:
                bg_color = (60, 60, 80)
                border_width = 4
            else:
                bg_color = (40, 40, 50)
                border_width = 2
            
            pygame.draw.rect(surface, bg_color, (btn_x, btn_y + i * 80, btn_width, btn_height))
            pygame.draw.rect(surface, color if is_selected else COLOR_BLACK, 
                           (btn_x, btn_y + i * 80, btn_width, btn_height), border_width)
            
            # Button text
            text_surface = font_medium.render(text, True, color if is_selected else (150, 150, 150))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, btn_y + i * 80 + btn_height // 2))
            surface.blit(text_surface, text_rect)
        
        # Instructions
        instr = font_small.render("Arrow Keys + ENTER or Click to select", True, (100, 100, 120))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        surface.blit(instr, instr_rect)
        
        # Decorative elements - simple plane silhouette
        self._draw_plane_silhouette(surface, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100)
    
    def _draw_plane_silhouette(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw a simple plane silhouette."""
        # Wings
        pygame.draw.rect(surface, (60, 60, 80), (x - 40, y - 4, 80, 8))
        # Fuselage
        pygame.draw.rect(surface, (60, 60, 80), (x - 4, y - 40, 8, 80))
        # Tail
        pygame.draw.rect(surface, (50, 50, 70), (x - 6, y + 36, 12, 8))


class LevelSelect:
    """Level select screen with 2x3 grid of level icons."""
    
    def __init__(self, unlocked_levels: int = 6, level_manager: LevelManager = None):
        self.selected_level = 1
        self.unlocked_levels = unlocked_levels
        self.level_manager = level_manager or LevelManager()
        self.cols = 2
        self.rows = 3
        self.icon_size = 200
        self.icon_spacing_x = 280
        self.icon_spacing_y = 280
        self.start_x = (SCREEN_WIDTH - (self.cols * self.icon_spacing_x)) // 2 + 40
        self.start_y = 250
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'level_X', 'back', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_level = max(1, self.selected_level - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_level = min(self.unlocked_levels, self.selected_level + 1)
            elif event.key == pygame.K_UP:
                self.selected_level = max(1, self.selected_level - self.cols)
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(self.unlocked_levels, self.selected_level + self.cols)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_level <= self.unlocked_levels:
                    return f'level_{self.selected_level}'
            elif event.key == pygame.K_ESCAPE:
                return 'back'
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Check back button
            if 50 <= mx <= 150 and 50 <= my <= 90:
                return 'back'
            
            # Check level icons
            for i in range(6):
                col = i % self.cols
                row = i // self.cols
                icon_x = self.start_x + col * self.icon_spacing_x
                icon_y = self.start_y + row * self.icon_spacing_y
                
                if icon_x <= mx <= icon_x + self.icon_size:
                    if icon_y <= my <= icon_y + self.icon_size:
                        level_num = i + 1
                        if level_num <= self.unlocked_levels:
                            return f'level_{level_num}'
        
        return 'none'
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the level select screen."""
        surface.fill((20, 20, 35))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Title
        title = font_large.render("SELECT LEVEL", True, COLOR_YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)
        
        # Back button
        pygame.draw.rect(surface, (60, 60, 80), (50, 50, 100, 40))
        pygame.draw.rect(surface, COLOR_BLACK, (50, 50, 100, 40), 2)
        back_text = font_small.render("BACK", True, COLOR_WHITE)
        surface.blit(back_text, (60, 60))
        
        # Level icons in 2x3 grid
        for i in range(6):
            level_num = i + 1
            col = i % self.cols
            row = i // self.cols
            icon_x = self.start_x + col * self.icon_spacing_x
            icon_y = self.start_y + row * self.icon_spacing_y
            
            is_locked = level_num > self.unlocked_levels
            is_selected = (level_num == self.selected_level and not is_locked)
            
            # Icon background
            if is_locked:
                bg_color = (40, 40, 50)
                border_color = (80, 80, 90)
            elif is_selected:
                bg_color = (60, 60, 90)
                border_color = COLOR_YELLOW
            else:
                bg_color = (50, 50, 70)
                border_color = COLOR_BLACK
            
            pygame.draw.rect(surface, bg_color, (icon_x, icon_y, self.icon_size, self.icon_size))
            pygame.draw.rect(surface, border_color, (icon_x, icon_y, self.icon_size, self.icon_size), 4)
            
            # Level preview (mini scene)
            if not is_locked:
                self._draw_level_preview(surface, icon_x, icon_y, level_num)
            else:
                # Lock icon
                self._draw_lock(surface, icon_x + self.icon_size // 2, icon_y + self.icon_size // 2)
            
            # Level number
            level_text = font_medium.render(f"LEVEL {level_num}", True, 
                                           COLOR_WHITE if not is_locked else (100, 100, 100))
            level_rect = level_text.get_rect(center=(icon_x + self.icon_size // 2, 
                                                      icon_y + self.icon_size + 25))
            surface.blit(level_text, level_rect)
        
        # Instructions
        instr = font_small.render("Arrow Keys + ENTER or Click to select level", True, (120, 120, 140))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        surface.blit(instr, instr_rect)
    
    def _draw_level_preview(self, surface: pygame.Surface, x: int, y: int, level_num: int) -> None:
        """Draw a mini preview of the level."""
        preview_x = x + 20
        preview_y = y + 20
        preview_w = self.icon_size - 40
        preview_h = self.icon_size - 60
        
        # Mini sky background
        pygame.draw.rect(surface, (100, 180, 255), (preview_x, preview_y, preview_w, preview_h // 2))
        # Mini ground
        pygame.draw.rect(surface, (34, 139, 34), (preview_x, preview_y + preview_h // 2, 
                                                  preview_w, preview_h // 2))
        
        # Draw balloons based on level
        balloon_count = min(level_num * 2 + 2, 10)
        colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
        
        for i in range(balloon_count):
            bx = preview_x + 15 + (i % 5) * 30
            by = preview_y + 20 + (i // 5) * 25
            tier = min(i // 2, 4)
            color = colors[tier]
            pygame.draw.circle(surface, color, (bx, by), 8)
            pygame.draw.circle(surface, COLOR_BLACK, (bx, by), 8, 1)
    
    def _draw_lock(self, surface: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a lock icon."""
        pygame.draw.rect(surface, (120, 120, 120), (cx - 15, cy - 5, 30, 25))
        pygame.draw.arc(surface, (120, 120, 120), (cx - 12, cy - 25, 24, 24), 0, 3.14, 3)
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + 8), 5)


class Shop:
    """Shop screen accessible from main menu."""
    
    def __init__(self, total_orbs: int = 0, dart_speed_level: int = 0,
                 laser_level: int = 0, missile_level: int = 0, boomerang_level: int = 0):
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.missile_level = missile_level
        self.boomerang_level = boomerang_level
        self.selected_option = 0  # 0 = back
        
        # Recalculate costs
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER
        )
        
        # Dart: unlocked from beginning, upgrades start at 100, increase by 50%
        self.dart_speed_cost = int(UPGRADE_DART_SPEED_BASE_COST * 
                                   (UPGRADE_DART_SPEED_COST_MULTIPLIER ** dart_speed_level))
        self.can_buy_dart_speed = self.total_orbs >= self.dart_speed_cost
        
        # Laser: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if laser_level == 0:
            self.laser_cost = LASER_UNLOCK_COST
        else:
            self.laser_cost = int(LASER_BASE_COST * (LASER_COST_MULTIPLIER ** (laser_level - 1)))
        self.can_buy_laser = self.total_orbs >= self.laser_cost
        
        # Missile: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if missile_level == 0:
            self.missile_cost = MISSILE_UNLOCK_COST
        else:
            self.missile_cost = int(MISSILE_BASE_COST * (MISSILE_COST_MULTIPLIER ** (missile_level - 1)))
        self.can_buy_missile = self.total_orbs >= self.missile_cost
        
        # Boomerang: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if boomerang_level == 0:
            self.boomerang_cost = BOOMERANG_UNLOCK_COST
        else:
            self.boomerang_cost = int(BOOMERANG_BASE_COST * (BOOMERANG_COST_MULTIPLIER ** (boomerang_level - 1)))
        self.can_buy_boomerang = self.total_orbs >= self.boomerang_cost
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'buy_X', 'back', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Check back button
            if 50 <= mx <= 150 and 50 <= my <= 90:
                return 'back'
            
            # Check upgrade buttons
            btn_x = 100
            btn_y = 200
            btn_width = 350
            btn_height = 80
            
            for i in range(4):
                if btn_x <= mx <= btn_x + btn_width:
                    if btn_y + i * 100 <= my <= btn_y + i * 100 + btn_height:
                        if i == 0 and self.can_buy_dart_speed:
                            return 'buy_dart'
                        elif i == 1 and self.can_buy_laser:
                            return 'buy_laser'
                        elif i == 2 and self.can_buy_missile:
                            return 'buy_missile'
                        elif i == 3 and self.can_buy_boomerang:
                            return 'buy_boomerang'
        
        return 'none'
    
    def buy_upgrade(self, upgrade_type: str) -> bool:
        """Attempt to buy an upgrade. Returns True if successful."""
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER
        )
        
        if upgrade_type == 'dart' and self.can_buy_dart_speed:
            self.total_orbs -= self.dart_speed_cost
            self.dart_speed_level += 1
            self.dart_speed_cost = int(UPGRADE_DART_SPEED_BASE_COST * 
                                        (UPGRADE_DART_SPEED_COST_MULTIPLIER ** self.dart_speed_level))
            self.can_buy_dart_speed = self.total_orbs >= self.dart_speed_cost
            return True
        elif upgrade_type == 'laser' and self.can_buy_laser:
            self.total_orbs -= self.laser_cost
            self.laser_level += 1
            # After unlock, upgrades cost 100 * 1.5^(level-1)
            if self.laser_level == 1:
                self.laser_cost = LASER_BASE_COST  # First upgrade after unlock
            else:
                self.laser_cost = int(LASER_BASE_COST * (LASER_COST_MULTIPLIER ** (self.laser_level - 1)))
            self.can_buy_laser = self.total_orbs >= self.laser_cost
            return True
        elif upgrade_type == 'missile' and self.can_buy_missile:
            self.total_orbs -= self.missile_cost
            self.missile_level += 1
            # After unlock, upgrades cost 100 * 1.5^(level-1)
            if self.missile_level == 1:
                self.missile_cost = MISSILE_BASE_COST  # First upgrade after unlock
            else:
                self.missile_cost = int(MISSILE_BASE_COST * (MISSILE_COST_MULTIPLIER ** (self.missile_level - 1)))
            self.can_buy_missile = self.total_orbs >= self.missile_cost
            return True
        elif upgrade_type == 'boomerang' and self.can_buy_boomerang:
            self.total_orbs -= self.boomerang_cost
            self.boomerang_level += 1
            # After unlock, upgrades cost 100 * 1.5^(level-1)
            if self.boomerang_level == 1:
                self.boomerang_cost = BOOMERANG_BASE_COST  # First upgrade after unlock
            else:
                self.boomerang_cost = int(BOOMERANG_BASE_COST * (BOOMERANG_COST_MULTIPLIER ** (self.boomerang_level - 1)))
            self.can_buy_boomerang = self.total_orbs >= self.boomerang_cost
            return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the shop screen."""
        surface.fill((20, 20, 35))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Title
        title = font_large.render("UPGRADE SHOP", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title, title_rect)
        
        # Orb display
        orb_x = SCREEN_WIDTH - 200
        orb_y = 40
        pygame.draw.circle(surface, COLOR_YELLOW, (orb_x, orb_y), 25)
        pygame.draw.circle(surface, COLOR_BLACK, (orb_x, orb_y), 25, 2)
        orb_text = font_medium.render(f"x {self.total_orbs}", True, COLOR_YELLOW)
        surface.blit(orb_text, (orb_x + 35, orb_y - 15))
        
        # Back button
        pygame.draw.rect(surface, (60, 60, 80), (50, 50, 100, 40))
        pygame.draw.rect(surface, COLOR_BLACK, (50, 50, 100, 40), 2)
        back_text = font_small.render("BACK", True, COLOR_WHITE)
        surface.blit(back_text, (60, 60))
        
        # Upgrade items
        items = [
            ("Dart Speed +20%", self.dart_speed_level, self.dart_speed_cost, 
             self.can_buy_dart_speed, COLOR_WHITE),
            ("Laser Beam", self.laser_level, self.laser_cost,
             self.can_buy_laser, COLOR_CYAN),
            ("Missiles", self.missile_level, self.missile_cost,
             self.can_buy_missile, COLOR_ORANGE),
            ("Boomerang", self.boomerang_level, self.boomerang_cost,
             self.can_buy_boomerang, COLOR_BROWN)
        ]
        
        btn_x = 100
        btn_y = 200
        btn_width = 350
        btn_height = 80
        
        for i, (name, level, cost, can_buy, color) in enumerate(items):
            is_selected = (i == self.selected_option)
            
            # Button background
            if can_buy:
                bg_color = (60, 60, 80)
            else:
                bg_color = (40, 40, 50)
            
            pygame.draw.rect(surface, bg_color, (btn_x, btn_y + i * 100, btn_width, btn_height))
            pygame.draw.rect(surface, color if can_buy else (80, 80, 80),
                           (btn_x, btn_y + i * 100, btn_width, btn_height), 3)
            
            # Name and level/status
            if level == 0:
                status = "Unlock"
            else:
                status = f"Lv.{level}"
            name_text = font_small.render(f"{name} {status}", True, 
                                         color if can_buy else (100, 100, 100))
            surface.blit(name_text, (btn_x + 10, btn_y + i * 100 + 10))
            
            # Cost
            cost_text = font_tiny.render(f"{cost} Orbs", True,
                                        COLOR_YELLOW if can_buy else (80, 80, 80))
            surface.blit(cost_text, (btn_x + 10, btn_y + i * 100 + 40))
            
            # Icon preview (small)
            self._draw_icon(surface, btn_x + btn_width - 40, 
                          btn_y + i * 100 + btn_height // 2, i)
        
        # Instructions
        instr = font_small.render("Click to buy upgrades | Press ESC to go back", True, (120, 120, 140))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        surface.blit(instr, instr_rect)
    
    def _draw_icon(self, surface: pygame.Surface, cx: int, cy: int, index: int) -> None:
        """Draw a small icon for each upgrade."""
        if index == 0:  # Dart
            pygame.draw.polygon(surface, COLOR_WHITE, [
                (cx, cy - 10), (cx + 4, cy), (cx + 2, cy),
                (cx + 2, cy + 8), (cx - 2, cy + 8),
                (cx - 2, cy), (cx - 4, cy)
            ])
        elif index == 1:  # Laser
            pygame.draw.rect(surface, COLOR_CYAN, (cx - 1, cy - 15, 2, 30))
            pygame.draw.circle(surface, COLOR_CYAN, (cx, cy), 6)
        elif index == 2:  # Missile
            pygame.draw.rect(surface, COLOR_WHITE, (cx - 3, cy - 8, 6, 16))
            pygame.draw.rect(surface, COLOR_RED, (cx - 3, cy - 8, 6, 4))
        elif index == 3:  # Boomerang
            points = [(cx, cy - 10), (cx + 10, cy + 10), (cx, cy + 5), (cx - 10, cy + 10)]
            pygame.draw.polygon(surface, COLOR_BROWN, points)
