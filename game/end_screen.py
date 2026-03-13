"""End-of-Level Screen - Separate page shown after completing a level."""

import pygame
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE,
    COLOR_YELLOW, COLOR_RED, COLOR_GREEN
)

class EndScreen:
    """End-of-level screen showing orbs collected and next level option."""
    
    def __init__(self, orbs_collected: int, level_num: int, has_next: bool):
        self.orbs_collected = orbs_collected
        self.level_num = level_num
        self.has_next = has_next
        self.selected_option = 0  # 0 = next level, 1 = quit
        
        # Button rects
        self.button_y = SCREEN_HEIGHT - 150
        self.button_height = 50
        self.button_width = 200
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """Handle input. Returns 'next', 'quit', or 'none'."""
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
            # Check button clicks
            btn_x = SCREEN_WIDTH // 2 - self.button_width // 2
            if btn_x <= mx <= btn_x + self.button_width:
                if self.button_y <= my <= self.button_y + self.button_height:
                    return 'next' if self.has_next else 'quit'
                elif self.button_y + 60 <= my <= self.button_y + 60 + self.button_height:
                    return 'quit'
        
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            btn_x = SCREEN_WIDTH // 2 - self.button_width // 2
            if btn_x <= mx <= btn_x + self.button_width:
                if self.button_y <= my <= self.button_y + self.button_height:
                    self.selected_option = 0
                elif self.button_y + 60 <= my <= self.button_y + 60 + self.button_height:
                    self.selected_option = 1
        
        return 'none'
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the end screen."""
        # Clear with dark background
        surface.fill((20, 20, 30))
        
        # Title
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # "Level Complete" text
        title = font_large.render(f"LEVEL {self.level_num} COMPLETE!", True, COLOR_GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(title, title_rect)
        
        # Orb count display
        orb_y = 350
        
        # Draw large yellow orb icon
        pygame.draw.circle(surface, COLOR_YELLOW, (SCREEN_WIDTH // 2 - 80, orb_y), 30)
        pygame.draw.circle(surface, COLOR_BLACK, (SCREEN_WIDTH // 2 - 80, orb_y), 30, 3)
        pygame.draw.circle(surface, (255, 255, 200), (SCREEN_WIDTH // 2 - 85, orb_y - 5), 12)
        
        # Orb count text
        orb_text = font_large.render(f"x {self.orbs_collected}", True, COLOR_YELLOW)
        surface.blit(orb_text, (SCREEN_WIDTH // 2 - 30, orb_y - 25))
        
        # "Orbs Collected" label
        label = font_small.render("ORBS COLLECTED", True, COLOR_WHITE)
        label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, orb_y + 60))
        surface.blit(label, label_rect)
        
        # Buttons
        btn_x = SCREEN_WIDTH // 2 - self.button_width // 2
        
        # Next Level button
        if self.has_next:
            next_color = COLOR_YELLOW if self.selected_option == 0 else (100, 100, 100)
            pygame.draw.rect(surface, next_color, (btn_x, self.button_y, self.button_width, self.button_height))
            pygame.draw.rect(surface, COLOR_BLACK, (btn_x, self.button_y, self.button_width, self.button_height), 3)
            next_text = font_medium.render("NEXT LEVEL", True, COLOR_BLACK)
            text_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, self.button_y + 25))
            surface.blit(next_text, text_rect)
        
        # Quit button
        quit_color = COLOR_RED if self.selected_option == 1 else (100, 100, 100)
        quit_y = self.button_y + 60 if self.has_next else self.button_y
        pygame.draw.rect(surface, quit_color, (btn_x, quit_y, self.button_width, self.button_height))
        pygame.draw.rect(surface, COLOR_BLACK, (btn_x, quit_y, self.button_width, self.button_height), 3)
        quit_text = font_medium.render("QUIT", True, COLOR_WHITE)
        text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, quit_y + 25))
        surface.blit(quit_text, text_rect)
        
        # Instructions
        instr = font_small.render("Use arrow keys and ENTER, or click", True, (150, 150, 150))
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(instr, instr_rect)
