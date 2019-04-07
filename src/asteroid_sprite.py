'''
Created on Apr 2, 2019

@author: sojin
'''
import game_definitions as gd
import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, image_file, name, location, radius, speed):
        # Call the parent class (Sprite) constructor
        super().__init__() 
        self.image = pygame.image.load(resource_path(image_file))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        
        self.name = name
        self.radius = radius
        
        # Speed and direction of asteroid
        self.change_x = speed
        self.change_y = speed
        
    def move_asteroid(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # Bounce the ball if it hits the borders
        if self.rect.y >= (gd.SCREEN_HEIGHT - self.radius):
            self.change_y = self.change_y * -1
            self.rect.y = gd.SCREEN_HEIGHT - self.radius - 1
        elif self.rect.y <= self.radius:
            self.change_y = self.change_y * -1
            self.rect.y = self.radius + 1
            
        if self.rect.x >= (gd.SCREEN_WIDTH - self.radius):
            self.change_x = self.change_x * -1
            self.rect.x = gd.SCREEN_WIDTH - self.radius - 1
        elif self.rect.x <= self.radius:
            self.change_x = self.change_x * -1
            self.rect.x = self.radius + 1