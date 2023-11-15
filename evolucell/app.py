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
        #main features of the App class
        self._running = True
        self.screen = None
        self.size = globals.screen_width, globals.screen_height
        self.clock = pygame.time.Clock()
        self.pool_cell = np.array([])
        #self.quadtree_test = np.array([])
        self.timer_food = 0
        self.wait_for_food = 0
        self.camera_loc = (0,0) #top_left corner of the camera
        self.camera_zoom = 1
        self.camera_boundaries = Rectangle(self.camera_loc[0], self.camera_loc[1], globals.screen_width, globals.screen_height)
        

    def on_init(self):
        """called only once, at the start of the program"""

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

        #camera screen
        self.camera_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.camera_screen.convert_alpha()

        #debug screen
        self.debug_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.debug_screen.convert_alpha()
        self.pool_test = np.array([])

        #food screen
        self.food_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #cell_screen
        self.cell_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()

        #first quadtree
        boundary = Rectangle(0,0, globals.playground_width, globals.playground_height, color.boudaries_quadtree)
        self.quadtree = Quadtree(2, boundary)
    
        #launching food
        for i in range(globals.initial_qtt_of_food):
            self.quadtree.insert(Food(size=1))
        food1 = Food(500,10)
        self.quadtree.insert(food1)

        self.quadtree.show(self.screen)

        #launching cell
        cell1 = Cell(500,300)
        self.pool_cell = np.append(self.pool_cell, cell1)
  
        #display everything on screen
        self.on_render()
        
        pygame.display.flip()
        
        self._running = True

    
    def cell_handler (self):
        """deal with life cycle of every cell"""

        cindex = 0
        while cindex < len(self.pool_cell) and cindex >= 0:

            #if a cell is dead, delete it from the the list cell_pool
            x = int(self.pool_cell[cindex].posx)
            y = int(self.pool_cell[cindex].posy)
            if self.pool_cell[cindex].is_dead():
                self.pool_cell = np.delete(self.pool_cell, [cindex])
                #release some food while dying
                food1 = Food(x,y)
                self.quadtree.insert(food1)

                #update beacause the length of pool_cell has changed
                cindex -= 1
                
            else:
                
                #decrease energy every frame
                self.pool_cell[cindex].decrease_energy()  

                #if there is any colision btwn a cell and some food, the cell eat the food
                list_object_colision=list_colision(self.pool_cell[cindex], self.quadtree)
                for food in list_object_colision:
                    self.quadtree.delete(food)
                    self.pool_cell[cindex].eat()

                #if a cell has enough energy, it gives birth to another cell
                if self.pool_cell[cindex].is_pregnant():
                    child = self.pool_cell[cindex].give_birth()
                    self.pool_cell = np.append(self.pool_cell, child)

                #random walk
                self.pool_cell[cindex].random_walk()

            cindex += 1

    def food_handler (self):
        """deal with the renewal of foods"""
        if self.quadtree.particles.size <= globals.initial_qtt_of_food :
            current_time = pygame.time.get_ticks() 
            if current_time - self.timer_food >= self.wait_for_food*1000/globals.time_speed :
                self.timer_food = current_time
                food = Food(size=1)
                self.quadtree.insert(food)


    def on_event(self, event):
        """process every user action"""

        #quit the app
        if event.type == pygame.QUIT:
            self._running = False

        #press the mouse somewhere on the screen to add cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            keys  = pygame.key.get_pressed()
            x, y = pygame.mouse.get_pos()
            x -= self.camera_loc[0]
            y -= self.camera_loc[1]
            if keys[pygame.K_q]:
                for p in self.quadtree.get_last_quadtree_from_pos((x,y)).particles :
                    print(p.pos)
            else :
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] :
                    self.quadtree.insert(Food(x,y,1))
                else :
                    cell = Cell(x,y)
                    self.pool_cell = np.append(self.pool_cell, cell)
            
        #use zqsd keys to move the cell
        if event.type == pygame.KEYDOWN:

            keys  = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                #zoom camera
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] :
                    step = 120
                    if keys[pygame.K_DOWN]:
                        if self.camera_boundaries.width < 5000 :
                            self.camera_boundaries.height += step
                    if keys[pygame.K_UP]:
                        if self.camera_boundaries.width > 1000 :
                            self.camera_boundaries.height -= step
                    self.camera_boundaries.width = int(self.camera_boundaries.height * (globals.screen_width/globals.screen_height))
                    self.camera_zoom = round(globals.initial_screen_width/self.camera_boundaries.width,2)
                
                #move camera
                else :
                    step = 10
                    if keys[pygame.K_UP]:
                        self.camera_loc = (self.camera_loc[0], self.camera_loc[1]-step)
                    if keys[pygame.K_DOWN]:
                        self.camera_loc = (self.camera_loc[0], self.camera_loc[1]+step)
                    if keys[pygame.K_LEFT]:
                        self.camera_loc = (self.camera_loc[0]-step, self.camera_loc[1])
                    if keys[pygame.K_RIGHT]:
                        self.camera_loc = (self.camera_loc[0]+step, self.camera_loc[1])
                    self.camera_boundaries = Rectangle(self.camera_loc[0], self.camera_loc[1], self.camera_boundaries.width, self.camera_boundaries.height)
                
                print(self.camera_zoom)
                print(self.camera_loc)
                print(self.camera_boundaries.width, self.camera_boundaries.height)

            #control first cell
            elif keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d]:
                if len(self.pool_cell) != 0 :
                    if keys[pygame.K_z]:
                        self.pool_cell[0].move_forward()
                    if keys[pygame.K_s]:
                        self.pool_cell[0].move_backward()
                    if keys[pygame.K_q]:
                        self.pool_cell[0].turn_left()
                    if keys[pygame.K_d]:
                        self.pool_cell[0].turn_right()
            
            #control time
            elif keys[pygame.K_p]:
                globals.increase_speed()
                if len(self.pool_cell) != 0 :
                    for cell in self.pool_cell:
                        cell.update_speed()
            elif keys[pygame.K_m]:
                globals.decrease_speed()
                if len(self.pool_cell) != 0 :
                    for cell in self.pool_cell:
                        cell.update_speed()

            #delete every food
            elif keys[pygame.K_SPACE]:
                for food in self.quadtree.particles:
                    self.quadtree.delete(food)
                self.quadtree.particles = np.array([])




    def on_loop(self):
        #tick every frame
        self.clock.tick(globals.fps)

        clear_surface(self.debug_screen)

        self.cell_handler()
            
        self.food_handler()

        #self.quadtree_test = get_quadtrees_from_a_sprite(self.pool_cell[0], self.quadtree, get_maximal_depth(self.pool_cell[0]))

        pygame.display.flip()


    def on_render(self):
        """manage the screen display"""

        #erase main screen
        self.screen.fill(color.background) 

        #print useful data on debug_screen
        #clear_surface(self.debug_screen)
        #self.quadtree.show(self.debug_screen)
        # for qt in self.quadtree_test :
        #     qt.show(self.debug_screen, (255,0,0))
        


        for test in self.pool_test:
            test.shift_color((-255,-255,+255))
            if self.camera_boundaries.containsParticle(test.pos) :
                self.debug_screen.blit(test.img, test)
            

        #print each food on food_screen
        clear_surface(self.food_screen)
        for food in self.quadtree.particles:
            qt_final = self.quadtree.get_last_quadtree_from_pos(food.pos)
            if not contain(food.pos, qt_final.particles) :
                print("ERROR : unknown")
                self.quadtree.delete(food)
                food.shift_color((255,-255,-255))
            if self.camera_boundaries.containsParticle(food.pos) :
                self.food_screen.blit(food.img, food)
        #self.food_screen = pygame.transform.scale(self.food_screen, (self.camera_boundaries.width, self.camera_boundaries.height))

        #print each cell on cell_screen
        clear_surface(self.cell_screen)
        for cell in self.pool_cell:
            if self.camera_boundaries.containsParticle((cell.posx, cell.posy)) :
                self.cell_screen.blit(cell.img, cell)
        #self.cell_screen = pygame.transform.scale(self.cell_screen, (self.camera_boundaries.width, self.camera_boundaries.height))
        

        #copy every screen into the main screen
        clear_surface(self.camera_screen)
        self.camera_screen.blits([(self.cell_screen, (0,0)),(self.food_screen, (0,0)),(self.debug_screen, (0,0))])
        self.camera_boundaries.draw(self.camera_screen, color=(255,0,0))
        w = self.camera_screen.get_width()*(globals.screen_width/self.camera_boundaries.width)
        h = self.camera_screen.get_height()*(globals.screen_height/self.camera_boundaries.height)
        self.camera_test = pygame.transform.scale(self.camera_screen, (int(w),int(h)))
        self.screen.blit(self.camera_test, (-self.camera_loc[0]*self.camera_zoom, -self.camera_loc[1]*self.camera_zoom))


        #info displayed
        sentence_speed = "x"+str(globals.time_speed)+" : "+str(int(self.clock.get_fps()))+" FPS"
        time_surface = self.my_font.render(sentence_speed, False, (0, 0, 0))
        sentence_cells_alive = "no. of cells alive : "+str(len(self.pool_cell))
        alive_surface = self.my_font.render(sentence_cells_alive, False, (0, 0, 0))
        self.screen.blit(time_surface, (5,0))
        self.screen.blit(alive_surface, (5,20))

        pygame.display.flip()

        pygame.display.update()

    def on_cleanup(self):
        """before quitting"""
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
 
