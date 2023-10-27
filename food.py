import pygame
import data.default as default
import time
import random
from sprite import Sprite


 
class Food(Sprite):
    '''Food() generate a pearl at random location while Food(x,y) place the food at a specific location'''
    size = random.randrange(2, 5)/2

    def __init__(self, posx=None, posy=None):
        super().__init__("food.png", posx, posy)
        self.size = random.randrange(2, 5)/2
        self.img = pygame.transform.scale(self.img_init, (self.size*self.width,self.size*self.height))

    def grow(self):
        if self.size < 2 :
            self.size += 0.5
            self.img = pygame.transform.scale(self.img_init, (self.size*self.width,self.size*self.height))
            self.rect = self.img.get_rect(center=(self.posx, self.posy))


