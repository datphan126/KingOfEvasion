'''
Created on Apr 2, 2019

@author: sojin
'''

from win32api import GetSystemMetrics

# Define screen size
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080

# Game Speed
BALL_MOVE_SPEED_EASY = 10
BALL_MOVE_SPEED_MED = 11
BALL_MOVE_SPEED_HARD = 11
BALL_MOVE_SPEED_IMPOSSIBLE = 13

# Number of balls
BALL_LIMIT_EASY = 0.007
BALL_LIMIT_MED = 0.008
BALL_LIMIT_HARD = 0.009
BALL_LIMIT_IMPOSSIBLE = 0.012

# Speed of balls increases after players get a specific amount of points 
SPEED_INCREASE_POINTS = 25

# Images
BALL_IMG = "Asteroid.png"
BACKGROUND_IMG = "Space2.jpg"
PLAYER_IMG = "ufo.png"
REWARD_IMG = "star.png"