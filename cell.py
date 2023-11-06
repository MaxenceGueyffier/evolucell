import pygame
import math
from sprite import Sprite
from common.default import *


class Cell(Sprite): 
    energy_level = 100
    speed = 5
    angular_speed = 5
    direction = 0
    posx = None
    posy = None
    width = None
    height = None

    def __init__(self, posx=None, posy=None):
        super().__init__("body.png", posx, posy)

    def move_forward (self):
        future_posx = self.posx + self.speed*math.cos(math.radians(self.direction))
        future_posy = self.posy - self.speed*math.sin(math.radians(self.direction))
        if self.is_inside_boudaries(future_posx, future_posy, self.width, self.height) :
            self.posx = future_posx
            self.posy = future_posy
            self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)
            self.mask = pygame.mask.from_surface(self.img)
    
    def move_backward (self):
        self.direction -= 180
        self.direction %= 360
        self.move_forward()
        self.direction -= 180
        self.direction %= 360

    def turn(self, future_direction):
        future_direction = future_direction % 360
        future_img = pygame.transform.rotate(self.img_init, future_direction)
        future_width, future_height = future_img.get_size()
        if self.is_inside_boudaries(self.posx, self.posy, future_width, future_height):
            self.direction = future_direction
            self.img = future_img
            self.width = future_width
            self.height = future_height
            self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center) 
            self.mask = pygame.mask.from_surface(self.img)

    def turn_left (self):
        future_direction = self.direction + self.angular_speed
        self.turn(future_direction)

    def turn_right (self):
        future_direction = self.direction - self.angular_speed
        self.turn(future_direction)

    def is_inside_boudaries(self, future_posx, future_posy, future_width, future_height):
        if future_posx-future_width/2 >= 0 and future_posx+future_width/2 <= SCREEN_WIDTH :
            if future_posy-future_height/2 >= 0 and future_posy+future_height/2 <= SCREEN_HEIGHT :
                return True
        return False
    
    def eat(self):
        self.energy_level += 50
        
    def decrease_energy(self):
        self.energy_level -= 0.5

    def give_birth():
        pass

    def is_dead(self):
        if self.energy_level <= 0:
            return True
        else :
            return False
