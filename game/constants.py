"""Game constants and configuration values - Retro Atari Inspired."""

# Screen dimensions
SCREEN_WIDTH = 600  # Narrower for retro feel
SCREEN_HEIGHT = 800
FPS = 60

# Retro Color Palette (Atari-style)
COLOR_BG_GRASS = (34, 139, 34)
COLOR_BG_RIVER = (0, 191, 255)
COLOR_BG_ROAD = (105, 105, 105)
COLOR_BG_SAND = (238, 232, 170)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_RED_DARK = (180, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_PURPLE = (255, 0, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_ORANGE = (255, 165, 0)
COLOR_CLOUD = (255, 255, 255, 200)

# Player settings
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 48
PLAYER_SPEED = 0.15  # Lerp factor
DART_COOLDOWN = 100  # milliseconds
DART_OFFSET_X = 16

# Dart settings
DART_SPEED = 12
DART_WIDTH = 4
DART_HEIGHT = 16
DART_LIFETIME = 1500

# Background settings
CLOUD_COUNT = 8
TREE_COUNT = 12
RIVER_WIDTH = 100
SCENERY_SPEED = 3

# Visual effects
PARTICLE_SIZE = 4
TRAIL_ALPHA = 150
