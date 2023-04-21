#imports
import pygame 
from pygame.locals import *
import sys

#constants
BROWN = (150,75,0)
GREEN = (38, 130, 35)
BLACK =(0,0,0)
DISPLAY_SIZE = (640, 360)
HOLE_RADIUS = 14
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE)
RES = [31.22, 36, 581.81, 288]
holeData = [[35,35],[320,35],[610,35],[35,325],[320,325],[615, 320]]


#defines the board as a class
class Board:
    def __init__(self):
        self.position = []

    #initialises board
    def draw_table(self):
        pygame.draw.rect(DISPLAY, (BROWN), pygame.Rect(0, 0, DISPLAY_SIZE[0], DISPLAY_SIZE[1]))
        pygame.draw.rect(DISPLAY, (GREEN), pygame.Rect(RES))

        
class Hole:
    def __init__(self, center, DISPLAY):
        self.colour = BLACK
        self.center = center
        self.radius = HOLE_RADIUS

    def setup(self, holeData):
        self.create_holes(holeData)
        
    def hole_draw(self, surface):
        self.hole = pygame.draw.circle(surface, self.colour, tuple(self.center), self.radius)
