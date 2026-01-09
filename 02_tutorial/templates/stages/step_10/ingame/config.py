"""Step 10: Behavior Tree Enemy AI - Configuration"""

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
    "wall": "#",
    "obstacle": "#",
}

# Auto-save
AUTO_SAVE = True

# Debug mode
DEBUG = True

# BT thresholds
CHASE_DISTANCE = 5  # Condition: player close
FLEE_HP = 30        # Condition: low HP

# AI enabled by default
AI_ENABLED = True
