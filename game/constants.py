"""Game constants and configuration values - Retro Atari Inspired."""

# Screen dimensions (Now 1125x1500 - 25% larger than previous 900x1200)
SCREEN_WIDTH = 1125
SCREEN_HEIGHT = 1500
FPS = 0  # Uncapped frame rate

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
DART_COOLDOWN = 96  # milliseconds (20% slower than original 80)
DART_OFFSET_X = 24

# Dart settings
DART_SPEED = 18
DART_WIDTH = 6
DART_HEIGHT = 20
DART_LIFETIME = 2000

# Balloon settings
BALLOON_SPEED = 1.8
BALLOON_BASE_RADIUS = 21  # 16 * 1.3 ≈ 21

# Orb settings
ORB_SIZE = 8  # Larger for visibility
ORB_SPEED = 1.2
ORB_MAGNET_RADIUS = 300  # Larger magnet radius
ORB_MAGNET_STRENGTH = 15.0  # Stronger magnet
ORB_COLLECTION_RADIUS = 50  # Large collection hitbox

# Orb upgrade settings
ORB_MAGNET_UNLOCK_COST = 200
ORB_MAGNET_BASE_COST = 100
ORB_MAGNET_COST_MULTIPLIER = 1.5
ORB_LUCK_UNLOCK_COST = 200
ORB_LUCK_BASE_COST = 100
ORB_LUCK_COST_MULTIPLIER = 1.5
ORB_LUCK_BASE_CHANCE = 0.20
ORB_LUCK_CHANCE_PER_LEVEL = 0.05

# Upgrade settings
UPGRADE_DART_SPEED_BASE_COST = 100
UPGRADE_DART_SPEED_COST_MULTIPLIER = 1.5

# Dart Pierce settings
UPGRADE_DART_PIERCE_BASE_COST = 100
UPGRADE_DART_PIERCE_COST_MULTIPLIER = 1.5
DART_BASE_PIERCE = 1  # Base number of balloons a dart can hit

# Chilling Wind (Ice) settings
ICE_UNLOCK_COST = 200  # Cost to unlock the weapon
ICE_BASE_COST = 100  # First upgrade cost after unlock
ICE_COST_MULTIPLIER = 1.5
ICE_BASE_RADIUS = 120  # Same as boomerang orbit radius
ICE_RADIUS_GROWTH = 0.05  # 5% per level
ICE_BASE_SLOW = 0.10  # 10% slow
ICE_SLOW_GROWTH = 0.05  # 5% more slow per level
ICE_BASE_DAMAGE_INTERVAL = 1.0  # 1 second between damage
ICE_DAMAGE_INTERVAL_GROWTH = 0.05  # 5% faster per level

# Laser settings
LASER_BASE_COOLDOWN = 5000  # ms
LASER_BASE_DURATION = 3000  # ms
LASER_POP_DELAY = 100  # ms
LASER_UNLOCK_COST = 200  # Cost to unlock the weapon
LASER_BASE_COST = 100  # First upgrade cost after unlock
LASER_COST_MULTIPLIER = 1.5
LASER_UPGRADE_COOLDOWN_REDUCTION = 0.15
LASER_UPGRADE_DURATION_REDUCTION = 0.15
LASER_WIDTH = 4

# Missile settings
MISSILE_SPEED = 6  # 1/3 of DART_SPEED (18)
MISSILE_UNLOCK_COST = 200  # Cost to unlock the weapon
MISSILE_BASE_COST = 100  # First upgrade cost after unlock
MISSILE_UPGRADE_COST = 100
MISSILE_COST_MULTIPLIER = 1.5
MISSILE_BASE_AOE_RADIUS = 160  # Twice the size of plane (80x80)
MISSILE_UPGRADE_AOE_GROWTH = 0.15
MISSILE_COOLDOWN = 3000  # ms
MISSILE_WIDTH = 12
MISSILE_HEIGHT = 30

# Boomerang settings
BOOMERANG_UNLOCK_COST = 200  # Cost to unlock the weapon
BOOMERANG_BASE_COST = 100  # First upgrade cost after unlock
BOOMERANG_COST = 200
BOOMERANG_UPGRADE_COST = 100
BOOMERANG_COST_MULTIPLIER = 1.5
BOOMERANG_ORBIT_RADIUS = 120
BOOMERANG_SPEED = 360  # Degrees per second (1 full cycle per second)
BOOMERANG_WIDTH = 40
BOOMERANG_HEIGHT = 40
COLOR_BROWN = (139, 69, 19)

# Lightning settings
LIGHTNING_UNLOCK_COST = 200  # Cost to unlock the weapon
LIGHTNING_BASE_COST = 100  # First upgrade cost after unlock
LIGHTNING_COST_MULTIPLIER = 1.5
LIGHTNING_BASE_COOLDOWN = 3000  # ms
LIGHTNING_COOLDOWN_REDUCTION = 0.10  # 10% per level
LIGHTNING_BASE_ARCS = 4  # base extra targets
LIGHTNING_ARC_GROWTH = 2  # extra arcs per level
LIGHTNING_STRIKE_COLOR = (160, 90, 255)
LIGHTNING_GLOW_COLOR = (210, 160, 255)

# Wingman Ace settings
WINGMAN_UNLOCK_COST = 200  # Cost to unlock the weapon
WINGMAN_BASE_COST = 100  # First upgrade cost after unlock
WINGMAN_COST_MULTIPLIER = 1.5
WINGMAN_MAX_SPEED = 3.4
WINGMAN_MIN_SPEED = 2.4
WINGMAN_TURN_RATE = 1.4  # radians per second
WINGMAN_ORBIT_RADIUS = 220
WINGMAN_DART_COOLDOWN_MULTIPLIER = 2.0  # shoots half as fast as player

# Background settings
CLOUD_COUNT = 12
TREE_COUNT = 20
RIVER_WIDTH = 200
SCENERY_SPEED = 2

# Visual effects
PARTICLE_SIZE = 4
