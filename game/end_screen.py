"""End-of-Level Screen - Separate page shown after completing a level."""

import pygame
import math
import random
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_CYAN, COLOR_ORANGE,
    UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
    LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
    MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
    BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER,
    LIGHTNING_UNLOCK_COST, LIGHTNING_BASE_COST, LIGHTNING_COST_MULTIPLIER,
    LIGHTNING_STRIKE_COLOR, LIGHTNING_GLOW_COLOR,
    WINGMAN_UNLOCK_COST, WINGMAN_BASE_COST, WINGMAN_COST_MULTIPLIER,
    COLOR_BROWN
)

class EndScreen:
    """End-of-level screen showing orbs collected, upgrades, and next level option."""
    
    def __init__(self, orbs_collected: int, level_num: int, has_next: bool, 
                 total_orbs: int = 0, dart_speed_level: int = 0, laser_level: int = 0,
                 missile_level: int = 0, boomerang_level: int = 0, lightning_level: int = 0,
                 wingman_level: int = 0, stars_earned: int = 0, perfect: bool = False,
                 popped_ratio: float = 0.0):
        self.orbs_collected = orbs_collected
        self.level_num = level_num
        self.has_next = has_next
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.missile_level = missile_level
        self.boomerang_level = boomerang_level
        self.lightning_level = lightning_level
        self.wingman_level = wingman_level
        self.stars_earned = stars_earned
        self.perfect = perfect
        self.popped_ratio = popped_ratio
        self.selected_option = 0  # 0 = next level, 1 = quit
        self.star_fx_time = 0.0
        self.star_sparkles = []
        self.show_upgrades = False
        
        # Upgrade state - Dart: unlocked from beginning, upgrades start at 100, increase by 50%
        self.dart_speed_cost = int(UPGRADE_DART_SPEED_BASE_COST * (UPGRADE_DART_SPEED_COST_MULTIPLIER ** dart_speed_level))
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
        
        # Upgrade layout: 2 columns x 3 rows
        self.upgrade_cols = 2
        self.upgrade_rows = 3
        self.upgrade_size = 180 # Larger icons
        self.upgrade_spacing_x = 250
        self.upgrade_spacing_y = 250
        self.upgrade_start_x = (SCREEN_WIDTH - (self.upgrade_cols * self.upgrade_spacing_x)) // 2 + 35
        self.upgrade_start_y = 350
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'next', 'menu', 'quit', 'buy_dart', 'buy_laser', 'buy_missile', 'buy_boomerang', 'buy_lightning', 'buy_wingman', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.show_upgrades = True
            if not self.show_upgrades:
                return 'none'
            if event.key == pygame.K_ESCAPE:
                return 'menu'
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:
                    return 'next' if self.has_next else 'menu'
                else:
                    return 'menu'
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.selected_option = 1 - self.selected_option
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.show_upgrades = True
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
                        elif i == 3 and self.can_buy_boomerang:
                            return 'buy_boomerang'
                        elif i == 4 and self.can_buy_lightning:
                            return 'buy_lightning'
                        elif i == 5 and self.can_buy_wingman:
                            return 'buy_wingman'
                        return 'none'
            
            # Check next/menu buttons
            btn_x = SCREEN_WIDTH // 2 - 100
            btn_y = self.upgrade_start_y + self.upgrade_rows * self.upgrade_spacing_y + 20
            if btn_x <= mx <= btn_x + 200:
                if btn_y <= my <= btn_y + 50:
                    return 'next' if self.has_next else 'menu'
                elif btn_y + 60 <= my <= btn_y + 110:
                    return 'menu'
        
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
        
        # Stars summary
        self._update_star_fx()
        self._draw_star_summary(surface, font_medium, font_small)
        
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
        
        if not self.show_upgrades:
            self._draw_star_prompt(surface, font_small)
            return
        
        # Upgrade section
        upgrade_title = font_medium.render("UPGRADES", True, COLOR_WHITE)
        surface.blit(upgrade_title, (self.upgrade_start_x, self.upgrade_start_y - 60))
        
        # 6 Upgrade buttons in 2x3 layout
        upgrade_info = [
            ("Dart Speed", self.dart_speed_level, self.dart_speed_cost, self.can_buy_dart_speed, self._draw_dart_icon),
            ("Laser Beam", self.laser_level, self.laser_cost, self.can_buy_laser, self._draw_laser_icon),
            ("Missiles", self.missile_level, self.missile_cost, self.can_buy_missile, self._draw_missile_icon),
            ("Boomerang", self.boomerang_level, self.boomerang_cost, self.can_buy_boomerang, self._draw_boomerang_icon),
            ("Lightning", self.lightning_level, self.lightning_cost, self.can_buy_lightning, self._draw_lightning_icon),
            ("Wingman Aces", self.wingman_level, self.wingman_cost, self.can_buy_wingman, self._draw_wingman_icon)
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
                # Name and Level/Status
                if level == 0:
                    status_text = "Unlock"
                else:
                    status_text = f"Lv.{level}"
                name_text = font_tiny.render(f"{name} {status_text}", True, COLOR_WHITE)
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
        
        # Main Menu button
        menu_color = COLOR_CYAN if self.selected_option == 1 else (100, 100, 100)
        pygame.draw.rect(surface, menu_color, (btn_x, btn_y, btn_width, btn_height))
        pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, btn_width, btn_height), 3)
        menu_text = font_medium.render("MAIN MENU", True, COLOR_BLACK)
        text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, btn_y + 25))
        surface.blit(menu_text, text_rect)
        
        # Instructions
        instr = font_small.render("Click upgrade to buy | Arrow keys + ENTER for navigation", True, (150, 150, 150))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(instr, instr_rect)
    
    def _update_star_fx(self) -> None:
        """Update star sparkle animations."""
        now = pygame.time.get_ticks() / 1000.0
        last_tick = getattr(self, "_last_star_tick", now)
        dt = now - last_tick
        self._last_star_tick = now
        self.star_fx_time += dt
        
        if not self.star_sparkles:
            return
        
        updated = []
        for sparkle in self.star_sparkles:
            sparkle["life"] -= dt
            if sparkle["life"] <= 0:
                continue
            sparkle["x"] += sparkle["vx"] * dt
            sparkle["y"] += sparkle["vy"] * dt
            sparkle["vy"] += 25 * dt
            sparkle["alpha"] = max(0, sparkle["alpha"] - dt * 160)
            updated.append(sparkle)
        self.star_sparkles = updated
    
    def _emit_star_sparkle(self, cx: float, cy: float, color: tuple) -> None:
        """Spawn a sparkle near a star."""
        if random.random() > 0.08:
            return
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(15, 40)
        self.star_sparkles.append({
            "x": cx + random.uniform(-6, 6),
            "y": cy + random.uniform(-6, 6),
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed - 20,
            "life": random.uniform(0.4, 0.9),
            "size": random.randint(2, 4),
            "color": color,
            "alpha": 200
        })
    
    def _draw_star_summary(self, surface: pygame.Surface, font_medium: pygame.font.Font, font_small: pygame.font.Font) -> None:
        """Draw the stars earned popup."""
        panel_w = 460
        panel_h = 160
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = 115
        
        # Panel with depth
        pygame.draw.rect(surface, (10, 10, 15), (panel_x + 5, panel_y + 5, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(surface, (32, 34, 50), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(surface, (90, 95, 120), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)
        
        header = font_medium.render("STARS EARNED", True, COLOR_WHITE)
        header_rect = header.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
        surface.blit(header, header_rect)
        
        base_color = COLOR_WHITE if self.perfect and self.stars_earned >= 3 else COLOR_YELLOW
        spacing = 75
        star_y = panel_y + 90
        
        for i in range(3):
            star_x = SCREEN_WIDTH // 2 - spacing + i * spacing
            filled = i < self.stars_earned
            if filled:
                pulse = 1.0 + 0.05 * math.sin(self.star_fx_time * 3.5 + i)
                self._draw_star(surface, star_x, star_y, 24 * pulse, base_color, hollow=False)
                self._emit_star_sparkle(star_x, star_y, base_color)
            else:
                self._draw_star(surface, star_x, star_y, 22, (160, 165, 190), hollow=True)
        
        percent = int(self.popped_ratio * 100)
        detail_color = (220, 220, 230) if not self.perfect else COLOR_CYAN
        detail = font_small.render(f"Pop Accuracy: {percent}%", True, detail_color)
        detail_rect = detail.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 132))
        surface.blit(detail, detail_rect)
        
        if self.perfect:
            tag = font_small.render("PERFECT CLEAR!", True, COLOR_WHITE)
            tag_rect = tag.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 17))
            surface.blit(tag, tag_rect)
        
        for sparkle in self.star_sparkles:
            alpha = int(max(0, min(255, sparkle["alpha"])))
            sparkle_color = (*sparkle["color"], alpha)
            sparkle_surface = pygame.Surface((sparkle["size"] * 2 + 2, sparkle["size"] * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(
                sparkle_surface,
                sparkle_color,
                (sparkle["size"] + 1, sparkle["size"] + 1),
                sparkle["size"]
            )
            surface.blit(sparkle_surface, (sparkle["x"], sparkle["y"]))
    
    def _draw_star_prompt(self, surface: pygame.Surface, font_small: pygame.font.Font) -> None:
        """Draw hint to proceed to upgrades."""
        prompt_text = "Press ENTER to continue to upgrades"
        color = (200, 200, 220)
        pulse = 0.7 + 0.3 * math.sin(self.star_fx_time * 3.5)
        color = (int(color[0] * pulse), int(color[1] * pulse), int(color[2] * pulse))
        prompt = font_small.render(prompt_text, True, color)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 295))
        surface.blit(prompt, prompt_rect)
    
    def _draw_star(self, surface: pygame.Surface, cx: float, cy: float, radius: float, color: tuple, hollow: bool = False) -> None:
        """Draw a stylized star with optional glow."""
        radius = max(6, radius)
        glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        glow_color = (*color, 80) if not hollow else (0, 0, 0, 0)
        if not hollow:
            pygame.draw.circle(glow_surface, glow_color, (radius * 2, radius * 2), int(radius * 1.2))
            surface.blit(glow_surface, (cx - radius * 2, cy - radius * 2))
        
        points = []
        inner = radius * 0.5
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = radius if i % 2 == 0 else inner
            points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
        
        if hollow:
            pygame.draw.polygon(surface, color, points, 2)
        else:
            shadow_points = [(x + 2, y + 2) for x, y in points]
            pygame.draw.polygon(surface, (20, 20, 30), shadow_points)
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, COLOR_BLACK, points, 1)
    
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

    def _draw_boomerang_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a boomerang icon."""
        w, h = 20 * scale, 20 * scale
        points = [
            (cx, cy - h),
            (cx + w, cy + h),
            (cx, cy + h // 2),
            (cx - w, cy + h)
        ]
        pygame.draw.polygon(surface, COLOR_BROWN, points)
        pygame.draw.polygon(surface, COLOR_BLACK, points, 2)

    def _draw_lightning_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a lightning icon."""
        glow_color = (*LIGHTNING_GLOW_COLOR, 180)
        bolt_color = LIGHTNING_STRIKE_COLOR
        # Glow bolts
        pygame.draw.line(surface, glow_color, (cx - 12 * scale, cy - 18 * scale), (cx + 3 * scale, cy - 2 * scale), int(5 * scale))
        pygame.draw.line(surface, glow_color, (cx + 3 * scale, cy - 2 * scale), (cx - 2 * scale, cy + 16 * scale), int(5 * scale))
        # Main bolt
        pygame.draw.line(surface, bolt_color, (cx - 10 * scale, cy - 16 * scale), (cx + 3 * scale, cy - 2 * scale), int(3 * scale))
        pygame.draw.line(surface, bolt_color, (cx + 3 * scale, cy - 2 * scale), (cx - 1 * scale, cy + 14 * scale), int(3 * scale))
        # Core
        pygame.draw.line(surface, COLOR_WHITE, (cx - 10 * scale, cy - 16 * scale), (cx + 3 * scale, cy - 2 * scale), int(1 * scale))
        pygame.draw.line(surface, COLOR_WHITE, (cx + 3 * scale, cy - 2 * scale), (cx - 1 * scale, cy + 14 * scale), int(1 * scale))
        # Sparkle
        pygame.draw.circle(surface, COLOR_WHITE, (cx - 2 * scale, cy - 8 * scale), int(2 * scale))

    def _draw_wingman_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a wingman ace icon."""
        # Glow
        pygame.draw.circle(surface, (255, 120, 120), (cx, cy), int(14 * scale))
        # Wings
        pygame.draw.rect(surface, COLOR_RED, (cx - 12 * scale, cy - 3 * scale, 24 * scale, 6 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 12 * scale, cy - 3 * scale, 24 * scale, 6 * scale), 1)
        # Body
        pygame.draw.rect(surface, COLOR_RED, (cx - 4 * scale, cy - 10 * scale, 8 * scale, 20 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 4 * scale, cy - 10 * scale, 8 * scale, 20 * scale), 1)
        # Propeller
        pygame.draw.line(surface, COLOR_WHITE, (cx - 8 * scale, cy - 12 * scale), (cx + 8 * scale, cy - 12 * scale), max(1, int(2 * scale)))
        pygame.draw.line(surface, COLOR_WHITE, (cx, cy - 16 * scale), (cx, cy - 8 * scale), max(1, int(2 * scale)))

    def _draw_locked_icon(self, surface: pygame.Surface, cx: int, cy: int, scale: float = 1.0) -> None:
        """Draw a locked padlock icon."""
        # Lock body
        pygame.draw.rect(surface, (100, 100, 100), (cx - 12 * scale, cy - 5 * scale, 24 * scale, 20 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (cx - 12 * scale, cy - 5 * scale, 24 * scale, 20 * scale), 2)
        # Lock shackle
        pygame.draw.arc(surface, (100, 100, 100), (cx - 10 * scale, cy - 20 * scale, 20 * scale, 20 * scale), 0, 3.14, int(3 * scale))
        # Keyhole
        pygame.draw.circle(surface, COLOR_BLACK, (cx, cy + 5 * scale), int(4 * scale))
