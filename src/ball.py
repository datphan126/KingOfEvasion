'''
Created on Apr 2, 2019

@author: sojin
'''
import game_definitions as gd

class Ball():
    
    def __init__(self, name, x_start_pos, y_start_pos, radius,game_speed):
        self.name = name
        self.radius = radius
        self.x_pos = x_start_pos
        self.y_pos = y_start_pos
        # Speed and direction of circle
        self.circle_change_x = game_speed
        self.circle_change_y = game_speed
        
    def move_ball(self):
        self.x_pos += self.circle_change_x
        self.y_pos += self.circle_change_y
        
        # Bounce the ball if it hits the borders
        if self.y_pos >= (gd.SCREEN_HEIGHT - self.radius):
            self.circle_change_y = self.circle_change_y * -1
            self.y_pos = gd.SCREEN_HEIGHT - self.radius - 1
        elif self.y_pos <= self.radius:
            self.circle_change_y = self.circle_change_y * -1
            self.y_pos = self.radius + 1
            
        if self.x_pos >= (gd.SCREEN_WIDTH - self.radius):
            self.circle_change_x = self.circle_change_x * -1
            self.x_pos = gd.SCREEN_WIDTH - self.radius - 1
        elif self.x_pos <= self.radius:
            self.circle_change_x = self.circle_change_x * -1
            self.x_pos = self.radius + 1