#pylint: disable=all
from math import pi, cos
from Matrices import Point, Vector
from Base3DObjects import Color

# Cheats
JUMP = False # Not implemented
WALLHACK = False # Not implemented
ALLOW_UP_DOWN_LOOK = False

# Window
WINDOW_HEIGHT = 600
WINDOW_WIDTH  = 800

# Camera
DEFAULT_FOV = pi / 2
DEFAULT_NEAR = 0.1
DEFAULT_FAR  = 37

# Setup
PLAYER_RADIUS = 1.0
PLAYER_STARTING_POS  = Point(5, PLAYER_RADIUS, 5)
PLAYER_STARTING_LOOK = PLAYER_STARTING_POS + Point(5, 0, 0)
VECTOR_UP = Vector(0, 1, 0)

# Colors
COLOR_PLAYER  = Color(0.8, 0.05, 0.8)
COLOR_WALL    = Color(0.7, 0.7, 0.7)
COLOR_FLOOR   = Color(0.05, 0.9, 0.1)
COLOR_ENEMY   = Color(0.9, 0.05, 0.05)
COLOR_BG      = Color(0.0, 0.0, 0.0)
COLOR_GOAL    = Color(0.05, 0.05, 0.9)
COLOR_CEILING = Color(0.5, 0.0, 0.0)

# Specular
SPECULAR_PLAYER  = Color(0.5, 0.5, 0.5)
SPECULAR_WALL    = Color(0.5, 0.5, 0.5)
SPECULAR_FLOOR   = Color(0.5, 0.5, 0.5)
SPECULAR_ENEMY   = Color(0.5, 0.5, 0.5)
SPECULAR_GOAL    = Color(0.1, 0.1, 0.1)
SPECULAR_CEILING = Color(0.5, 0.5, 0.5)

# Shiny
SHINY_PLAYER = 10
SHINY_WALL   = 10
SHINY_FLOOR  = 10
SHINY_ENEMY  = 10
SHINY_GOAL   = 250
SHINY_CEILING = 500

# Emit
EMIT_PLAYER = 0.0
EMIT_WALL = 0.0
EMIT_FLOOR = 0.0
EMIT_ENEMY = 0.0
EMIT_GOAL = 0.5
EMIT_CEILING = 0.0

# Game Settings
DEFAULT_GRAVITY = 0.0
PLAYER_MOVE_SPEED = 12.0
PLAYER_TURN_SPEED = 100.0
PLAYER_FOV_SPEED  = 0.25

# Lights
PLAYER_LIGHT_COLOR = Color(0.2, 0.01, 0.01)
PLAYER_LIGHT_ATT_CONSTANT = 1.0
PLAYER_LIGHT_ATT_LINEAR = 0.35
PLAYER_LIGHT_ATT_QUAD = 0.44

GLOBAL_LIGHT_COLOR = Color(0.1, 0.1, 0.1)
GLOBAL_LIGHT_DIRECTION = Point(-0.2, -1.0, -0.3)

PLAYER_FLASHLIGHT_COLOR = Color(1.0, 209/255, 178/255)
PLAYER_FLASHLIGHT_CUTOFF = cos((45 + 6.5) * pi/180)
PLAYER_FLASHLIGHT_OUTER_CUTOFF = cos((45 + 11.5) * pi/180)
PLAYER_FLASHLIGHT_ATT_CONSTANT = 1.0
PLAYER_FLASHLIGHT_ATT_LINEAR = 0.14
PLAYER_FLASHLIGHT_ATT_QUAD = 0.07

# Set to 0 to disable
FOG_DISTANCE = 32 # this roughly corresponds to the range of the flashlight
FOG_COLOR = Color(0.1, 0.1, 0.1)

# Maze
# Minimum size is 5x5 and only odd numbers allowed
# There is no maximum, but above 25 you'll run into severe performance issues
MAZE_WIDTH  = 51
MAZE_HEIGHT = 51
MAZE_COMPLEXITY = 0.75
MAZE_DENSITY = 0.75
MAZE_WALL_SIZE = 5
MAZE_FLOOR_THICK = 0.5
MAZE_GOAL_SIZE = 2

DRAW_ANGLE_CUTOFF = cos((45 + 45) * pi/180)
DRAW_ANGLE_MIN_DISTANCE = 6 ** 2
DRAW_DISTANCE_CUTOFF_SQUARED = FOG_DISTANCE ** 2