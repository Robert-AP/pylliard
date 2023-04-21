#imports
import pygame
from pygame.locals import *
import sys

WHITE = (255,255,255)


class Mouse():
    def __init__(self):
        self.on_white = False
        
        
    def get_list_pos(self):  # gets mouse position as a list
        posList = []
        pos = pygame.mouse.get_pos()
        for item in pos:
            posList.append(item)
        return posList
    
    
    def get_mouse_data(self):
        left, middle, right = pygame.mouse.get_pressed()
        self.mouseData = {'pos': self.get_list_pos(), 'left': left, 'middle': middle, 'right': right}
        return self.mouseData
