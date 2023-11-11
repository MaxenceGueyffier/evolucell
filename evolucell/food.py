import pygame
import random

from .common import globals as globals
from .sprite import Sprite


 
class Food(Sprite):
    '''Food() generate a pearl at random location while Food(x,y,size) place the food at a specific location and the image is zoomed according to the size factor'''
    

    def __init__(self, posx=None, posy=None, size=1 ):
        super().__init__("food.png", posx, posy)
        if size == None:
            self.size = random.randrange(2, 4)/2
        else :
            self.size = size
        self.img = pygame.transform.scale(self.img_init, (self.size*self.width,self.size*self.height))
        self.rect = self.img.get_rect(center=(self.posx, self.posy))
         

    def grow(self):
        if self.size < 2 :
            self.size += 0.5
            self.img = pygame.transform.scale(self.img_init, (self.size*self.width,self.size*self.height))
            self.rect = self.img.get_rect(center=(self.posx, self.posy))


