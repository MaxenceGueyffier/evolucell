import pygame
from data.color import *
from pygame.math import Vector2


class Rectangle:
    """
    Rectangle(x, y, width, height, color=(0,0,0), line_thickness=1)\n
    Rectangle used as boundaries by a Quadtree\n
    x,y are the coordinates of the upper left corner of the rectangle
    """
    def __init__(self, x:int, y:int, width, height, color=(0,0,0), line_thickness=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.line_thickness = line_thickness

    def containsParticle(self, particle):     
        (x_particle, y_particle) = particle
        if x_particle >= self.x and x_particle <= self.x+self.width and y_particle >= self.y and y_particle <= self.y+self.height:
            return True
        else:
            return False

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], self.line_thickness)
        