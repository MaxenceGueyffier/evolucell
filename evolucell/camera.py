import pygame
from .rectangle import Rectangle
from .common import globals as globals


class Camera:
    def __init__(self, loc=(0,0), zoom=1):
        self.loc = loc #top_left corner of the camera
        self.zoom_coef = zoom
        self.boundaries = Rectangle(self.loc[0], self.loc[1], globals.screen_width, globals.screen_height)
        self.screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)

    def move(self, move_vector):
        (x,y) = move_vector
        self.loc = (self.loc[0]+x, self.loc[1]-y)
        self.boundaries.x = self.loc[0]
        self.boundaries.y = self.loc[1]

    def zoom(self, value):
        if (self.boundaries.width>1000 and value<0) or (self.boundaries.width<5000 and value>0):
            self.boundaries.height += value
            self.boundaries.width = int(self.boundaries.height * (globals.screen_width/globals.screen_height))
            self.loc = (self.loc[0]-(value*(globals.screen_width/globals.screen_height))/2, self.loc[1]-value/2)
            self.boundaries.x = self.loc[0]
            self.boundaries.y = self.loc[1]
            self.zoom_coef = globals.initial_screen_width/self.boundaries.width

    def get_relative_coordinates(self, local_coordinates):
        x,y = local_coordinates
        x = x/(globals.initial_screen_width/self.boundaries.width) + self.loc[0]
        y = y/(globals.initial_screen_width/self.boundaries.width) + self.loc[1]
        return int(x),int(y)

    def contains_particle(self, coordinates):
        if self.boundaries.containsParticle(coordinates) :
            return True
        else :
            return False
        
    def render(self, list_screens, ):
        self.screen.fill([0,0,0,0])
        self.screen.blits(list_screens)
        #self.camera_boundaries.draw(self.screen, color=(255,0,0))
        w = self.screen.get_width()*(globals.screen_width/self.boundaries.width)
        h = self.screen.get_height()*(globals.screen_height/self.boundaries.height)
        output = pygame.transform.scale(self.screen, (int(w),int(h)))
        return output, (-self.loc[0]*self.zoom_coef, -self.loc[1]*self.zoom_coef)
