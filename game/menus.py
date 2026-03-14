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
        """Draw the main menu with title card."""
        # Dark sky background with gradient
        for y in range(SCREEN_HEIGHT):
            color = (10 + y // 30, 15 + y // 25, 30 + y // 20)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        import random
        for _ in range(80):
            star_x = (pygame.time.get_ticks() // 50 + _ * 137) % SCREEN_WIDTH
            star_y = (_ * 83) % SCREEN_HEIGHT
            brightness = 100 + (pygame.time.get_ticks() // 100 + _) % 155
            pygame.draw.circle(surface, (brightness, brightness, brightness), (star_x, star_y), 1)
        
        font_title = pygame.font.Font(None, 140)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Title card background
        card_x = SCREEN_WIDTH // 2 - 400
        card_y = 80
        card_w = 800
        card_h = 220
        
        # Card with gradient
        pygame.draw.rect(surface, (30, 35, 50), (card_x, card_y, card_w, card_h))
        pygame.draw.rect(surface, (80, 90, 120), (card_x, card_y, card_w, card_h), 4)
        
        # Inner glow
        pygame.draw.rect(surface, (50, 60, 80), (card_x + 5, card_y + 5, card_w - 10, card_h - 10), 2)
        
        # Title with glow
        title = font_title.render("SKY DEFENDER", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, card_y + 80))
        
        # Glow effect
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            glow = font_title.render("SKY DEFENDER", True, (0, 100, 150))
            surface.blit(glow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_small.render("Retro Atari-Style Shooter", True, (180, 180, 220))
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, card_y + 150))
        surface.blit(subtitle, sub_rect)
        
        # Draw decorative balloons in title card
        balloon_colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
        for i in range(5):
            bx = card_x + 80 + i * 140
            by = card_y + 60 + (i % 2) * 30
            self._draw_menu_balloon(surface, bx, by, balloon_colors[i], 25)
        
        # Draw plane in title card
        self._draw_menu_plane(surface, SCREEN_WIDTH // 2, card_y + 180)
        
        # Menu buttons
        btn_x = SCREEN_WIDTH // 2 - 150
        btn_y = 380
        btn_width = 300
        btn_height = 65
        
        options = [("PLAY", COLOR_GREEN), ("SHOP", COLOR_YELLOW), ("QUIT", COLOR_RED)]
        
        for i, (text, color) in enumerate(options):
            is_selected = (i == self.selected_option)
            
            # Button background with depth
            if is_selected:
                bg_color = (70, 70, 95)
                border_width = 4
                shadow_offset = 3
            else:
                bg_color = (45, 45, 60)
                border_width = 3
                shadow_offset = 2
            
            # Shadow
            pygame.draw.rect(surface, (20, 20, 30), (btn_x + shadow_offset, btn_y + i * 85 + shadow_offset, btn_width, btn_height))
            
            # Button
            pygame.draw.rect(surface, bg_color, (btn_x, btn_y + i * 85, btn_width, btn_height))
            pygame.draw.rect(surface, color if is_selected else (80, 80, 100), 
                           (btn_x, btn_y + i * 85, btn_width, btn_height), border_width)
            
            # Button text
            text_surface = font_medium.render(text, True, color if is_selected else (170, 170, 180))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, btn_y + i * 85 + btn_height // 2))
            surface.blit(text_surface, text_rect)
        
        # Instructions
        instr = font_small.render("Arrow Keys + ENTER or Click to select", True, (120, 120, 140))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(instr, instr_rect)
    
    def _draw_menu_balloon(self, surface: pygame.Surface, x: int, y: int, color: tuple, radius: int) -> None:
        """Draw a balloon for the title card."""
        # Balloon body
        pygame.draw.circle(surface, color, (x, y), radius)
        # Highlight
        pygame.draw.circle(surface, (255, 255, 255), (x - radius//3, y - radius//3), radius//4)
        # String
        pygame.draw.line(surface, (100, 100, 100), (x, y + radius), (x, y + radius + 20), 1)
    
    def _draw_menu_plane(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw a detailed plane for the title card."""
        # Shadow
        pygame.draw.ellipse(surface, (0, 0, 0, 50), (x - 45, y + 5, 90, 20))
        
        # Wings
        pygame.draw.rect(surface, COLOR_RED, (x - 45, y - 5, 90, 10))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 45, y - 5, 90, 10), 2)
        # Wing highlights
        pygame.draw.line(surface, (255, 100, 100), (x - 43, y - 3), (x + 43, y - 3), 2)
        
        # Fuselage
        pygame.draw.rect(surface, COLOR_RED, (x - 8, y - 35, 16, 70))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 8, y - 35, 16, 70), 2)
        pygame.draw.line(surface, (255, 100, 100), (x - 6, y - 33), (x - 6, y + 33), 2)
        
        # Nose cone
        pygame.draw.polygon(surface, COLOR_WHITE, [(x, y - 45), (x - 8, y - 35), (x + 8, y - 35)])
        pygame.draw.polygon(surface, COLOR_BLACK, [(x, y - 45), (x - 8, y - 35), (x + 8, y - 35)], 1)
        
        # Cockpit
        pygame.draw.rect(surface, (100, 200, 255), (x - 5, y - 25, 10, 15))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 5, y - 25, 10, 15), 1)
        
        # Tail fin
        pygame.draw.polygon(surface, COLOR_RED, [(x - 6, y + 35), (x + 6, y + 35), (x, y + 55)])
        pygame.draw.polygon(surface, COLOR_BLACK, [(x - 6, y + 35), (x + 6, y + 35), (x, y + 55)], 1)
        
        # Engine glow
        pygame.draw.circle(surface, (255, 150, 50), (x, y + 50), 5)
        pygame.draw.circle(surface, (255, 200, 100), (x, y + 50), 3)


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
                 laser_level: int = 0, missile_level: int = 0, boomerang_level: int = 0,
                 lightning_level: int = 0, wingman_level: int = 0):
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.missile_level = missile_level
        self.boomerang_level = boomerang_level
        self.lightning_level = lightning_level
        self.wingman_level = wingman_level
        self.selected_option = 0  # 0 = back
        
        # Recalculate costs
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER,
            LIGHTNING_UNLOCK_COST, LIGHTNING_BASE_COST, LIGHTNING_COST_MULTIPLIER,
            WINGMAN_UNLOCK_COST, WINGMAN_BASE_COST, WINGMAN_COST_MULTIPLIER
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

        # Lightning: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if lightning_level == 0:
            self.lightning_cost = LIGHTNING_UNLOCK_COST
        else:
            self.lightning_cost = int(LIGHTNING_BASE_COST * (LIGHTNING_COST_MULTIPLIER ** (lightning_level - 1)))
        self.can_buy_lightning = self.total_orbs >= self.lightning_cost

        # Wingman: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if wingman_level == 0:
            self.wingman_cost = WINGMAN_UNLOCK_COST
        else:
            self.wingman_cost = int(WINGMAN_BASE_COST * (WINGMAN_COST_MULTIPLIER ** (wingman_level - 1)))
        self.can_buy_wingman = self.total_orbs >= self.wingman_cost
    
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
            
            # 2x3 grid click detection
            grid_start_x = 80
            grid_start_y = 170
            btn_width = 420
            btn_height = 160
            col_gap = 80
            row_gap = 30
            
            for i in range(6):
                col = i % 2
                row = i // 2
                bx = grid_start_x + col * (btn_width + col_gap)
                by = grid_start_y + row * (btn_height + row_gap)
                
                if bx <= mx <= bx + btn_width and by <= my <= by + btn_height:
                    if i == 0 and self.can_buy_dart_speed:
                        return 'buy_dart'
                    elif i == 1 and self.can_buy_laser:
                        return 'buy_laser'
                    elif i == 2 and self.can_buy_missile:
                        return 'buy_missile'
                    elif i == 3 and self.can_buy_boomerang:
                        return 'buy_boomerang'
                    elif i == 4 and self.can_buy_lightning:
                        return 'buy_lightning'
                    elif i == 5 and self.can_buy_wingman:
                        return 'buy_wingman'
        
        return 'none'
    
    def buy_upgrade(self, upgrade_type: str) -> bool:
        """Attempt to buy an upgrade. Returns True if successful."""
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER,
            LIGHTNING_UNLOCK_COST, LIGHTNING_BASE_COST, LIGHTNING_COST_MULTIPLIER,
            WINGMAN_UNLOCK_COST, WINGMAN_BASE_COST, WINGMAN_COST_MULTIPLIER
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
        elif upgrade_type == 'lightning' and self.can_buy_lightning:
            self.total_orbs -= self.lightning_cost
            self.lightning_level += 1
            # After unlock, upgrades cost 100 * 1.5^(level-1)
            if self.lightning_level == 1:
                self.lightning_cost = LIGHTNING_BASE_COST
            else:
                self.lightning_cost = int(LIGHTNING_BASE_COST * (LIGHTNING_COST_MULTIPLIER ** (self.lightning_level - 1)))
            self.can_buy_lightning = self.total_orbs >= self.lightning_cost
            return True
        elif upgrade_type == 'wingman' and self.can_buy_wingman:
            self.total_orbs -= self.wingman_cost
            self.wingman_level += 1
            # After unlock, upgrades cost 100 * 1.5^(level-1)
            if self.wingman_level == 1:
                self.wingman_cost = WINGMAN_BASE_COST
            else:
                self.wingman_cost = int(WINGMAN_BASE_COST * (WINGMAN_COST_MULTIPLIER ** (self.wingman_level - 1)))
            self.can_buy_wingman = self.total_orbs >= self.wingman_cost
            return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the shop screen with lab/workshop style."""
        # Lab/workshop background with metal texture feel
        for y in range(SCREEN_HEIGHT):
            # Create a subtle gradient with metal-like pattern
            base = 25 + y // 50
            r = base + 5
            g = base + 8
            b = base + 15
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw workbench texture lines
        for i in range(0, SCREEN_HEIGHT, 60):
            pygame.draw.line(surface, (35, 35, 45), (0, i), (SCREEN_WIDTH, i), 1)
        
        font_large = pygame.font.Font(None, 80)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Workshop header banner
        banner_y = 30
        pygame.draw.rect(surface, (50, 45, 40), (50, banner_y, SCREEN_WIDTH - 100, 70))
        pygame.draw.rect(surface, (120, 100, 80), (50, banner_y, SCREEN_WIDTH - 100, 70), 3)
        # Metal rivets
        for rx in range(70, SCREEN_WIDTH - 70, 60):
            pygame.draw.circle(surface, (80, 70, 60), (rx, banner_y + 10), 6)
            pygame.draw.circle(surface, (100, 90, 80), (rx, banner_y + 10), 3)
        
        # Title
        title = font_large.render("WEAPON WORKSHOP", True, (200, 180, 150))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, banner_y + 35))
        surface.blit(title, title_rect)
        
        # Orb display - looks like a coin purse
        orb_x = SCREEN_WIDTH - 150
        orb_y = 120
        pygame.draw.ellipse(surface, (60, 50, 40), (orb_x - 50, orb_y - 25, 100, 50))
        pygame.draw.ellipse(surface, (100, 80, 60), (orb_x - 50, orb_y - 25, 100, 50), 3)
        pygame.draw.circle(surface, COLOR_YELLOW, (orb_x, orb_y), 20)
        pygame.draw.circle(surface, COLOR_BLACK, (orb_x, orb_y), 20, 2)
        orb_text = font_small.render(f"{self.total_orbs}", True, COLOR_BLACK)
        orb_text_rect = orb_text.get_rect(center=(orb_x, orb_y))
        surface.blit(orb_text, orb_text_rect)
        orbs_label = font_tiny.render("ORBS", True, (150, 140, 130))
        surface.blit(orbs_label, (orb_x + 30, orb_y - 10))
        
        # Back button - styled like a metal button
        back_x, back_y = 60, 110
        pygame.draw.rect(surface, (60, 55, 50), (back_x, back_y, 80, 35))
        pygame.draw.rect(surface, (100, 90, 80), (back_x, back_y, 80, 35), 2)
        back_text = font_small.render("BACK", True, (200, 190, 180))
        surface.blit(back_text, (back_x + 15, back_y + 8))
        
        # Upgrade items in 2x3 grid
        items = [
            ("Dart Speed +20%", self.dart_speed_level, self.dart_speed_cost, 
             self.can_buy_dart_speed, COLOR_WHITE, 
             "Increases dart speed by 20% per level"),
            ("Laser Beam", self.laser_level, self.laser_cost,
             self.can_buy_laser, COLOR_CYAN,
             "Fires a laser that damages balloons over time"),
            ("Missiles", self.missile_level, self.missile_cost,
             self.can_buy_missile, COLOR_ORANGE,
             "Launches missiles with area damage"),
            ("Boomerang", self.boomerang_level, self.boomerang_cost,
             self.can_buy_boomerang, COLOR_BROWN,
             "Adds orbiting boomerangs that damage balloons"),
            ("Lightning", self.lightning_level, self.lightning_cost,
             self.can_buy_lightning, (180, 120, 255),
             "Strikes closest balloon and arcs to nearby ones"),
            ("Wingman Aces", self.wingman_level, self.wingman_cost,
             self.can_buy_wingman, (255, 120, 120),
             "Deploys ally planes that shoot at closest balloons")
        ]
        
        # 2x3 grid layout
        grid_start_x = 80
        grid_start_y = 170
        btn_width = 420
        btn_height = 160
        col_gap = 80
        row_gap = 30
        
        # Get mouse position for hover
        mx, my = pygame.mouse.get_pos()
        hovered_item = None
        
        for i, (name, level, cost, can_buy, color, description) in enumerate(items):
            col = i % 2
            row = i // 2
            bx = grid_start_x + col * (btn_width + col_gap)
            by = grid_start_y + row * (btn_height + row_gap)
            
            is_selected = (i == self.selected_option)
            is_hovered = (bx <= mx <= bx + btn_width and by <= my <= by + btn_height)
            
            if is_hovered:
                hovered_item = (i, name, level, cost, color, description, can_buy)
            
            # Button background - lab workbench style
            if can_buy:
                base_bg = (55, 60, 75)
                border_color = color
            else:
                base_bg = (35, 38, 45)
                border_color = (60, 60, 70)
            
            if is_hovered and can_buy:
                base_bg = (65, 70, 85)
            
            # Metal button with depth
            pygame.draw.rect(surface, (20, 20, 25), (bx + 4, by + 4, btn_width, btn_height))
            pygame.draw.rect(surface, base_bg, (bx, by, btn_width, btn_height))
            
            # Metal border with rivets
            pygame.draw.rect(surface, border_color, (bx, by, btn_width, btn_height), 3)
            # Corner rivets
            rivet_size = 6
            for rx, ry in [(bx + 10, by + 10), (bx + btn_width - 10, by + 10),
                          (bx + 10, by + btn_height - 10), (bx + btn_width - 10, by + btn_height - 10)]:
                pygame.draw.circle(surface, (80, 75, 70), (rx, ry), rivet_size)
                pygame.draw.circle(surface, (120, 115, 110), (rx, ry), rivet_size - 2)
            
            # Large icon on left side
            icon_x = bx + 60
            icon_y = by + btn_height // 2
            self._draw_large_icon(surface, icon_x, icon_y, i, color, can_buy)
            
            # Info on right side
            info_x = bx + 140
            info_y = by + 25
            
            # Name
            name_text = font_medium.render(name, True, color if can_buy else (100, 100, 110))
            surface.blit(name_text, (info_x, info_y))
            
            # Level badge
            if level == 0:
                level_text = "LOCKED"
                level_color = (180, 80, 80)
            else:
                level_text = f"LEVEL {level}"
                level_color = (100, 200, 100)
            level_badge = font_tiny.render(level_text, True, level_color)
            surface.blit(level_badge, (info_x, info_y + 40))
            
            # Cost
            if can_buy:
                cost_text = font_small.render(f"{cost} ORBS", True, COLOR_YELLOW)
            else:
                cost_text = font_small.render(f"{cost} ORBS", True, (80, 80, 80))
            surface.blit(cost_text, (info_x, info_y + 70))
            
            # Buy/Upgrade indicator
            if can_buy:
                if level == 0:
                    action_text = "CLICK TO UNLOCK"
                else:
                    action_text = "CLICK TO UPGRADE"
                action_color = (100, 200, 100)
            else:
                action_text = "NEED MORE ORBS"
                action_color = (150, 80, 80)
            action_badge = font_tiny.render(action_text, True, action_color)
            surface.blit(action_badge, (info_x, info_y + 100))
        
        # Tooltip panel on right side
        tooltip_x = 1000
        tooltip_y = 170
        tooltip_w = 250
        tooltip_h = 350
        
        if hovered_item:
            _, name, level, cost, color, description, can_buy = hovered_item
            
            # Tooltip background - parchment/lab note style
            pygame.draw.rect(surface, (45, 42, 38), (tooltip_x, tooltip_y, tooltip_w, tooltip_h))
            pygame.draw.rect(surface, (100, 90, 80), (tooltip_x, tooltip_y, tooltip_w, tooltip_h), 3)
            
            # Header
            header_text = font_small.render("WEAPON INFO", True, (180, 170, 160))
            surface.blit(header_text, (tooltip_x + 20, tooltip_y + 15))
            
            # Divider
            pygame.draw.line(surface, (80, 70, 60), (tooltip_x + 10, tooltip_y + 45),
                           (tooltip_x + tooltip_w - 10, tooltip_y + 45), 1)
            
            # Weapon name
            weapon_name = font_medium.render(name, True, color)
            surface.blit(weapon_name, (tooltip_x + 20, tooltip_y + 60))
            
            # Current level
            if level == 0:
                level_info = "Not Acquired"
            else:
                level_info = f"Current: Level {level}"
            level_info_text = font_tiny.render(level_info, True, (150, 150, 160))
            surface.blit(level_info_text, (tooltip_x + 20, tooltip_y + 100))
            
            # Description
            # Word wrap description
            words = description.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if font_tiny.size(test_line)[0] < tooltip_w - 40:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            desc_y = tooltip_y + 130
            for line in lines:
                desc_text = font_tiny.render(line, True, (170, 170, 180))
                surface.blit(desc_text, (tooltip_x + 20, desc_y))
                desc_y += 25
            
            # Stats section
            pygame.draw.line(surface, (80, 70, 60), (tooltip_x + 10, tooltip_y + 220),
                           (tooltip_x + tooltip_w - 10, tooltip_y + 220), 1)
            
            stats_title = font_tiny.render("STATS:", True, (180, 170, 160))
            surface.blit(stats_title, (tooltip_x + 20, tooltip_y + 235))
            
            # Show specific stats based on weapon
            stats_y = tooltip_y + 260
            if "Dart" in name:
                stats = ["+20% speed per level", "Fires from both wings", "Fast cooldown"]
            elif "Laser" in name:
                stats = ["Continuous beam", "-15% cooldown per level", "Destroys layers over time"]
            elif "Missile" in name:
                stats = ["Area damage", "+15% AOE per level", "3 second cooldown"]
            elif "Boomerang" in name:
                stats = ["Orbits player", "Pierces balloons", "+1 per level"]
            elif "Lightning" in name:
                stats = ["Targets closest balloon", "+2 arcs per level", "-10% cooldown per level"]
            elif "Wingman" in name:
                stats = ["Ally planes", "Shoots at half rate", "Targets closest balloon"]
            else:
                stats = []
            
            for stat in stats:
                stat_text = font_tiny.render("• " + stat, True, (160, 160, 170))
                surface.blit(stat_text, (tooltip_x + 25, stats_y))
                stats_y += 22
        
        # Instructions
        instr = font_small.render("Hover for details | Click to buy | ESC to go back", True, (130, 130, 140))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(instr, instr_rect)
    
    def _draw_large_icon(self, surface: pygame.Surface, cx: int, cy: int, index: int, color: tuple, can_buy: bool) -> None:
        """Draw a large icon for each upgrade in the workshop."""
        alpha = 255 if can_buy else 100
        
        if index == 0:  # Dart
            # Large dart
            pygame.draw.polygon(surface, color, [
                (cx, cy - 30), (cx + 10, cy - 5), (cx + 5, cy - 5),
                (cx + 5, cy + 20), (cx - 5, cy + 20),
                (cx - 5, cy - 5), (cx - 10, cy - 5)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 30), (cx + 10, cy - 5), (cx + 5, cy - 5),
                (cx + 5, cy + 20), (cx - 5, cy + 20),
                (cx - 5, cy - 5), (cx - 10, cy - 5)
            ], 2)
            pygame.draw.polygon(surface, COLOR_YELLOW, [
                (cx, cy - 30), (cx + 10, cy - 5), (cx - 10, cy - 5)
            ])
            pygame.draw.rect(surface, (200, 50, 50), (cx - 6, cy + 18, 12, 6))
            
        elif index == 1:  # Laser
            # Laser beam
            pygame.draw.line(surface, color, (cx, cy - 40), (cx, cy + 40), 8)
            pygame.draw.line(surface, COLOR_WHITE, (cx, cy - 40), (cx, cy + 40), 4)
            pygame.draw.circle(surface, color, (cx, cy), 15)
            pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), 8)
            
        elif index == 2:  # Missile
            pygame.draw.rect(surface, COLOR_WHITE, (cx - 8, cy - 20, 16, 40))
            pygame.draw.rect(surface, (230, 230, 230), (cx - 8, cy - 20, 4, 40))
            pygame.draw.polygon(surface, COLOR_RED, [
                (cx, cy - 28), (cx - 8, cy - 20), (cx + 8, cy - 20)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 28), (cx - 8, cy - 20), (cx + 8, cy - 20)
            ], 1)
            pygame.draw.circle(surface, (255, 150, 50), (cx, cy + 25), 8)
            pygame.draw.circle(surface, (255, 255, 200), (cx, cy + 25), 4)
            
        elif index == 3:  # Boomerang
            pygame.draw.polygon(surface, color, [
                (cx, cy - 25), (cx + 25, cy + 25), (cx, cy + 10), (cx - 25, cy + 25)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 25), (cx + 25, cy + 25), (cx, cy + 10), (cx - 25, cy + 25)
            ], 2)
            pygame.draw.line(surface, (100, 60, 30), (cx - 20, cy + 5), (cx + 20, cy + 5), 2)
            pygame.draw.line(surface, (100, 60, 30), (cx - 15, cy + 15), (cx + 15, cy + 15), 2)
            
        elif index == 4:  # Lightning
            pygame.draw.line(surface, (210, 160, 255), (cx - 15, cy - 35), (cx + 5, cy - 5), 10)
            pygame.draw.line(surface, (210, 160, 255), (cx + 5, cy - 5), (cx - 5, cy + 30), 10)
            pygame.draw.line(surface, color, (cx - 12, cy - 30), (cx + 5, cy - 5), 6)
            pygame.draw.line(surface, color, (cx + 5, cy - 5), (cx - 2, cy + 25), 6)
            pygame.draw.line(surface, COLOR_WHITE, (cx - 12, cy - 30), (cx + 5, cy - 5), 2)
            pygame.draw.line(surface, COLOR_WHITE, (cx + 5, cy - 5), (cx - 2, cy + 25), 2)
            
        elif index == 5:  # Wingman
            # Larger wingman plane
            pygame.draw.circle(surface, (255, 80, 80, 80), (cx, cy), 35)
            pygame.draw.rect(surface, color, (cx - 25, cy - 5, 50, 10))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 25, cy - 5, 50, 10), 2)
            pygame.draw.rect(surface, color, (cx - 8, cy - 20, 16, 40))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 8, cy - 20, 16, 40), 2)
            pygame.draw.polygon(surface, COLOR_WHITE, [
                (cx, cy - 28), (cx - 8, cy - 20), (cx + 8, cy - 20)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 28), (cx - 8, cy - 20), (cx + 8, cy - 20)
            ], 1)
            pygame.draw.rect(surface, (100, 200, 255), (cx - 5, cy - 12, 10, 10))
            pygame.draw.line(surface, (200, 200, 200), (cx - 12, cy - 26), (cx + 12, cy - 26), 3)
            pygame.draw.line(surface, (200, 200, 200), (cx, cy - 30), (cx, cy - 22), 3)
    
    def _draw_icon(self, surface: pygame.Surface, cx: int, cy: int, index: int) -> None:
        """Draw an enhanced small icon for each upgrade."""
        if index == 0:  # Dart - detailed arrow
            # Glow
            pygame.draw.polygon(surface, (255, 255, 255, 100), [
                (cx, cy - 12), (cx + 5, cy - 2), (cx + 2, cy - 2),
                (cx + 2, cy + 10), (cx - 2, cy + 10),
                (cx - 2, cy - 2), (cx - 5, cy - 2)
            ])
            # Main dart
            pygame.draw.polygon(surface, COLOR_WHITE, [
                (cx, cy - 10), (cx + 4, cy - 2), (cx + 2, cy - 2),
                (cx + 2, cy + 8), (cx - 2, cy + 8),
                (cx - 2, cy - 2), (cx - 4, cy - 2)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 10), (cx + 4, cy - 2), (cx + 2, cy - 2),
                (cx + 2, cy + 8), (cx - 2, cy + 8),
                (cx - 2, cy - 2), (cx - 4, cy - 2)
            ], 1)
            # Yellow tip
            pygame.draw.polygon(surface, COLOR_YELLOW, [
                (cx, cy - 10), (cx + 4, cy - 2), (cx - 4, cy - 2)
            ])
            # Red fletching
            pygame.draw.rect(surface, (200, 50, 50), (cx - 4, cy + 6, 8, 4))
            
        elif index == 1:  # Laser - glowing beam
            # Outer glow
            pygame.draw.line(surface, (0, 200, 255), (cx, cy - 18), (cx, cy + 18), 6)
            # Main beam
            pygame.draw.line(surface, COLOR_CYAN, (cx, cy - 15), (cx, cy + 15), 4)
            # Inner core
            pygame.draw.line(surface, COLOR_WHITE, (cx, cy - 15), (cx, cy + 15), 2)
            # Energy orb at center
            pygame.draw.circle(surface, COLOR_CYAN, (cx, cy), 8)
            pygame.draw.circle(surface, COLOR_WHITE, (cx, cy), 4)
            # Sparkles
            pygame.draw.circle(surface, (255, 255, 255), (cx - 2, cy - 2), 2)
            
        elif index == 2:  # Missile - detailed rocket
            # Body
            pygame.draw.rect(surface, COLOR_WHITE, (cx - 4, cy - 10, 8, 20))
            # Metallic shine
            pygame.draw.rect(surface, (230, 230, 230), (cx - 4, cy - 10, 2, 20))
            # Red nose cone
            pygame.draw.polygon(surface, COLOR_RED, [
                (cx, cy - 14), (cx - 4, cy - 10), (cx + 4, cy - 10)
            ])
            pygame.draw.polygon(surface, COLOR_BLACK, [
                (cx, cy - 14), (cx - 4, cy - 10), (cx + 4, cy - 10)
            ], 1)
            # Fins
            pygame.draw.polygon(surface, (180, 50, 50), [
                (cx - 4, cy + 6), (cx - 8, cy + 12), (cx - 4, cy + 10)
            ])
            pygame.draw.polygon(surface, (180, 50, 50), [
                (cx + 4, cy + 6), (cx + 8, cy + 12), (cx + 4, cy + 10)
            ])
            # Exhaust
            pygame.draw.circle(surface, (255, 150, 50), (cx, cy + 12), 4)
            pygame.draw.circle(surface, (255, 255, 200), (cx, cy + 12), 2)
            
        elif index == 3:  # Boomerang - detailed V
            # Outer glow
            pygame.draw.polygon(surface, (139, 69, 19, 80), [
                (cx, cy - 12), (cx + 12, cy + 12), (cx, cy + 6), (cx - 12, cy + 12)
            ])
            # Main shape
            points = [(cx, cy - 10), (cx + 10, cy + 10), (cx, cy + 4), (cx - 10, cy + 10)]
            pygame.draw.polygon(surface, COLOR_BROWN, points)
            # Wood grain
            pygame.draw.line(surface, (100, 60, 30), (cx - 8, cy + 2), (cx + 8, cy + 2), 1)
            pygame.draw.line(surface, (100, 60, 30), (cx - 6, cy + 6), (cx + 6, cy + 6), 1)
            # Black border
            pygame.draw.polygon(surface, COLOR_BLACK, points, 2)
            # Highlight
            pygame.draw.line(surface, (180, 100, 60), (cx - 8, cy - 8), (cx + 8, cy - 8), 2)

        elif index == 4:  # Lightning icon
            # Outer glow
            pygame.draw.line(surface, (210, 160, 255), (cx - 8, cy - 14), (cx + 2, cy - 2), 5)
            pygame.draw.line(surface, (210, 160, 255), (cx + 2, cy - 2), (cx - 2, cy + 12), 5)
            # Main bolt
            pygame.draw.line(surface, (160, 90, 255), (cx - 6, cy - 12), (cx + 2, cy - 2), 3)
            pygame.draw.line(surface, (160, 90, 255), (cx + 2, cy - 2), (cx - 1, cy + 10), 3)
            # Inner core
            pygame.draw.line(surface, COLOR_WHITE, (cx - 6, cy - 12), (cx + 2, cy - 2), 1)
            pygame.draw.line(surface, COLOR_WHITE, (cx + 2, cy - 2), (cx - 1, cy + 10), 1)
            # Sparkle
            pygame.draw.circle(surface, COLOR_WHITE, (cx - 2, cy - 6), 2)

        elif index == 5:  # Wingman icon
            # Glow
            pygame.draw.circle(surface, (255, 120, 120), (cx, cy), 12)
            # Wings
            pygame.draw.rect(surface, COLOR_RED, (cx - 10, cy - 2, 20, 4))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 10, cy - 2, 20, 4), 1)
            # Body
            pygame.draw.rect(surface, COLOR_RED, (cx - 3, cy - 8, 6, 16))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 3, cy - 8, 6, 16), 1)
            # Propeller
            pygame.draw.line(surface, COLOR_WHITE, (cx - 6, cy - 10), (cx + 6, cy - 10), 2)
            pygame.draw.line(surface, COLOR_WHITE, (cx, cy - 14), (cx, cy - 6), 2)
