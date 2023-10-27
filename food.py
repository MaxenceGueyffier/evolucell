import pygame
from pygame.locals import *
from data.color import Color
from cell import Cell
import time

 
class Food:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1000, 600
        self.clock = pygame.time.Clock()
        self.pool = []
        self.color = Color()
