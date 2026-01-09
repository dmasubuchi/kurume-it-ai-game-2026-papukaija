"""Step 09: FSM Enemy AI - Configuration"""

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

# FSM thresholds
CHASE_DISTANCE = 5  # IDLE -> CHASE when distance <= this
LOSE_DISTANCE = 8   # CHASE -> IDLE when distance >= this
FLEE_HP = 30        # CHASE -> FLEE when HP <= this

# AI enabled by default
AI_ENABLED = True
