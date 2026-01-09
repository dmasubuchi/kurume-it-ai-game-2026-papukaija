"""Step 12: System AI (Director) - Configuration"""

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

# Director thresholds
LOW_HP_THRESHOLD = 30   # HP <= this -> HIGH tension
HIGH_HP_THRESHOLD = 70  # HP >= this -> LOW tension

# Tension affects enemy behavior
CHASE_DISTANCE_LOW = 8     # When tension is LOW
CHASE_DISTANCE_MID = 5     # When tension is MID
CHASE_DISTANCE_HIGH = 3    # When tension is HIGH

# AI enabled by default
AI_ENABLED = True
DIRECTOR_ENABLED = True
