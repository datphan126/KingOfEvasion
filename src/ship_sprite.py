'''
Created on Apr 6, 2019

@author: sojin
'''
import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Ship(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        # Call the parent class (Sprite) constructor
        super().__init__() 
        self.image = pygame.image.load(resource_path(image_file))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        
    def move_ship(self, x, y):
        # Change the moving direction of the ship
        self.change_x += x
        self.change_y += y
 
    def update(self):
        # Get a new position for the ship
        self.rect.x += self.change_x
        self.rect.y += self.change_y