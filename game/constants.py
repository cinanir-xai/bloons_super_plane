"""Game constants and configuration values - Retro Atari Inspired."""

# Screen dimensions (Now 1125x1500 - 25% larger than previous 900x1200)
SCREEN_WIDTH = 1125
SCREEN_HEIGHT = 1500
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
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_SPEED = 0.12  # Lerp factor
DART_COOLDOWN = 80  # milliseconds
DART_OFFSET_X = 24

# Dart settings
DART_SPEED = 18
DART_WIDTH = 6
DART_HEIGHT = 20
DART_LIFETIME = 2000

# Balloon settings
BALLOON_SPEED = 1.8
BALLOON_SPAWN_DELAY = 500  # ms between rows
BALLOON_WAVE_DELAY = 3000  # ms between color waves
# Sizes: Red is base (16), each tier up +5%
# Red (4): 16, Blue (3): 16.8, Green (2): 17.6, Yellow (1): 18.5, Pink (0): 19.4
BALLOON_BASE_RADIUS = 16

# Orb settings
ORB_SIZE = 4
ORB_SPEED = 1.2
ORB_MAGNET_RADIUS = 200
ORB_MAGNET_STRENGTH = 8.0

# Background settings
CLOUD_COUNT = 12
TREE_COUNT = 20
RIVER_WIDTH = 200
SCENERY_SPEED = 2

# Visual effects
PARTICLE_SIZE = 4
