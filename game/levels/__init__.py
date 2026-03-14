"""Levels package - Each level defines its own balloon spawning pattern."""

def get_level(num: int):
    """Get level module by number (1-12)."""
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
    elif num == 7:
        from . import level_7
        return level_7
    elif num == 8:
        from . import level_8
        return level_8
    elif num == 9:
        from . import level_9
        return level_9
    elif num == 10:
        from . import level_10
        return level_10
    elif num == 11:
        from . import level_11
        return level_11
    elif num == 12:
        from . import level_12
        return level_12
    from . import level_1
    return level_1

def get_total_levels() -> int:
    return 12
