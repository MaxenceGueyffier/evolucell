import pygame
import math
from sprite import Sprite
from random import choice, randint
import common.globals as globals


class Cell(Sprite): 
    energy_level_init = 100
    energy_level = energy_level_init
    speed = 5*globals.time_speed
    angular_speed = 5*globals.time_speed
    direction = 0
    posx = None
    posy = None
    width = None
    height = None
    color_variation = (0,0,0)

    def __init__(self, posx=None, posy=None):
        super().__init__("body.png", posx, posy)
        self.generation = 0

    def random_walk(self):
        moves = ["forward"]*40 + ["left"]*25 + ["right"]*25 + ["backward"]*10
        move = choice(moves)

        if move == "forward":
            self.move_forward()
        elif move == "left":
            self.turn_left()
        elif move == "right":
            self.turn_right()
        else :
            self.move_backward()


    def move_forward (self):
        future_posx = self.posx + self.speed*math.cos(math.radians(self.direction))
        future_posy = self.posy - self.speed*math.sin(math.radians(self.direction))
        if self.is_inside_boudaries(future_posx, future_posy, self.width, self.height) :
            self.posx = future_posx
            self.posy = future_posy
            self.rect = self.img.get_rect(center = self.img.get_rect(center = (self.posx, self.posy)).center)
            self.mask = pygame.mask.from_surface(self.img)

    def is_inside_boudaries(self, future_posx, future_posy, future_width, future_height):
        if future_posx-future_width/2 >= 0 and future_posx+future_width/2 <= globals.SCREEN_WIDTH :
            if future_posy-future_height/2 >= 0 and future_posy+future_height/2 <= globals.SCREEN_HEIGHT :
                return True
        return False
    
    def move_backward (self):
        self.direction -= 180
        self.direction %= 360
        self.move_forward()
        self.direction -= 180
        self.direction %= 360

    def turn_left (self):
        future_direction = self.direction + self.angular_speed
        self.turn(future_direction)

    def turn_right (self):
        future_direction = self.direction - self.angular_speed
        self.turn(future_direction)

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
    
    def eat(self):
        self.energy_level += 50
        
    def decrease_energy(self):
        self.energy_level -= 0.5*globals.time_speed

    def is_dead(self):
        if self.energy_level <= 0:
            return True
        else :
            return False
        
    def is_pregnant(self):
        if self.energy_level >= 3*self.energy_level_init:
            return True
        else :
            return False

    def give_birth(self):
        self.energy_level -= self.energy_level_init
        child = Cell(int(self.posx), int(self.posy))
        child.generation = self.generation+1
        child.evolve()
        child.direction = randint(0,360)
        child.update_speed()
        return child
    
    def evolve(self):
        list_evolution = ["red"]+["blue"]+["green"]+["no evolution"]*7
        choice_criterion = choice(list_evolution)

        (r,g,b) = self.color_variation
        if choice_criterion == "red":
            r = r+randint(-50,50)
            self.color_variation = (r,g,b)

        elif choice_criterion == "blue":
            g = g+randint(-50,50)
            self.color_variation = (r,g,b)

        elif choice_criterion == "green":
            b = b+randint(-50,50)
            self.color_variation = (r,g,b)

        
        if choice_criterion != "no evolution" :
            print("____"+choice_criterion)
            print(self.color_variation)
            print(self.generation)


        self.color = self.shift_color(self.color_variation)

        

    def update_speed(self):
        """modify the speed according to the timespeed ts"""
        self.speed = 5*globals.time_speed
        self.angular_speed = 5*globals.time_speed

