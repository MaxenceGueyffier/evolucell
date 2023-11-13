import pygame
import math
from copy import deepcopy
from random import choice, randint

from .sprite import Sprite
from .common import globals as globals


class Cell(Sprite): 

    def __init__(self, posx=None, posy=None, genetical_features=None, generation=0):
        super().__init__("body.png", posx, posy)
        self.generation = generation
        self.direction = randint(0,360)
        self.size = 1
        if not genetical_features==None:
            self.genetical_features = genetical_features
        else :
            self.genetical_features = {
                "color_variation" : (0,0,0),
                "size_variation" : 1,
                "initial_energy" : 100,
                "pregnancy_threshold" : 3
            }
        #adapt features according to genetical_features
        self.shift_color(self.genetical_features["color_variation"])
        self.change_size(self.genetical_features["size_variation"])
        self.energy_level_init = int(self.genetical_features["initial_energy"]/(self.size**2))
        self.energy_level = self.energy_level_init
        self.update_speed()


    def random_walk(self):
        """move randomly"""
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
        """use only after turn_left or turn_right"""
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
    
    def is_inside_boudaries(self, future_posx, future_posy, future_width, future_height):
        """check if a cell will still be inside the boundaries of the screen"""
        if future_posx-future_width/2 >= 0 and future_posx+future_width/2 <= globals.SCREEN_WIDTH :
            if future_posy-future_height/2 >= 0 and future_posy+future_height/2 <= globals.SCREEN_HEIGHT :
                return True
        return False
    
    def eat(self):
        """increase the energy of the cell"""
        self.energy_level += 50
        
    def decrease_energy(self):
        """decrease the energy of the cell"""
        self.energy_level -= 0.5*globals.time_speed

    def is_dead(self):
        """if the cell as not enough energy to survive return True, else return False"""
        if self.energy_level <= 0:
            return True
        else :
            return False
        
    def is_pregnant(self):
        """if the cell as enough energy to evolve return True, else return False"""
        if self.energy_level > int(self.genetical_features["pregnancy_threshold"]*self.energy_level_init):
            return True
        else :
            return False

    def give_birth(self):
        """create a new cell with a slight proability to evolve"""
        #energy needed to give_birth
        self.energy_level -= self.energy_level_init
        #change child's features
        child_features = deepcopy(self.genetical_features)
        feature_name, feature_value = self.feature_to_evolve()
        if feature_name != "no_evolution":
            print("mutation ! "+feature_name+" : "+str(self.genetical_features[feature_name])+" -> "+str(feature_value))
        child_features[feature_name] = feature_value
        #create the child, a new cell
        child = Cell(int(self.posx), int(self.posy), child_features, self.generation+1)
        #increase generation
        #chose a random direction
        return child
    
    def feature_to_evolve(self):
        """select a feature to evolve, return its name and its new value"""
        #list every evolution possible and its weight
        list_evolution = ["no_evolution"]*100+["red"]+["blue"]+["green"]+["size_variation"]+["initial_energy"]+["pregnancy_threshold"]
        #chose one of them
        choice_criterion = choice(list_evolution)

        #select a random color to modify to a random value
        (r,g,b) = self.genetical_features["color_variation"]
        if choice_criterion == "red":
            r = r+randint(-50,50)
            return "color_variation", (r,g,b)
        elif choice_criterion == "blue":
            g = g+randint(-50,50)
            return "color_variation", (r,g,b)
        elif choice_criterion == "green":
            b = b+randint(-50,50)
            return "color_variation", (r,g,b)
        #change size
        elif choice_criterion == "size_variation" :
            coef = max(self.genetical_features["size_variation"] + randint(-2,2)/10, 0.4)
            return "size_variation", coef
        #change initial energy
        elif choice_criterion == "initial_energy" :
            init_energy = max(self.genetical_features["initial_energy"] + randint(-15,15), 25)
            return "initial_energy", init_energy
        #change thre
        elif choice_criterion == "pregnancy_threshold" :
            pregnancy_threshold = max(round(self.genetical_features["pregnancy_threshold"] + randint(-3, 3)/10, 2), 1.1)
            return "pregnancy_threshold", pregnancy_threshold

        #no evolution
        else :
            return "no_evolution", None


    def change_size(self, coef):
        """modify size of the image
        coef : an integer which will be multiplicated to width and height ot determine the new size"""
        if self.size*coef > 0.3 :
            self.size *= coef
            self.width = int(self.size*self.width)
            self.height = int(self.size*self.height)
            self.img_init = pygame.transform.scale(self.img_init, (self.width,self.height))
            self.img = pygame.transform.scale(self.img, (self.width,self.height))
            self.rect = self.img.get_rect(center=(self.posx, self.posy))

    def update_speed(self):
        """modify the speed according to the timespeed ts"""
        self.speed = 5*globals.time_speed/(self.size**2)
        self.angular_speed = 5*globals.time_speed/(self.size**2)

