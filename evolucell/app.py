import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

from .common.color import *
from .common import globals as globals
from .cell import Cell
from .food import Food
from .quadtree import Quadtree, contain
from .rectangle import Rectangle
from .colision_handler import *

def clear_surface(surface):
        surface.fill([0,0,0,0])


class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.pool_cell = np.array([])
        self.pool_food = np.array([])
        #self.quadtree_test = np.array([])
        self.timer_food = 0
        self.wait_for_food = 0
        self.initial_qtt_of_food = 500
        



    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 15)
        pygame.key.set_repeat(150,50)
        self.clock = pygame.time.Clock()

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background) 

        #debug screen
        self.debug_screen = pygame.surface.Surface((globals.SCREEN_WIDTH,globals.SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.debug_screen.convert_alpha()
        self.pool_test = np.array([])

        #food screen
        self.food_screen = pygame.surface.Surface((globals.SCREEN_WIDTH,globals.SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #cell_screen
        self.cell_screen = pygame.surface.Surface((globals.SCREEN_WIDTH,globals.SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #first quadtree
        boundary = Rectangle(0,0, globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT, color.boudaries_quadtree)
        self.quadtree = Quadtree(2, boundary)
    
        #launching food
        for i in range(self.initial_qtt_of_food):
            self.pool_food = np.append(self.pool_food, Food(size=1))
            self.quadtree.insert(self.pool_food[i].pos)
        food1 = Food(500,10)
        self.pool_food = np.append(self.pool_food, food1)
        self.quadtree.insert(food1.pos)

        self.quadtree.show(self.screen)

        #launching cell
        cell1 = Cell(500,300)
        self.pool_cell = np.append(self.pool_cell, cell1)
  
        #display everything on screen
        self.on_render()
        
        pygame.display.flip()
        
        self._running = True

    
    def cell_handler (self):
        cindex = 0
        while cindex < len(self.pool_cell) and cindex >= 0:

            #if a cell is dead, delete it from the the list cell_pool
            x = int(self.pool_cell[cindex].posx)
            y = int(self.pool_cell[cindex].posy)
            if self.pool_cell[cindex].is_dead():
                self.pool_cell = np.delete(self.pool_cell, [cindex])
                #release some food while dying
                food1 = Food(x,y)
                self.pool_food = np.append(self.pool_food, food1)
                self.quadtree.insert(food1.pos)

                #update beacause the length of pool_cell has changed
                cindex -= 1
                
            else:
                
                #decrease energy every frame
                self.pool_cell[cindex].decrease_energy()  

                #if there is any colision btwn a cell and some food, the cell eat the food
                list_object_colision=is_colision(self.pool_cell[cindex], Food, self.quadtree)
                list_object_colision = np.reshape(list_object_colision, (-1,2))
                for food_x, food_y in list_object_colision:
                    if not self.quadtree.delete((food_x, food_y)):
                        print("ERROR : food couldn't be deleted",food_x, food_y)
                        # f_test = Food(int(food_x), int(food_y))
                        # self.pool_test = np.append(self.pool_test, f_test)
                    else :
                        for index in range(len(self.pool_food)):
                            if self.pool_food[index].pos == (food_x, food_y):
                                self.pool_food = np.delete(self.pool_food, [index])
                                self.pool_cell[cindex].eat()
                                break

                #if a cell has enough energy, it gives birth to another cell
                if self.pool_cell[cindex].is_pregnant():
                    child = self.pool_cell[cindex].give_birth()
                    self.pool_cell = np.append(self.pool_cell, child)

                #random walk
                self.pool_cell[cindex].random_walk()

            cindex += 1

    def food_handler (self):
        if self.pool_food.size <= self.initial_qtt_of_food :
            current_time = pygame.time.get_ticks() 
            if current_time - self.timer_food >= self.wait_for_food*1000/globals.time_speed :
                self.timer_food = current_time
                f = Food(size=1)
                if self.quadtree.insert(f.pos) :
                    self.pool_food = np.append(self.pool_food, f)


                




    def on_event(self, event):
        #quit the app
        if event.type == pygame.QUIT:
            self._running = False

        #press the mouse somewhere on the screen to add cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            keys  = pygame.key.get_pressed()
            x, y = pygame.mouse.get_pos()
            if keys[pygame.K_q]:
                print(self.quadtree.get_last_quadtree((x,y)).particles)
            else :
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] :
                    f = Food(x,y,1)
                    if self.quadtree.insert(f.pos):
                        self.pool_food = np.append(self.pool_food, f)
                    else :
                        print("ERROR : food couldn't be appened")
                    
                else :
                    cell = Cell(x,y)
                    self.pool_cell = np.append(self.pool_cell, cell)
            
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
            if event.key == pygame.K_p:
                globals.increase_speed()
                if len(self.pool_cell) != 0 :
                    for cell in self.pool_cell:
                        cell.update_speed()
            if event.key == pygame.K_m:
                globals.decrease_speed()
                if len(self.pool_cell) != 0 :
                    for cell in self.pool_cell:
                        cell.update_speed()
            if event.key == pygame.K_SPACE:
                for food in self.pool_food:
                    self.quadtree.delete(food.pos)
                self.pool_food = np.array([])




    def on_loop(self):
        #tick every frame
        self.clock.tick(globals.FPS)
        clear_surface(self.debug_screen)

        self.cell_handler()
            
        self.food_handler()

        #self.quadtree_test = get_quadtrees_from_a_sprite(self.pool_cell[0], self.quadtree, get_maximal_depth(self.pool_cell[0]))

        pygame.display.flip()

    def on_render(self):
        #erase main screen
        self.screen.fill(color.background) 

        #print useful data on debug_screen
        clear_surface(self.debug_screen)
        #self.quadtree.show(self.debug_screen)
        # for qt in self.quadtree_test :
        #     qt.show(self.debug_screen, (255,0,0))
        sentence_speed = "x"+str(globals.time_speed)+" : "+str(int(self.clock.get_fps()))+" FPS"
        time_surface = self.my_font.render(sentence_speed, False, (0, 0, 0))
        self.debug_screen.blit(time_surface, (0,0))
        for test in self.pool_test:
            test.shift_color((-255,-255,+255))
            self.debug_screen.blit(test.img, test)

        #print each food on food_screen
        clear_surface(self.food_screen)
        for food in self.pool_food:
            qt_final = self.quadtree.get_last_quadtree(food.pos)
            if not contain(food.pos, qt_final.particles) :
                print("ERROR : unknown")
                self.quadtree.delete(food.pos)
                for index in range(len(self.pool_food)):
                    if self.pool_food[index].pos == (food.posx, food.posy):
                        self.pool_food = np.delete(self.pool_food, [index])
                        break
                food.shift_color((255,-255,-255))
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
 
