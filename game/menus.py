"""Menu screens for the game - Main Menu, Level Select, and Shop."""

import pygame
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_CYAN, COLOR_ORANGE,
    COLOR_BROWN, COLOR_BLUE, COLOR_PINK
)
from game.level_manager import LevelManager


class MainMenu:
    """Main menu screen with Play, Shop, and Quit options and animated background."""
    
    def __init__(self):
        self.selected_option = 0  # 0 = Play, 1 = Shop, 2 = Quit
        self._init_animations()
    
    def _init_animations(self):
        """Initialize animated elements."""
        import random
        self.time_offset = random.randint(0, 10000)
        
        # Floating balloons with different properties
        self.balloons = []
        balloon_colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_ORANGE, COLOR_CYAN]
        for i in range(15):
            self.balloons.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(100, SCREEN_HEIGHT - 150),
                'size': random.randint(20, 40),
                'color': random.choice(balloon_colors),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.5, -0.2),  # Float upward
                'bob_phase': random.uniform(0, 6.28),
                'bob_speed': random.uniform(0.5, 1.5),
                'bob_amplitude': random.uniform(10, 25)
            })
        
        # Flying planes
        self.planes = []
        for i in range(4):
            direction = 1 if i % 2 == 0 else -1
            self.planes.append({
                'x': -100 if direction == 1 else SCREEN_WIDTH + 100,
                'y': random.randint(150, SCREEN_HEIGHT - 200),
                'direction': direction,
                'speed': random.uniform(1.5, 3.0),
                'size': random.uniform(0.8, 1.2),
                'color': random.choice([COLOR_RED, COLOR_BLUE, (100, 200, 100), (200, 150, 50)])
            })
        
        # Clouds for depth
        self.clouds = []
        for i in range(8):
            self.clouds.append({
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(50, SCREEN_HEIGHT - 300),
                'size': random.randint(60, 120),
                'speed': random.uniform(0.1, 0.3)
            })
        
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
    
    def _update_animations(self):
        """Update all animated elements."""
        import math
        t = pygame.time.get_ticks() / 1000.0
        
        # Update balloons
        for balloon in self.balloons:
            balloon['x'] += balloon['vx']
            balloon['y'] += balloon['vy'] + math.sin(t * balloon['bob_speed'] + balloon['bob_phase']) * 0.1
            
            # Bobbing motion
            balloon['y'] += math.sin(t * balloon['bob_speed'] + balloon['bob_phase']) * balloon['bob_amplitude'] * 0.02
            
            # Wrap around screen
            if balloon['x'] < -50:
                balloon['x'] = SCREEN_WIDTH + 50
            elif balloon['x'] > SCREEN_WIDTH + 50:
                balloon['x'] = -50
            if balloon['y'] < -50:
                balloon['y'] = SCREEN_HEIGHT + 50
        
        # Update planes
        for plane in self.planes:
            plane['x'] += plane['speed'] * plane['direction']
            # Slight sine wave for flight path
            plane['y'] += math.sin(t * 0.5 + plane['x'] * 0.01) * 0.3
            
            # Wrap around
            if plane['direction'] == 1 and plane['x'] > SCREEN_WIDTH + 150:
                plane['x'] = -150
                plane['y'] = (plane['y'] + 200) % (SCREEN_HEIGHT - 300) + 100
            elif plane['direction'] == -1 and plane['x'] < -150:
                plane['x'] = SCREEN_WIDTH + 150
                plane['y'] = (plane['y'] + 200) % (SCREEN_HEIGHT - 300) + 100
        
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > SCREEN_WIDTH + 150:
                cloud['x'] = -150
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu with animated background."""
        # Update animations
        self._update_animations()
        
        # Dark sky background with gradient
        for y in range(SCREEN_HEIGHT):
            color = (10 + y // 30, 15 + y // 25, 30 + y // 20)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw clouds in background
        for cloud in self.clouds:
            self._draw_cloud(surface, cloud['x'], cloud['y'], cloud['size'])
        
        # Draw floating balloons (behind title card)
        for balloon in self.balloons:
            self._draw_animated_balloon(surface, int(balloon['x']), int(balloon['y']), 
                                        balloon['color'], balloon['size'])
        
        # Draw flying planes (behind title card)
        for plane in self.planes:
            self._draw_flying_plane(surface, int(plane['x']), int(plane['y']), 
                                    plane['direction'], plane['size'], plane['color'])
        
        # Draw stars with twinkle effect
        t = pygame.time.get_ticks()
        for i in range(60):
            star_x = (t // 50 + i * 137) % SCREEN_WIDTH
            star_y = (i * 83) % SCREEN_HEIGHT
            # Twinkle effect
            twinkle = (t // 100 + i * 47) % 200
            if twinkle > 100:
                brightness = 200 - twinkle + 55
            else:
                brightness = twinkle + 55
            size = 1 if (t // 500 + i) % 3 != 0 else 2
            pygame.draw.circle(surface, (brightness, brightness, brightness), (star_x, star_y), size)
        
        font_title = pygame.font.Font(None, 140)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Title card background with glow
        card_x = SCREEN_WIDTH // 2 - 400
        card_y = 80
        card_w = 800
        card_h = 220
        
        # Outer glow
        for i in range(10, 0, -1):
            glow_color = (20 + i * 3, 25 + i * 4, 40 + i * 5)
            pygame.draw.rect(surface, glow_color, (card_x - i, card_y - i, card_w + i * 2, card_h + i * 2), 2)
        
        # Card with gradient
        pygame.draw.rect(surface, (30, 35, 50), (card_x, card_y, card_w, card_h))
        pygame.draw.rect(surface, (80, 90, 120), (card_x, card_y, card_w, card_h), 4)
        
        # Inner glow
        pygame.draw.rect(surface, (50, 60, 80), (card_x + 5, card_y + 5, card_w - 10, card_h - 10), 2)
        
        # Title with animated glow
        title = font_title.render("SKY DEFENDER", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, card_y + 80))
        
        # Animated glow effect
        glow_intensity = 100 + int(50 * (0.5 + 0.5 * __import__('math').sin(t / 500)))
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            glow = font_title.render("SKY DEFENDER", True, (0, glow_intensity // 2, glow_intensity))
            surface.blit(glow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        surface.blit(title, title_rect)
        
        # Subtitle with fade effect
        pulse = 0.7 + 0.3 * (0.5 + 0.5 * __import__('math').sin(t / 800))
        subtitle_color = (int(180 * pulse), int(180 * pulse), int(220 * pulse))
        subtitle = font_small.render("Retro Atari-Style Shooter", True, subtitle_color)
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, card_y + 150))
        surface.blit(subtitle, sub_rect)
        
        # Draw decorative balloons in title card (static but animated)
        balloon_colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
        for i in range(5):
            bx = card_x + 80 + i * 140
            by = card_y + 60 + (i % 2) * 30 + int(5 * __import__('math').sin(t / 400 + i))
            self._draw_menu_balloon(surface, bx, by, balloon_colors[i], 25)
        
        # Draw plane in title card (with engine animation)
        self._draw_menu_plane(surface, SCREEN_WIDTH // 2, card_y + 180, t)
        
        # Menu buttons with enhanced visuals
        btn_x = SCREEN_WIDTH // 2 - 150
        btn_y = 380
        btn_width = 300
        btn_height = 65
        
        options = [("PLAY", COLOR_GREEN), ("SHOP", COLOR_YELLOW), ("QUIT", COLOR_RED)]
        
        mx, my = pygame.mouse.get_pos()
        
        for i, (text, color) in enumerate(options):
            is_selected = (i == self.selected_option)
            is_hovered = btn_x <= mx <= btn_x + btn_width and btn_y + i * 80 <= my <= btn_y + i * 80 + btn_height
            
            # Button background with depth
            if is_selected or is_hovered:
                bg_color = (70, 70, 95)
                border_width = 4
                shadow_offset = 3
                # Add glow for selected/hovered
                for g in range(3, 0, -1):
                    pygame.draw.rect(surface, (color[0]//10, color[1]//10, color[2]//10), 
                                   (btn_x - g, btn_y + i * 80 - g, btn_width + g*2, btn_height + g*2), 2)
            else:
                bg_color = (45, 45, 60)
                border_width = 3
                shadow_offset = 2
            
            # Shadow
            pygame.draw.rect(surface, (20, 20, 30), (btn_x + shadow_offset, btn_y + i * 80 + shadow_offset, btn_width, btn_height))
            
            # Button
            pygame.draw.rect(surface, bg_color, (btn_x, btn_y + i * 80, btn_width, btn_height))
            pygame.draw.rect(surface, color if (is_selected or is_hovered) else (80, 80, 100), 
                           (btn_x, btn_y + i * 80, btn_width, btn_height), border_width)
            
            # Button text
            text_surface = font_medium.render(text, True, color if (is_selected or is_hovered) else (170, 170, 180))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, btn_y + i * 80 + btn_height // 2))
            surface.blit(text_surface, text_rect)
        
        # Instructions with pulsing
        instr_alpha = 0.5 + 0.5 * (0.5 + 0.5 * __import__('math').sin(t / 600))
        instr = font_small.render("Arrow Keys + ENTER or Click to select", True, (int(120 * instr_alpha), int(120 * instr_alpha), int(140 * instr_alpha)))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(instr, instr_rect)
    
    def _draw_cloud(self, surface: pygame.Surface, x: int, y: int, size: int) -> None:
        """Draw a fluffy cloud."""
        color = (60, 65, 85)
        # Draw multiple overlapping circles for fluffy effect
        pygame.draw.circle(surface, color, (x, y), size // 2)
        pygame.draw.circle(surface, color, (x + size // 3, y - size // 4), size // 3)
        pygame.draw.circle(surface, color, (x - size // 3, y), size // 3)
        pygame.draw.circle(surface, color, (x + size // 4, y + size // 4), size // 4)
        pygame.draw.circle(surface, color, (x - size // 4, y - size // 5), size // 4)
    
    def _draw_animated_balloon(self, surface: pygame.Surface, x: int, y: int, color: tuple, radius: int) -> None:
        """Draw an animated floating balloon with string and glow."""
        # Outer glow using semi-transparent circles
        for i in range(3, 0, -1):
            glow_radius = radius + i * 4
            # Create a soft glow by drawing multiple circles with decreasing opacity
            glow_surface = pygame.Surface((glow_radius * 2 + 2, glow_radius * 2 + 2), pygame.SRCALPHA)
            # Fade from center
            for r in range(glow_radius, 0, -2):
                alpha = max(0, 40 - (glow_radius - r) * 3)
                pygame.draw.circle(glow_surface, (*color, alpha), (glow_radius + 1, glow_radius + 1), r)
            surface.blit(glow_surface, (x - glow_radius - 1, y - glow_radius - 1))
        
        # Balloon body with gradient effect
        pygame.draw.circle(surface, color, (x, y), radius)
        # Inner highlight
        pygame.draw.circle(surface, (min(color[0] + 60, 255), min(color[1] + 60, 255), min(color[2] + 60, 255)), 
                          (x - radius//3, y - radius//3), radius//4)
        # Shine
        pygame.draw.circle(surface, (255, 255, 255), (x - radius//2, y - radius//2), radius//8)
        # String
        pygame.draw.line(surface, (80, 80, 80), (x, y + radius), (x, y + radius + 25), 1)
        # Knot
        pygame.draw.circle(surface, (60, 60, 60), (x, y + radius + 5), 3)
    
    def _draw_menu_balloon(self, surface: pygame.Surface, x: int, y: int, color: tuple, radius: int) -> None:
        """Draw a balloon for the title card."""
        # Balloon body
        pygame.draw.circle(surface, color, (x, y), radius)
        # Highlight
        pygame.draw.circle(surface, (255, 255, 255), (x - radius//3, y - radius//3), radius//4)
        # String
        pygame.draw.line(surface, (100, 100, 100), (x, y + radius), (x, y + radius + 20), 1)
    
    def _draw_flying_plane(self, surface: pygame.Surface, x: int, y: int, direction: int, scale: float, color: tuple) -> None:
        """Draw a flying plane with propeller animation and exhaust trails."""
        import math
        t = pygame.time.get_ticks()
        
        # Exhaust trail behind the plane
        trail_length = 8
        trail_offset = -direction * 15 * scale
        for i in range(trail_length):
            trail_x = x + trail_offset * (i + 1)
            trail_y = y - 25 * scale + math.sin(t / 100 + i) * 2
            trail_alpha = max(0, 100 - i * 12)
            trail_size = max(1, 6 - i * 0.6) * scale
            trail_surface = pygame.Surface((int(trail_size * 2 + 2), int(trail_size * 2 + 2)), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 150, 50, trail_alpha), 
                              (int(trail_size + 1), int(trail_size + 1)), int(trail_size))
            surface.blit(trail_surface, (trail_x - trail_size - 1, trail_y - trail_size - 1))
        
        # Shadow
        shadow_offset = 5
        pygame.draw.ellipse(surface, (0, 0, 0), (x - 40 * scale + shadow_offset, y + 3 + shadow_offset, 80 * scale, 10 * scale))
        
        # Wings with gradient
        pygame.draw.rect(surface, color, (x - 45 * scale, y - 3 * scale, 90 * scale, 6 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 45 * scale, y - 3 * scale, 90 * scale, 6 * scale), 1)
        # Wing highlight
        pygame.draw.line(surface, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)),
                        (x - 43 * scale, y - 2 * scale), (x + 43 * scale, y - 2 * scale), 2)
        
        # Fuselage
        pygame.draw.rect(surface, color, (x - 6 * scale, y - 20 * scale, 12 * scale, 40 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 6 * scale, y - 20 * scale, 12 * scale, 40 * scale), 1)
        
        # Nose cone
        nose_points = [(x, y - 28 * scale), (x - 6 * scale, y - 20 * scale), (x + 6 * scale, y - 20 * scale)]
        pygame.draw.polygon(surface, COLOR_WHITE, nose_points)
        pygame.draw.polygon(surface, COLOR_BLACK, nose_points, 1)
        
        # Cockpit with shine
        pygame.draw.rect(surface, (100, 200, 255), (x - 4 * scale, y - 15 * scale, 8 * scale, 10 * scale))
        pygame.draw.rect(surface, COLOR_BLACK, (x - 4 * scale, y - 15 * scale, 8 * scale, 10 * scale), 1)
        pygame.draw.circle(surface, (200, 240, 255), (x - 2 * scale, y - 12 * scale), 2 * scale)
        
        # Tail fin
        pygame.draw.polygon(surface, color, [(x - 4 * scale, y + 20 * scale), (x + 4 * scale, y + 20 * scale), (x, y + 35 * scale)])
        pygame.draw.polygon(surface, COLOR_BLACK, [(x - 4 * scale, y + 20 * scale), (x + 4 * scale, y + 20 * scale), (x, y + 35 * scale)], 1)
        
        # Animated propeller (blur effect)
        prop_angle = (t / 20) % 360
        prop_length = 20 * scale
        prop_x = x + 6 * scale * direction
        
        # Propeller blur disc
        prop_surface = pygame.Surface((int(prop_length * 2 + 4), int(prop_length + 4)), pygame.SRCALPHA)
        pygame.draw.ellipse(prop_surface, (200, 200, 200, 150), 
                           (2, 2, int(prop_length * 2), int(prop_length)))
        surface.blit(prop_surface, (prop_x - prop_length - 2, y - 25 * scale - prop_length // 2 - 2))
        
        # Engine glow
        pygame.draw.circle(surface, (255, 150, 50), (prop_x, y - 25 * scale), 4 * scale)
        pygame.draw.circle(surface, (255, 200, 100), (prop_x, y - 25 * scale), 2 * scale)
    
    def _draw_menu_plane(self, surface: pygame.Surface, x: int, y: int, t: int = 0) -> None:
        """Draw a detailed plane for the title card with animated propeller."""
        import math
        
        # Shadow
        pygame.draw.ellipse(surface, (0, 0, 0), (x - 45, y + 5, 90, 20))
        
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
        
        # Animated propeller
        prop_angle = (t / 15) % 360
        for i in range(3):
            angle = math.radians(prop_angle + i * 120)
            end_x = x + math.cos(angle) * 25
            end_y = y - 50 + math.sin(angle) * 8
            pygame.draw.line(surface, (200, 200, 200), (x, y - 50), (end_x, end_y), 2)
        
        # Engine glow
        pygame.draw.circle(surface, (255, 150, 50), (x, y - 50), 6)
        pygame.draw.circle(surface, (255, 200, 100), (x, y - 50), 3)


class LevelSelect:
    """Level select screen with 2x3 grid of level icons and pagination."""
    
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
        self.start_y = 200
        self.current_page = 0
        self.levels_per_page = 6
        self.total_levels = 12  # Updated for 12 levels
    
    def _get_levels_on_page(self) -> tuple:
        """Get the range of levels on current page."""
        start = self.current_page * self.levels_per_page + 1
        end = min(start + self.levels_per_page - 1, self.total_levels)
        return start, end
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'level_X', 'back', 'next_page', 'prev_page', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_level = max(1, self.selected_level - 1)
                # Update page if needed
                page = (self.selected_level - 1) // self.levels_per_page
                self.current_page = page
            elif event.key == pygame.K_RIGHT:
                self.selected_level = min(self.unlocked_levels, self.selected_level + 1)
                # Update page if needed
                page = (self.selected_level - 1) // self.levels_per_page
                self.current_page = page
            elif event.key == pygame.K_UP:
                self.selected_level = max(1, self.selected_level - self.cols)
                page = (self.selected_level - 1) // self.levels_per_page
                self.current_page = page
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(self.unlocked_levels, self.selected_level + self.cols)
                page = (self.selected_level - 1) // self.levels_per_page
                self.current_page = page
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_level <= self.unlocked_levels:
                    return f'level_{self.selected_level}'
            elif event.key == pygame.K_ESCAPE:
                return 'back'
            elif event.key == pygame.K_PAGEUP or event.key == pygame.K_LEFTBRACKET:
                if self.current_page > 0:
                    self.current_page -= 1
                    self.selected_level = self.current_page * self.levels_per_page + 1
            elif event.key == pygame.K_PAGEDOWN or event.key == pygame.K_RIGHTBRACKET:
                max_page = (self.total_levels - 1) // self.levels_per_page
                if self.current_page < max_page:
                    self.current_page += 1
                    self.selected_level = self.current_page * self.levels_per_page + 1
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Check back button
            if 50 <= mx <= 150 and 50 <= my <= 90:
                return 'back'
            
            # Check page navigation buttons
            # Previous page
            if self.current_page > 0:
                prev_x, prev_y = SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60
                if prev_x <= mx <= prev_x + 80 and prev_y <= my <= prev_y + 40:
                    self.current_page -= 1
                    self.selected_level = self.current_page * self.levels_per_page + 1
            
            # Next page
            max_page = (self.total_levels - 1) // self.levels_per_page
            if self.current_page < max_page:
                next_x, next_y = SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 60
                if next_x <= mx <= next_x + 80 and next_y <= my <= next_y + 40:
                    self.current_page += 1
                    self.selected_level = self.current_page * self.levels_per_page + 1
            
            # Check level icons on current page
            start_level, end_level = self._get_levels_on_page()
            for i in range(self.levels_per_page):
                level_num = start_level + i
                if level_num > end_level:
                    break
                col = i % self.cols
                row = i // self.cols
                icon_x = self.start_x + col * self.icon_spacing_x
                icon_y = self.start_y + row * self.icon_spacing_y
                
                if icon_x <= mx <= icon_x + self.icon_size:
                    if icon_y <= my <= icon_y + self.icon_size:
                        if level_num <= self.unlocked_levels:
                            return f'level_{level_num}'
        
        return 'none'
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the level select screen."""
        surface.fill((20, 20, 35))
        
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Title with page indicator
        start_level, end_level = self._get_levels_on_page()
        title_text = f"SELECT LEVEL (Page {self.current_page + 1}/2)"
        title = font_large.render(title_text, True, COLOR_YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title, title_rect)
        
        # Back button
        pygame.draw.rect(surface, (60, 60, 80), (50, 50, 100, 40))
        pygame.draw.rect(surface, COLOR_BLACK, (50, 50, 100, 40), 2)
        back_text = font_small.render("BACK", True, COLOR_WHITE)
        surface.blit(back_text, (60, 60))
        
        # Level icons in 2x3 grid for current page
        for i in range(self.levels_per_page):
            level_num = start_level + i
            if level_num > self.total_levels:
                break
                
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
            
            # Level preview - show actual level balloons
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
        
        # Page navigation buttons
        max_page = (self.total_levels - 1) // self.levels_per_page
        nav_y = SCREEN_HEIGHT - 60
        
        if self.current_page > 0:
            prev_x, prev_y = SCREEN_WIDTH // 2 - 100, nav_y
            pygame.draw.rect(surface, (80, 80, 120), (prev_x, prev_y, 80, 40))
            pygame.draw.rect(surface, COLOR_BLACK, (prev_x, prev_y, 80, 40), 2)
            prev_text = font_small.render("<< PREV", True, COLOR_WHITE)
            surface.blit(prev_text, (prev_x + 5, prev_y + 10))
        
        if self.current_page < max_page:
            next_x, next_y = SCREEN_WIDTH // 2 + 20, nav_y
            pygame.draw.rect(surface, (80, 80, 120), (next_x, next_y, 80, 40))
            pygame.draw.rect(surface, COLOR_BLACK, (next_x, next_y, 80, 40), 2)
            next_text = font_small.render("NEXT >>", True, COLOR_WHITE)
            surface.blit(next_text, (next_x + 5, next_y + 10))
        
        # Page indicator dots
        dot_y = nav_y - 20
        for p in range(2):
            dot_x = SCREEN_WIDTH // 2 - 20 + p * 40
            color = COLOR_YELLOW if p == self.current_page else (80, 80, 100)
            pygame.draw.circle(surface, color, (dot_x, dot_y), 8)
            pygame.draw.circle(surface, COLOR_BLACK, (dot_x, dot_y), 8, 1)
        
        # Instructions
        instr = font_tiny.render("Arrow Keys + ENTER or Click | Page Up/Down or [ ] to change page", True, (120, 120, 140))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        surface.blit(instr, instr_rect)
    
    def _draw_level_preview(self, surface: pygame.Surface, x: int, y: int, level_num: int) -> None:
        """Draw a mini preview of the level showing actual balloon pattern."""
        preview_x = x + 10
        preview_y = y + 10
        preview_w = self.icon_size - 20
        preview_h = self.icon_size - 40
        
        # Mini sky background
        pygame.draw.rect(surface, (100, 180, 255), (preview_x, preview_y, preview_w, preview_h))
        
        # Try to load actual level balloons and draw them
        try:
            from game.levels import get_level
            level_module = get_level(level_num)
            balloons = level_module.create_balloons()
            
            # Find bounds of balloons
            if balloons:
                min_x = min(b.x for b in balloons)
                max_x = max(b.x for b in balloons)
                min_y = min(b.y for b in balloons)
                max_y = max(b.y for b in balloons)
                
                # Calculate scale to fit in preview
                balloon_range_x = max_x - min_x if max_x > min_x else 1
                balloon_range_y = max_y - min_y if max_y > min_y else 1
                
                scale_x = (preview_w - 20) / balloon_range_x
                scale_y = (preview_h - 20) / balloon_range_y
                scale = min(scale_x, scale_y, 1.5)  # Cap scale
                
                # Center offset
                offset_x = preview_x + 10 + (preview_w - 20 - balloon_range_x * scale) / 2 - min_x * scale
                offset_y = preview_y + 10 + (preview_h - 20 - balloon_range_y * scale) / 2 - min_y * scale
                
                # Colors for each tier
                colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
                
                # Draw balloons (limit to prevent slowdown)
                for balloon in balloons[:150]:  # Limit preview balloons
                    bx = offset_x + balloon.x * scale
                    by = offset_y + balloon.y * scale
                    
                    # Skip if off preview area
                    if bx < preview_x or bx > preview_x + preview_w:
                        continue
                    if by < preview_y or by > preview_y + preview_h:
                        continue
                    
                    radius = max(3, int(balloon.radius * scale * 0.8))
                    color = colors[min(balloon.tier, 4)]
                    pygame.draw.circle(surface, color, (int(bx), int(by)), radius)
                    if radius > 4:
                        pygame.draw.circle(surface, COLOR_BLACK, (int(bx), int(by)), radius, 1)
        except Exception:
            # Fallback to simple preview
            colors = [COLOR_PINK, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_RED]
            balloon_count = min(level_num * 2 + 2, 10)
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
    """Shop screen accessible from main menu or level complete."""
    
    def __init__(self, total_orbs: int = 0, dart_speed_level: int = 0,
                 laser_level: int = 0, missile_level: int = 0, boomerang_level: int = 0,
                 lightning_level: int = 0, wingman_level: int = 0,
                 orb_magnet_level: int = 0, orb_luck_level: int = 0,
                 show_next_level: bool = False, level_num: int = 1, has_next: bool = True):
        self.total_orbs = total_orbs
        self.dart_speed_level = dart_speed_level
        self.laser_level = laser_level
        self.missile_level = missile_level
        self.boomerang_level = boomerang_level
        self.lightning_level = lightning_level
        self.wingman_level = wingman_level
        self.orb_magnet_level = orb_magnet_level
        self.orb_luck_level = orb_luck_level
        self.selected_option = 0  # 0 = back
        self.show_next_level = show_next_level
        self.level_num = level_num
        self.has_next = has_next
        
        # Recalculate costs
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER,
            LIGHTNING_UNLOCK_COST, LIGHTNING_BASE_COST, LIGHTNING_COST_MULTIPLIER,
            WINGMAN_UNLOCK_COST, WINGMAN_BASE_COST, WINGMAN_COST_MULTIPLIER,
            ORB_MAGNET_UNLOCK_COST, ORB_MAGNET_BASE_COST, ORB_MAGNET_COST_MULTIPLIER,
            ORB_LUCK_UNLOCK_COST, ORB_LUCK_BASE_COST, ORB_LUCK_COST_MULTIPLIER
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

        # Orb Magnet: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if orb_magnet_level == 0:
            self.orb_magnet_cost = ORB_MAGNET_UNLOCK_COST
        else:
            self.orb_magnet_cost = int(ORB_MAGNET_BASE_COST * (ORB_MAGNET_COST_MULTIPLIER ** (orb_magnet_level - 1)))
        self.can_buy_orb_magnet = self.total_orbs >= self.orb_magnet_cost

        # Orb Luck: 200 to unlock, then 100 * 1.5^(level-1) for upgrades
        if orb_luck_level == 0:
            self.orb_luck_cost = ORB_LUCK_UNLOCK_COST
        else:
            self.orb_luck_cost = int(ORB_LUCK_BASE_COST * (ORB_LUCK_COST_MULTIPLIER ** (orb_luck_level - 1)))
        self.can_buy_orb_luck = self.total_orbs >= self.orb_luck_cost
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'buy_X', 'back', 'next_level', or 'none'."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'back'
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Check back button (matches visual position in draw())
            if 60 <= mx <= 140 and 110 <= my <= 145:
                return 'back'
            
            # Check next level button if showing
            if self.show_next_level and self.has_next:
                btn_x = SCREEN_WIDTH // 2 - 120
                btn_y = SCREEN_HEIGHT - 80
                if btn_x <= mx <= btn_x + 240 and btn_y <= my <= btn_y + 50:
                    return 'next_level'
            
            # Check upgrade buttons
            # 2x4 grid click detection (8 total)
            grid_start_x = 80
            grid_start_y = 170
            btn_width = 420
            btn_height = 150
            col_gap = 80
            row_gap = 24
            
            for i in range(8):
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
                    elif i == 6 and self.can_buy_orb_magnet:
                        return 'buy_orb_magnet'
                    elif i == 7 and self.can_buy_orb_luck:
                        return 'buy_orb_luck'
        
        return 'none'
    
    def buy_upgrade(self, upgrade_type: str) -> bool:
        """Attempt to buy an upgrade. Returns True if successful."""
        from game.constants import (
            UPGRADE_DART_SPEED_BASE_COST, UPGRADE_DART_SPEED_COST_MULTIPLIER,
            LASER_UNLOCK_COST, LASER_BASE_COST, LASER_COST_MULTIPLIER,
            MISSILE_UNLOCK_COST, MISSILE_BASE_COST, MISSILE_COST_MULTIPLIER,
            BOOMERANG_UNLOCK_COST, BOOMERANG_BASE_COST, BOOMERANG_COST_MULTIPLIER,
            LIGHTNING_UNLOCK_COST, LIGHTNING_BASE_COST, LIGHTNING_COST_MULTIPLIER,
            WINGMAN_UNLOCK_COST, WINGMAN_BASE_COST, WINGMAN_COST_MULTIPLIER,
            ORB_MAGNET_UNLOCK_COST, ORB_MAGNET_BASE_COST, ORB_MAGNET_COST_MULTIPLIER,
            ORB_LUCK_UNLOCK_COST, ORB_LUCK_BASE_COST, ORB_LUCK_COST_MULTIPLIER
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
        elif upgrade_type == 'orb_magnet' and self.can_buy_orb_magnet:
            self.total_orbs -= self.orb_magnet_cost
            self.orb_magnet_level += 1
            if self.orb_magnet_level == 1:
                self.orb_magnet_cost = ORB_MAGNET_BASE_COST
            else:
                self.orb_magnet_cost = int(ORB_MAGNET_BASE_COST * (ORB_MAGNET_COST_MULTIPLIER ** (self.orb_magnet_level - 1)))
            self.can_buy_orb_magnet = self.total_orbs >= self.orb_magnet_cost
            return True
        elif upgrade_type == 'orb_luck' and self.can_buy_orb_luck:
            self.total_orbs -= self.orb_luck_cost
            self.orb_luck_level += 1
            if self.orb_luck_level == 1:
                self.orb_luck_cost = ORB_LUCK_BASE_COST
            else:
                self.orb_luck_cost = int(ORB_LUCK_BASE_COST * (ORB_LUCK_COST_MULTIPLIER ** (self.orb_luck_level - 1)))
            self.can_buy_orb_luck = self.total_orbs >= self.orb_luck_cost
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
        
        # Title - changes based on context
        if self.show_next_level:
            title = font_large.render(f"LEVEL {self.level_num} COMPLETE!", True, COLOR_GREEN)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, banner_y + 35))
            surface.blit(title, title_rect)
        else:
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
        
        # Upgrade items in 2x4 grid
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
             "Deploys ally planes that shoot at closest balloons"),
            ("Orb Magnet", self.orb_magnet_level, self.orb_magnet_cost,
             self.can_buy_orb_magnet, (120, 200, 255),
             "Boosts orb magnet radius and pull strength by 25% per level"),
            ("Orb Luck", self.orb_luck_level, self.orb_luck_cost,
             self.can_buy_orb_luck, (255, 210, 120),
             "Chance to spawn extra orbs when popping balloons")
        ]
        
        # 2x4 grid layout
        grid_start_x = 80
        grid_start_y = 170
        btn_width = 420
        btn_height = 150
        col_gap = 80
        row_gap = 24
        
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
        
        # Tooltip panel below the 8 options grid
        grid_end_y = grid_start_y + 4 * (btn_height + row_gap) - row_gap
        tooltip_x = 100
        tooltip_y = grid_end_y + 16
        tooltip_w = SCREEN_WIDTH - 200
        tooltip_h = 140
        
        if hovered_item:
            _, name, level, cost, color, description, can_buy = hovered_item
            
            # Tooltip background - parchment/lab note style
            pygame.draw.rect(surface, (45, 42, 38), (tooltip_x, tooltip_y, tooltip_w, tooltip_h))
            pygame.draw.rect(surface, (100, 90, 80), (tooltip_x, tooltip_y, tooltip_w, tooltip_h), 3)
            
            # Header on left
            header_text = font_small.render("WEAPON INFO", True, (180, 170, 160))
            surface.blit(header_text, (tooltip_x + 20, tooltip_y + 10))
            
            # Divider vertical
            pygame.draw.line(surface, (80, 70, 60), (tooltip_x + 180, tooltip_y + 5),
                           (tooltip_x + 180, tooltip_y + tooltip_h - 5), 1)
            
            # Left section: Weapon name and level
            weapon_name = font_medium.render(name, True, color)
            surface.blit(weapon_name, (tooltip_x + 20, tooltip_y + 40))
            
            # Current level
            if level == 0:
                level_info = "Not Acquired"
            else:
                level_info = f"Current: Level {level}"
            level_info_text = font_tiny.render(level_info, True, (150, 150, 160))
            surface.blit(level_info_text, (tooltip_x + 20, tooltip_y + 75))
            
            # Description in center
            desc_x = tooltip_x + 200
            desc_w = 400
            words = description.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if font_tiny.size(test_line)[0] < desc_w:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            desc_y = tooltip_y + 40
            for line in lines:
                desc_text = font_tiny.render(line, True, (170, 170, 180))
                surface.blit(desc_text, (desc_x, desc_y))
                desc_y += 25
            
            # Stats on right
            stats_x = tooltip_x + tooltip_w - 250
            stats_title = font_tiny.render("STATS:", True, (180, 170, 160))
            surface.blit(stats_title, (stats_x, tooltip_y + 10))
            
            # Show specific stats based on weapon
            stats_y = tooltip_y + 35
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
            elif "Orb Magnet" in name:
                stats = ["+25% radius per level", "+25% pull strength", "Boosts orb pickup"]
            elif "Orb Luck" in name:
                stats = ["+20% base extra orb", "+5% chance per level", "+1 max extra per level"]
            else:
                stats = []
            
            for stat in stats:
                stat_text = font_tiny.render("• " + stat, True, (160, 160, 170))
                surface.blit(stat_text, (stats_x, stats_y))
                stats_y += 22
        
        # Next level button at bottom if showing level complete
        if self.show_next_level and self.has_next:
            btn_x = SCREEN_WIDTH // 2 - 120
            btn_y = SCREEN_HEIGHT - 80
            # Check if hovered
            mx, my = pygame.mouse.get_pos()
            is_hovered = btn_x <= mx <= btn_x + 240 and btn_y <= my <= btn_y + 50
            
            if is_hovered:
                btn_color = (100, 200, 100)
            else:
                btn_color = COLOR_GREEN
            
            pygame.draw.rect(surface, btn_color, (btn_x, btn_y, 240, 50), border_radius=8)
            pygame.draw.rect(surface, COLOR_BLACK, (btn_x, btn_y, 240, 50), 3, border_radius=8)
            next_text = font_medium.render("NEXT LEVEL", True, COLOR_BLACK)
            text_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, btn_y + 25))
            surface.blit(next_text, text_rect)
            
            # Instructions with next level info
            instr = font_small.render("Buy upgrades | Click NEXT LEVEL to continue | ESC to go back", True, (130, 130, 140))
        else:
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
        
        elif index == 6:  # Orb Magnet
            # Horseshoe magnet icon
            pygame.draw.arc(surface, color, (cx - 25, cy - 25, 50, 50), 3.5, 5.9, 10)
            pygame.draw.arc(surface, COLOR_BLACK, (cx - 25, cy - 25, 50, 50), 3.5, 5.9, 3)
            pygame.draw.rect(surface, COLOR_WHITE, (cx - 26, cy + 5, 10, 18))
            pygame.draw.rect(surface, COLOR_WHITE, (cx + 16, cy + 5, 10, 18))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 26, cy + 5, 10, 18), 1)
            pygame.draw.rect(surface, COLOR_BLACK, (cx + 16, cy + 5, 10, 18), 1)
            pygame.draw.circle(surface, (200, 230, 255), (cx, cy - 10), 6)
        
        elif index == 7:  # Orb Luck
            # Clover-like luck icon
            pygame.draw.circle(surface, color, (cx - 8, cy - 6), 10)
            pygame.draw.circle(surface, color, (cx + 8, cy - 6), 10)
            pygame.draw.circle(surface, color, (cx - 8, cy + 8), 10)
            pygame.draw.circle(surface, color, (cx + 8, cy + 8), 10)
            pygame.draw.circle(surface, COLOR_BLACK, (cx - 8, cy - 6), 10, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx + 8, cy - 6), 10, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx - 8, cy + 8), 10, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx + 8, cy + 8), 10, 1)
            pygame.draw.rect(surface, (80, 160, 80), (cx - 2, cy + 14, 4, 12))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 2, cy + 14, 4, 12), 1)
    
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
        
        elif index == 6:  # Orb Magnet icon
            # Magnet shape
            pygame.draw.arc(surface, COLOR_CYAN, (cx - 10, cy - 10, 20, 20), 3.4, 5.9, 4)
            pygame.draw.arc(surface, COLOR_BLACK, (cx - 10, cy - 10, 20, 20), 3.4, 5.9, 2)
            pygame.draw.rect(surface, COLOR_WHITE, (cx - 11, cy + 2, 4, 8))
            pygame.draw.rect(surface, COLOR_WHITE, (cx + 7, cy + 2, 4, 8))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 11, cy + 2, 4, 8), 1)
            pygame.draw.rect(surface, COLOR_BLACK, (cx + 7, cy + 2, 4, 8), 1)
            pygame.draw.circle(surface, (180, 220, 255), (cx, cy - 2), 3)
        
        elif index == 7:  # Orb Luck icon
            # Clover
            pygame.draw.circle(surface, (120, 220, 120), (cx - 4, cy - 3), 5)
            pygame.draw.circle(surface, (120, 220, 120), (cx + 4, cy - 3), 5)
            pygame.draw.circle(surface, (120, 220, 120), (cx - 4, cy + 4), 5)
            pygame.draw.circle(surface, (120, 220, 120), (cx + 4, cy + 4), 5)
            pygame.draw.circle(surface, COLOR_BLACK, (cx - 4, cy - 3), 5, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx + 4, cy - 3), 5, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx - 4, cy + 4), 5, 1)
            pygame.draw.circle(surface, COLOR_BLACK, (cx + 4, cy + 4), 5, 1)
            pygame.draw.rect(surface, (80, 160, 80), (cx - 1, cy + 7, 2, 6))
            pygame.draw.rect(surface, COLOR_BLACK, (cx - 1, cy + 7, 2, 6), 1)
