"""Step 11: GOAP Enemy AI - Configuration"""

# Map size
MAP_WIDTH = 20
MAP_HEIGHT = 10

# Player start
PLAYER_START_X = 5
PLAYER_START_Y = 5
PLAYER_START_HP = 100

# Character mapping
CHAR_MAPPING = {
    "player": "@",
    "enemy": "E",
    "goal": "G",
    "item": "!",
    "wall": "#",
    "obstacle": "#",
}

# Auto-save
AUTO_SAVE = True

# Debug mode
DEBUG = True

# GOAP thresholds
CHASE_DISTANCE = 8
FLEE_HP = 30
ATTACK_RANGE = 1

# AI enabled by default
AI_ENABLED = True
