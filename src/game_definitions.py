'''
Created on Apr 2, 2019

@author: sojin
'''

from win32api import GetSystemMetrics

# Define screen size
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 800

# Game Speed
ASTEROID_MOVE_SPEED_EASY = 10
ASTEROID_MOVE_SPEED_MED = 11
ASTEROID_MOVE_SPEED_HARD = 11
ASTEROID_MOVE_SPEED_IMPOSSIBLE = 13

# Number of balls
ASTEROID_LIMIT_EASY = 0.007
ASTEROID_LIMIT_MED = 0.008
ASTEROID_LIMIT_HARD = 0.009
ASTEROID_LIMIT_IMPOSSIBLE = 0.012

# Asteroid radius
ASTEROID_RADIUS = 50

# Speed of balls increases after players get a specific amount of points 
SPEED_INCREASE_POINTS = 20

# Images
ASTEROID_IMG = "Asteroid.png"
BACKGROUND_IMG = "Space2.jpg"
PLAYER_IMG = "ufo.png"
REWARD_IMG = "star.png"

# Timer limit - In seconds
TIMER_LIMIT_EASY = 15
TIMER_LIMIT_MED = 10
TIMER_LIMIT_HARD = 10
TIMER_LIMIT_IMPOSSIBLE = 8

# Game Controllers
GAME_CONTROLLER_MOUSE = "MOUSE"
GAME_CONTROLLER_KEYBOARD = "KEYBOARD"

# Ship attributes
SHIP_SPEED = 25
SHIP_RADIUS = 25

# Reward attributes
REWARD_RADIUS = 25

# Highscore filename
HIGHSCORE_FILE_NAME = "highscores.csv"