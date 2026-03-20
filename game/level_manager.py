"""Level Manager - Handles level progression and transitions."""

import time
from typing import Optional, List, Tuple
from game.levels import get_level, get_total_levels
from game.enemies import Balloon

class LevelManager:
    """Manages level loading and state."""
    
    def __init__(self):
        self.current_level_num = 1
        self.total_levels = get_total_levels()
        self.balloons_remaining = 0
        self.level_complete = False
        # Delayed balloon spawning system
        self.delayed_spawns: List[Tuple[float, List[Balloon]]] = []  # [(spawn_time, balloons), ...]
        self.level_start_time: float = 0
        
    def load_level(self, level_num: int) -> List[Balloon]:
        """Load a specific level and return its balloons."""
        if 1 <= level_num <= self.total_levels:
            self.current_level_num = level_num
            level_module = get_level(level_num)
            
            # Clear any pending delayed spawns
            self.delayed_spawns = []
            self.level_start_time = time.time()
            
            # Get initial balloons and any delayed spawns
            balloons = level_module.create_balloons()
            
            # Check if level has delayed spawns
            if hasattr(level_module, 'get_delayed_spawns'):
                delayed = level_module.get_delayed_spawns()
                for delay_seconds, delayed_balloons in delayed:
                    spawn_time = self.level_start_time + delay_seconds
                    self.delayed_spawns.append((spawn_time, delayed_balloons))
            
            self.balloons_remaining = len(balloons)
            # Add delayed balloons to remaining count
            for _, delayed_balloons in self.delayed_spawns:
                self.balloons_remaining += len(delayed_balloons)
            
            self.level_complete = False
            return balloons
        return []
    
    def get_pending_spawns(self) -> List[Balloon]:
        """Get any balloons that should spawn now based on delays."""
        current_time = time.time()
        ready_balloons = []
        remaining_delays = []
        
        for spawn_time, balloons in self.delayed_spawns:
            if current_time >= spawn_time:
                ready_balloons.extend(balloons)
            else:
                remaining_delays.append((spawn_time, balloons))
        
        self.delayed_spawns = remaining_delays
        return ready_balloons
    
    def get_delay_remaining(self) -> float:
        """Get the remaining time until the next delayed spawn (0 if none)."""
        if not self.delayed_spawns:
            return 0.0
        next_spawn_time = min(spawn_time for spawn_time, _ in self.delayed_spawns)
        remaining = next_spawn_time - time.time()
        return max(0.0, remaining)
    
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
