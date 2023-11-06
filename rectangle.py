import pygame


class Rectangle:
    """
    Rectangle(x, y, width, height, color=(0,0,0), line_thickness=1)\n
    Rectangle used as boundaries by a Quadtree\n
    x,y are the coordinates of the upper left corner of the rectangle
    """
    def __init__(self, x:int, y:int, width:int, height:int, color=(0,0,0), line_thickness=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.line_thickness = line_thickness

    def containsParticle(self, particle):
        """if the particle (which is a tuple) is inside the boundaries of the rectangle"""   
        (x_particle, y_particle) = particle
        if x_particle >= self.x and x_particle <= self.x+self.width and y_particle >= self.y and y_particle <= self.y+self.height:
            return True
        else:
            return False

    def Draw(self, screen, color=(0,0,0)):
        """dislpay the rect on the screen"""
        self.color = color
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], self.line_thickness)
        