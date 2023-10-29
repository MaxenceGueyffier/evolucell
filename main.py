import pygame
from pygame.locals import *
from data.color import *
from data.default import *
from cell import Cell
from food import Food
from quadtree import Quadtree
from rectangle import Rectangle
import numpy as np



import time

 
class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.pool_cell = np.array([])
        self.pool_food = np.array([])

    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.key.set_repeat(160,50)
        self.clock = pygame.time.Clock()

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background)

        #cell test
        cell1 = Cell(400,400)
        self.pool_cell = np.append(self.pool_cell, cell1)
        self.screen.blit(self.pool_cell[0].img, self.pool_cell[0])

        #food test
        food1 = Food(400,400)
        self.pool_food = np.append(self.pool_food, food1)
        self.screen.blit(self.pool_food[0].img, self.pool_food[0])

        #quadtree test
        boundary = Rectangle(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, color.boudaries_quadtree)
        self.quadtree = Quadtree(1, boundary)
    
        #food test
        for i in range(10):
            self.pool_food = np.append(self.pool_food, Food(size = 0.5))
            self.screen.blit(self.pool_food[i].img, self.pool_food[i])
            self.quadtree.insert(self.pool_food[i].pos)

        self.quadtree.show(self.screen)

        #test

        
        #print(food_test.mask.overlap(cell_test.mask, (0,0)))
        

        pygame.display.flip()
        

        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print((x,y))
            food = Food(x,y,0.5)
            self.pool_food = np.append(self.pool_food, food)
            self.quadtree.insert(food.pos)
            self.screen.blit(food.img, food)

            
    def on_loop(self):
        self.clock.tick(FPS)

            
        self.quadtree.show(self.screen)


        pygame.display.flip()



    def on_render(self):
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