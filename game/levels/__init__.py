"""Levels package - Each level defines its own balloon spawning pattern."""

def get_level(num: int):
    """Get level module by number (1-6)."""
    if num == 1:
        from . import level_1
        return level_1
    elif num == 2:
        from . import level_2
        return level_2
    elif num == 3:
        from . import level_3
        return level_3
    elif num == 4:
        from . import level_4
        return level_4
    elif num == 5:
        from . import level_5
        return level_5
    elif num == 6:
        from . import level_6
        return level_6
    from . import level_1
    return level_1

def get_total_levels() -> int:
    return 6
