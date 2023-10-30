import pygame
from data.default import *
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
        self.img_init = pygame.image.load("lib/"+img_name).convert_alpha()
        self.img = pygame.image.load("lib/"+img_name).convert_alpha()
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
    