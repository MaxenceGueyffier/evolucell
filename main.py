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
        #self.quadtree_test = np.array([])



    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.key.set_repeat(150,50)
        self.clock = pygame.time.Clock()

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background) 

        #debug screen
        self.debug_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.debug_screen.convert_alpha()

        #food screen
        self.food_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #cell_screen
        self.cell_screen = pygame.surface.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #first quadtree
        boundary = Rectangle(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, color.boudaries_quadtree)
        self.quadtree = Quadtree(2, boundary)
    
        #launching food
        for i in range(100):
            self.pool_food = np.append(self.pool_food, Food(size=1))
            self.quadtree.insert(self.pool_food[i].pos)
        food1 = Food(500,10)
        self.pool_food = np.append(self.pool_food, food1)
        self.quadtree.insert(food1.pos)

        #self.quadtree.show(self.screen)

        #launching cell
        cell1 = Cell(500,300)
        self.pool_cell = np.append(self.pool_cell, cell1)
  
        #display everything on screen
        self.on_render()
        
        pygame.display.flip()
        
        self._running = True



    def on_event(self, event):
        #quit the app
        if event.type == pygame.QUIT:
            self._running = False

        #press the mouse somewhere on the screen to add/delete food
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            food = Food(x,y,1)
            if self.quadtree.insert(food.pos) :
                self.pool_food = np.append(self.pool_food, food)
            else:
                for index in range(len(self.pool_food)):
                    if self.pool_food[index].pos == food.pos :
                        self.pool_food = np.delete(self.pool_food, [index])
                        break
        
        #use zqsd keys to move the cell
        if event.type == pygame.KEYDOWN:
            if len(self.pool_cell) != 0 :
                if event.key == pygame.K_z:
                    self.pool_cell[0].move_forward()
                if event.key == pygame.K_s:
                    self.pool_cell[0].move_backward()
                if event.key == pygame.K_q:
                    self.pool_cell[0].turn_left()
                if event.key == pygame.K_d:
                    self.pool_cell[0].turn_right()



    def on_loop(self):
        #tick every frame
        self.clock.tick(FPS)
        clear_surface(self.debug_screen)

        for cindex in range(len(self.pool_cell)) :
            #decrease energy every frame
            self.pool_cell[cindex].decrease_energy()  

            #if there is any colision btwn a cell and some food, the cell eat the food
            list_object_colision=is_colision(self.pool_cell[cindex], Food, self.quadtree)
            list_object_colision = np.reshape(list_object_colision, (-1,2))
            for food_x, food_y in list_object_colision:
                self.quadtree.delete((food_x, food_y))
                for index in range(len(self.pool_food)):
                    if self.pool_food[index].pos == (food_x, food_y):
                        self.pool_food = np.delete(self.pool_food, [index])
                        self.pool_cell[cindex].eat()
                        print(self.pool_cell[cindex].energy_level)
                        break
            
            #if a cell is dead, delete it from the the list cell_pool
            if self.pool_cell[cindex].is_dead():
                self.pool_cell = np.delete(self.pool_cell, [cindex])
                print(f'cell n°{cindex} is dead')

        #self.quadtree_test = get_quadtrees_from_a_sprite(self.pool_cell[0], self.quadtree, get_maximal_depth(self.pool_cell[0]))

        pygame.display.flip()

    def on_render(self):
        #erase main screen
        self.screen.fill(color.background) 

        # self.quadtree.show(self.debug_screen)
        # for qt in self.quadtree_test :
        #     qt.show(self.debug_screen, (255,0,0))

        #print each food on food_screen
        clear_surface(self.food_screen)
        for food in self.pool_food:
            self.food_screen.blit(food.img, food)

        #print each cell on cell_screen
        clear_surface(self.cell_screen)
        for cell in self.pool_cell:
            self.cell_screen.blit(cell.img, cell)

        #copy every screen into the main screen
        self.screen.blit(self.cell_screen, (0,0))
        self.screen.blit(self.food_screen, (0,0))
        self.screen.blit(self.debug_screen, (0,0))

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