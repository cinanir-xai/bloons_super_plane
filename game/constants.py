"""Game constants and configuration values - Retro Atari Inspired."""

# Screen dimensions (50% larger)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 1200
FPS = 60

# Retro Color Palette (Atari-style)
COLOR_BG_GRASS = (34, 139, 34)
COLOR_BG_RIVER = (0, 191, 255)
COLOR_BG_SAND = (238, 232, 170)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_RED_DARK = (180, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_PINK = (255, 105, 180)
COLOR_CYAN = (0, 255, 255)
COLOR_ORANGE = (255, 165, 0)
COLOR_CLOUD = (255, 255, 255, 200)

# Player settings
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
PLAYER_SPEED = 0.12  # Lerp factor
DART_COOLDOWN = 80  # milliseconds
DART_OFFSET_X = 20

# Dart settings
DART_SPEED = 15
DART_WIDTH = 6
DART_HEIGHT = 20
DART_LIFETIME = 2000

# Balloon settings
BALLOON_SPEED = 1.5
BALLOON_SPAWN_DELAY = 500  # ms between rows
BALLOON_WAVE_DELAY = 3000  # ms between color waves

# Background settings
CLOUD_COUNT = 10
TREE_COUNT = 15
RIVER_WIDTH = 150
SCENERY_SPEED = 2

# Visual effects
PARTICLE_SIZE = 4
