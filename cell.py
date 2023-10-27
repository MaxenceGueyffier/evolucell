import pygame
import math
from copy import deepcopy

class Cell: 
    weight = 1.0
    speed = 0.1
    angular_speed = 0.01
    direction = 0

    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.last_posx = posx
        self.last_posy = posy
        self.img_init = pygame.image.load("lib/body.png").convert_alpha()
        self.img = pygame.image.load("lib/body.png").convert_alpha()
        self.rect = self.img.get_rect(center=(self.posx, self.posy))

    def move_forward (self):
        self.posx += self.speed*math.cos(math.radians(self.direction))
        self.posy -= self.speed*math.sin(math.radians(self.direction))
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)


    def turn_left (self):
        self.direction += self.angular_speed
        self.direction %= 360
        self.img = pygame.transform.rotate(self.img_init, self.direction)
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)


    def turn_right (self):
        self.direction -= self.angular_speed
        self.direction %= 360

        self.img = pygame.transform.rotate(self.img_init, self.direction)
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)



