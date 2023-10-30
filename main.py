import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
from common.color import *
from common.default import *
from cell import Cell
from food import Food
from quadtree import Quadtree
from rectangle import Rectangle
import numpy as np
from colision_handler import *



import time

def clear_surface(surface):
        surface.fill([0,0,0,0])


 
class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.pool_cell = np.array([])
        self.pool_food = np.array([])
        self.quadtree_test = np.array([])

    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.key.set_repeat(160,50)
        self.clock = pygame.time.Clock()

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background) 

        #food screen
        self.food_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #cell_screen
        self.cell_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #first quadtree
        boundary = Rectangle(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, color.boudaries_quadtree)
        self.quadtree = Quadtree(2, boundary)
    
        #food test
        for i in range(100):
            self.pool_food = np.append(self.pool_food, Food())
            self.quadtree.insert(self.pool_food[i].pos)
        food1 = Food(400,400)
        self.pool_food = np.append(self.pool_food, food1)
        self.quadtree.show(self.screen)

        #cell test
        cell1 = Cell(490,290)
        self.pool_cell = np.append(self.pool_cell, cell1)
  
        self.on_render()
        
        pygame.display.flip()
        
        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            #print((x,y))
            food = Food(x,y,2)
            self.pool_food = np.append(self.pool_food, food)
            self.quadtree.insert(food.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.pool_cell[0].move_forward()
            if event.key == pygame.K_q:
                self.pool_cell[0].turn_left()
            if event.key == pygame.K_d:
                self.pool_cell[0].turn_right()
            
    def on_loop(self):
        self.clock.tick(FPS)

        self.quadtree_test = get_quadtrees_from_a_sprite(self.pool_cell[0], self.quadtree, get_maximal_depth(self.pool_cell[0]))

        pygame.display.flip()

    def on_render(self):
        self.screen.fill(color.background) 

        self.quadtree.show(self.screen)
        for qt in self.quadtree_test :
            qt.show(self.screen, (255,0,0))

        for food in self.pool_food:
            self.food_screen.blit(food.img, food)
        
        for cell in self.pool_cell:
            clear_surface(self.cell_screen)
            self.cell_screen.blit(cell.img, cell)

        

        self.screen.blit(self.cell_screen, (0,0))
        self.screen.blit(self.food_screen, (0,0))

        pygame.display.flip()

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()