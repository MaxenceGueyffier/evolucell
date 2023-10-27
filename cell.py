import pygame
import math
from sprite import Sprite


class Cell(Sprite): 
    weight = 1.0
    speed = 0.1
    angular_speed = 0.01
    direction = 0

    def __init__(self, posx=None, posy=None):
        super().__init__("body.png", posx, posy)

    def move_forward (self):
        self.posx += self.speed*math.cos(math.radians(self.direction))
        self.posy -= self.speed*math.sin(math.radians(self.direction))
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)
        self.mask = pygame.mask.from_surface(self.img)


    def turn_left (self):
        self.direction += self.angular_speed
        self.direction %= 360
        self.img = pygame.transform.rotate(self.img_init, self.direction)
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)
        self.mask = pygame.mask.from_surface(self.img)


    def turn_right (self):
        self.direction -= self.angular_speed
        self.direction %= 360
        self.img = pygame.transform.rotate(self.img_init, self.direction)
        self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)
        self.mask = pygame.mask.from_surface(self.img)

    def give_birth():
        pass

    def die():
        pass
