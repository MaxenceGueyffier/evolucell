import pygame
from pygame.locals import *
from data.color import Color
from cell import Cell
import time

 
class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1000, 600
        self.clock = pygame.time.Clock()
        self.pool = []
        self.color = Color()

 
    def on_init(self):
        #pygame features
        pygame.init()
        pygame.display.set_caption('Evolucell')
        pygame.key.set_repeat(160,50)

       

        #background
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(self.color.background)
        pygame.display.flip()

        #cell test
        cell1 = Cell(400,400)
        self.pool.append(cell1)

        self.screen.blit(self.pool[0].img, self.pool[0])

        

        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
    def on_loop(self):
        self.screen.fill(self.color.background) 

        self.pool[0].move_forward()
        self.pool[0].turn_right()

        print(f"direction : {self.pool[0].direction}")
        print(f"location : {(self.pool[0].posx, self.pool[0].posy)}")
        self.screen.blit(self.pool[0].img, self.pool[0])
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