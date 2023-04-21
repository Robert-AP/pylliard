#imports
import pygame as pg
from pygame.locals import *
import sys


#defines the ball as a class
class Ball:

    def __init__(self, colour, center, radius, velocity):
        self.colour = colour
        self.radius = radius
        self.center = center

        self.velocity = velocity
        self.acceleration = 0.003
        self.area = [0, 0]

        self.collision_status = 0

    def update(self, res, balls):
        self.ball_deccelerate()
        self.collide_border(res)
        self.ball_stop()

    def ball_draw(self, surface):
        self.ball = pg.draw.circle(surface, self.colour, tuple(self.center),
                                   self.radius)

    def ball_move(self):  
        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]


    def collide_border(self, resolution):

        if self.center[0] + self.radius + self.velocity[0] >= resolution[2] + resolution[0]:  #right border
            self.center[0] = resolution[2] + resolution[0] - self.radius
            self.velocity[0] = -self.velocity[0]

        if self.center[0] + self.radius + self.velocity[0] <= resolution[0]:  #left border
            self.center[0] = resolution[0] + self.radius
            self.velocity[0] = -self.velocity[0]

        if self.center[1] + self.radius + self.velocity[1] >= resolution[3] + resolution[1]:  #bottom border
            self.center[1] = resolution[3] + resolution[1] - self.radius
            self.velocity[1] = -self.velocity[1]

        if self.center[1] + self.radius + self.velocity[1] <= resolution[1]:  #top border
            self.center[1] = resolution[1] + self.radius
            self.velocity[1] = -self.velocity[1]

    def ball_deccelerate(self):
        if self.velocity[0] > 0:
            self.velocity[0] -= self.acceleration
        if self.velocity[1] > 0:
            self.velocity[1] -= self.acceleration
        if self.velocity[0] < 0:
            self.velocity[0] += self.acceleration
        if self.velocity[1] < 0:
            self.velocity[1] += self.acceleration

    def ball_stop(self):
        if self.velocity[0] < self.acceleration and self.velocity[0] > 0:
            self.velocity[0] = 0
        elif self.velocity[0] > -self.acceleration and self.velocity[0] < 0:
            self.velocity[0] = 0
            
        if self.velocity[1] < self.acceleration and self.velocity[1] > 0:
            self.velocity[1] = 0
        elif self.velocity[1] > -self.acceleration and self.velocity[1] < 0:
            self.velocity[1] = 0
            
