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

class Reward(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
#         pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        # Call the parent class (Sprite) constructor
        super().__init__() 
        self.image = pygame.image.load(resource_path(image_file))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location