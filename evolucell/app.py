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
from .camera import Camera

def clear_surface(surface):
        surface.fill([0,0,0,0])

class App:
    def __init__(self):
        #main features of the App class
        self._running = True
        self.screen = None
        self.size = globals.screen_width, globals.screen_height
        self.clock = pygame.time.Clock()
        #self.pool_test = np.array([])
        #self.quadtree_test = np.array([])
        self.timer_food = 0
        self.wait_for_food = 0
        self.camera = Camera()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()   

    def on_init(self):
        """called only once, at the start of the program"""
        self.init_pygame_features()
        self.init_screens()
        self.create_quadtree_food()
        self.create_pool_cell()
        #display everything on screen
        self.on_render()
        pygame.display.flip()    
        self._running = True

    def init_pygame_features(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 15)
        pygame.key.set_repeat(150,50)
        self.clock = pygame.time.Clock()

    def init_screens(self):
        """create every screen needed"""
        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(color.background) 
        #debug screen
        self.debug_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.debug_screen.convert_alpha()
        #food screen
        self.food_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.food_screen.convert_alpha()
        #cell_screen
        self.cell_screen = pygame.surface.Surface((globals.playground_width,globals.playground_height), pygame.SRCALPHA, 32)
        self.cell_screen.convert_alpha()

    def create_quadtree_food(self):
        """fullfill the first quadtree with food particles"""
        #first quadtree
        boundary = Rectangle(0,0, globals.playground_width, globals.playground_height, color.boudaries_quadtree)
        self.quadtree = Quadtree(2, boundary)
        #launching food
        for i in range(globals.initial_qtt_of_food):
            self.quadtree.insert(Food(size=1))
        #food1 = Food(1900,1100)
        #food1.shift_color((255,-255,-255))
        #self.quadtree.insert(food1)

    def create_pool_cell(self):
        """launching cell"""
        self.pool_cell = np.array([])
        cell1 = Cell(500,300)
        self.pool_cell = np.append(self.pool_cell, cell1)

    def on_event(self, event):
        """process every user action"""
        self.event_quit(event)
        self.event_click(event)
        self.event_keys(event)   

    def event_quit(self, event):
        """if it's requested, quit the app and return True"""
        if event.type == pygame.QUIT:
            self._running = False
            return True
        return False
        
    def event_click(self, event):
        """if the user clicked somewhere on the screen, add cell and return True"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            keys  = pygame.key.get_pressed()
            local_coordinates = pygame.mouse.get_pos()
            x,y = self.camera.get_relative_coordinates(local_coordinates)
            if keys[pygame.K_q]:
                print(x, y)
            else :
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] :
                    new_food = Food(x,y,1)
                    new_food.shift_color((255,-255,-255))
                    self.quadtree.insert(new_food)
                else :
                    cell = Cell(x,y)
                    self.pool_cell = np.append(self.pool_cell, cell)
            return True
        return False
    
    def event_keys(self, event) :
        """if a valid key is pressed return True"""
        if event.type == pygame.KEYDOWN:
            keys  = pygame.key.get_pressed()
            if self.event_camera(keys):
                print(self.camera.zoom)
                print(self.camera.loc, self.camera.boundaries.width, self.camera.boundaries.height)
            elif self.event_ctrl_cell(keys):
                pass
            elif self.event_speed(keys):
                pass
            elif self.event_erase_all(keys):
                pass
            else :
                return False
            return True
        return False

    def event_camera(self, keys):
        """if user pressed zqsd keys, move (or zoom if shift is also pressed) and return True"""
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] :
                step = 0
                if keys[pygame.K_DOWN]:
                    step = 120
                elif keys[pygame.K_UP]:
                    step = -120
                self.camera.zoom(step)
            else :
                (x,y) = (0,0)
                step = 10
                if keys[pygame.K_UP]:
                    y += step
                elif keys[pygame.K_DOWN]:
                    y -= step
                if keys[pygame.K_LEFT]:
                    x -= step
                elif keys[pygame.K_RIGHT]:
                    x += step
                self.camera.move((x,y))
            return True
        return False

    def zoom_camera(self, keys):
        step = 120
        if keys[pygame.K_DOWN]:
            self.camera.zoom(step)
        elif keys[pygame.K_UP]:
            self.camera.zoom(-step)

    
    def move_camera(self, keys):
        step = 10
        if keys[pygame.K_UP]:
            self.camera.move((0,step))
        elif keys[pygame.K_DOWN]:
            self.camera.move((0,-step))
        if keys[pygame.K_LEFT]:
            self.camera.move((-step,0))
        elif keys[pygame.K_RIGHT]:
            self.camera.move((step,0))

    def event_ctrl_cell(self, keys):
        """control first cell with zqsd keys and return True, if it's impossible return False"""
        if keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d]:
            if len(self.pool_cell) != 0 :
                if keys[pygame.K_z]:
                    self.pool_cell[0].move_forward()
                if keys[pygame.K_s]:
                    self.pool_cell[0].move_backward()
                if keys[pygame.K_q]:
                    self.pool_cell[0].turn_left()
                if keys[pygame.K_d]:
                    self.pool_cell[0].turn_right()
                return True
        return False

    def event_speed(self, keys):
        """if user pressed p or m, increase or decrease speed and return True"""
        if keys[pygame.K_p]:
            globals.increase_speed()
            if len(self.pool_cell) != 0 :
                for cell in self.pool_cell:
                    cell.update_speed()
            return True
        elif keys[pygame.K_m]:
            globals.decrease_speed()
            if len(self.pool_cell) != 0 :
                for cell in self.pool_cell:
                    cell.update_speed()
            return True
        return False

    def event_erase_all(self, keys):
        """delete every food displayed on the screen and return true"""
        if keys[pygame.K_SPACE]:
            for food in self.quadtree.particles:
                self.quadtree.delete(food)
            self.quadtree.particles = np.array([])
            return True
        return False

    def on_loop(self):
        #tick every frame
        self.clock.tick(globals.fps)
        clear_surface(self.debug_screen)
        self.cell_handler()   
        self.food_handler()
        #self.quadtree_test = get_quadtrees_from_a_sprite(self.pool_cell[0], self.quadtree, get_maximal_depth(self.pool_cell[0]))
        pygame.display.flip()


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

    def on_render(self):
        """manage the screen display"""
        #erase main screen
        self.screen.fill(color.background) 
        # self.display_test()     
        self.display_food()
        self.display_cell()
        self.merge_screens()
        self.display_info()
        pygame.display.flip()
        pygame.display.update()
    
    def display_quadtrees(self):
        """print quadtrees on the screen"""
        clear_surface(self.debug_screen)
        self.quadtree.show(self.debug_screen)
        for qt in self.quadtree_test :
            qt.show(self.debug_screen, (255,0,0))

    def display_test(self):
        """print tests on the debug_screen"""
        for test in self.pool_test:
            test.shift_color((-255,-255,+255))
            if self.camera.contains_particle(test.pos) :
                self.debug_screen.blit(test.img, test)

    def display_food(self):
        """print food particles on the food_screen"""
        clear_surface(self.food_screen)
        for food in self.quadtree.particles:
            qt_final = self.quadtree.get_last_quadtree_from_pos(food.pos)
            if not contain(food.pos, qt_final.particles) :
                print("ERROR : unknown")
                self.quadtree.delete(food)
                food.shift_color((255,-255,-255))
            if self.camera.contains_particle(food.pos) :
                self.food_screen.blit(food.img, food)

    def display_cell(self):
        """print cells on the cell_screen"""
        clear_surface(self.cell_screen)
        for cell in self.pool_cell:
            if self.camera.contains_particle((cell.posx,cell.posy)) :
                self.cell_screen.blit(cell.img, cell)

    def merge_screens(self):
        """copy every screen into the main screen"""
        list_screens = [(self.cell_screen, (0,0)),(self.food_screen, (0,0)),(self.debug_screen, (0,0))]
        output_screen, output_pos = self.camera.render(list_screens)
        self.screen.blit(output_screen, output_pos)

    def display_info(self):
        """display useful data"""
        sentence_speed = "x"+str(globals.time_speed)+" : "+str(int(self.clock.get_fps()))+" FPS"
        time_surface = self.my_font.render(sentence_speed, False, (0, 0, 0))
        sentence_cells_alive = "no. of cells alive : "+str(len(self.pool_cell))
        alive_surface = self.my_font.render(sentence_cells_alive, False, (0, 0, 0))
        self.screen.blit(time_surface, (5,0))
        self.screen.blit(alive_surface, (5,20))

    def on_cleanup(self):
        """before quitting"""
        pygame.quit()
 
    
 
