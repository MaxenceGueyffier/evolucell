import pygame
from common.globals import *
import random


class Sprite:
    '''
    Every movable object is defined by an image and a location. If no coordinate is specified, then a random value is chosen instead.\n
    img_init : image before deformation
    img : image after deformation
    mask : mask of the deformed image
    rect : rect
    posx : x-coordinate
    posy : y-coordinate
    width : width
    height : height


    '''
    def __init__(self, img_name : str, posx=None, posy=None):
        self.img_name = img_name
        self.img_init = pygame.image.load("lib/"+img_name).convert_alpha()
        self.img = self.img_init
        self.mask = pygame.mask.from_surface(self.img)
        self.width, self.height = self.img.get_size()

        #if no coordinate is specified, use a random location
        if posx is None and posy is None :
            self.posx = random.randrange(int(self.width/2),SCREEN_WIDTH-int(self.width/2))
            self.posy = random.randrange(int(self.height/2),SCREEN_HEIGHT-int(self.height/2))
        else :
            #if there is one, check first if it is valid
            if isinstance(posx, int) and isinstance(posy, int) :
                if posx>=(int(self.width/2)) and posx<=(SCREEN_WIDTH-int(self.width/2)):
                    if posy>=(int(self.height/2)) and posy<=(SCREEN_HEIGHT-int(self.height/2)):
                        self.posx = posx
                        self.posy = posy
            #if the format is incorrect, return an error message and define the location as the center of the screen
            else:
                print("ERROR : location type isn't correct, random location used instead")
                self.posx = random.randrange(int(self.width/2),SCREEN_WIDTH-int(self.width/2))
                self.posy = random.randrange(int(self.width/2),SCREEN_HEIGHT-int(self.width/2))
        self.pos = (self.posx,self.posy)

        self.rect = self.img.get_rect(center=(self.posx, self.posy))
    
    def shift_color(self, color_shift):
        """Fill all pixels of the original with color shifted from the original color, preserve transparency.
        color_shift : (shift_r, shift_g, shift_b,) tuple with every shift of every color 
        """
        r, g, b = color_shift
        for x in range(self.width):
            for y in range(self.height):
                old_r, old_g, old_b, old_a = self.img_init.get_at((x, y))
                new_r = max(0, min(255, old_r+r))
                new_g = max(0, min(255, old_g+g))
                new_b = max(0, min(255, old_b+b))

                self.img_init.set_at((x, y), pygame.Color(new_r, new_g, new_b, old_a))
                self.img.set_at((x, y), pygame.Color(new_r, new_g, new_b, old_a))
     
        return (new_r, new_g, new_b, old_a)
        