"""Level Manager - Handles level progression and transitions."""

from typing import Optional, List
from game.levels import get_level, get_total_levels
from game.enemies import Balloon

class LevelManager:
    """Manages level loading and state."""
    
    def __init__(self):
        self.current_level_num = 1
        self.total_levels = get_total_levels()
        self.balloons_remaining = 0
        self.level_complete = False
        
    def load_level(self, level_num: int) -> List[Balloon]:
        """Load a specific level and return its balloons."""
        if 1 <= level_num <= self.total_levels:
            self.current_level_num = level_num
            level_module = get_level(level_num)
            balloons = level_module.create_balloons()
            self.balloons_remaining = len(balloons)
            self.level_complete = False
            return balloons
        return []
    
    def get_current_level_info(self) -> dict:
        """Get info about current level."""
        level_module = get_level(self.current_level_num)
        return {
            'number': level_module.LEVEL_NUMBER,
            'name': level_module.LEVEL_NAME,
            'tier': level_module.BALLOON_TIER,
            'total': level_module.get_total_balloons()
        }
    
    def balloon_popped(self) -> None:
        """Called when a balloon is fully popped."""
        self.balloons_remaining = max(0, self.balloons_remaining - 1)
        if self.balloons_remaining <= 0:
            self.level_complete = True
    
    def has_next_level(self) -> bool:
        """Check if there's a next level."""
        return self.current_level_num < self.total_levels
    
    def get_next_level_num(self) -> int:
        """Get next level number."""
        return self.current_level_num + 1
