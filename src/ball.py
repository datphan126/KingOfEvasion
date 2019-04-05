'''
Created on Apr 2, 2019

@author: sojin
'''
import game_definitions as gd

class Ball():
    
    def __init__(self, name, x_start_pos, y_start_pos, size,game_speed):
        self.name = name
        self.size = size
        self.x_pos = x_start_pos
        self.y_pos = y_start_pos
        # Speed and direction of circle
        self.circle_change_x = game_speed
        self.circle_change_y = game_speed
        
    def move_ball(self):
        self.x_pos += self.circle_change_x
        self.y_pos += self.circle_change_y
        
        # Bounce the ball if it hits the borders
        if self.y_pos >= (gd.SCREEN_HEIGHT - self.size) or self.y_pos <= self.size:
            self.circle_change_y = self.circle_change_y * -1
        if self.x_pos >= (gd.SCREEN_WIDTH - self.size) or self.x_pos <= self.size:
            self.circle_change_x = self.circle_change_x * -1