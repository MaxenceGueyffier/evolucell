import pygame
from pygame.locals import *
from data.color import *
import data.default as default
from cell import Cell
from food import Food

import time

 
class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = default.SCREEN_WIDTH, default.SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.pool_cell = []
        self.pool_food = []

    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.key.set_repeat(160,50)

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background)

        #cell test
        cell1 = Cell(400,400)
        self.pool_cell.append(cell1)
        self.screen.blit(self.pool_cell[0].img, self.pool_cell[0])

        #food test
        for i in range(10):
            self.pool_food.append(Food())
            self.screen.blit(self.pool_food[i].img, self.pool_food[i])

        #test
        food_test = Food(100,100)
        cell_test = Cell (110,100)
        print(food_test.mask.overlap(cell_test.mask, (0,0)))
        self.screen.blit(food_test.img, food_test)
        self.screen.blit(cell_test.img, cell_test)


        pygame.display.flip()
        

        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
    def on_loop(self):
        



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