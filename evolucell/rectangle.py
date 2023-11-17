import pygame


class Rectangle:
    """
    Rectangle(x, y, width, height, color=(0,0,0), line_thickness=1)\n
    Rectangle are used as boundaries by a Quadtree\n
    x,y are the coordinates of the upper left corner of the rectangle
    """
    def __init__(self, x:int, y:int, width:int, height:int, color=(0,0,0), line_thickness=1):
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.color = color
        self.line_thickness = line_thickness

    def containsParticle(self, coordinate):
        """if a coordinate is located inside the boundaries of the rectangle return True, otherwise return False"""   
        (x_particle, y_particle) = coordinate
        if x_particle >= self.posx and x_particle < self.posx+self.width and y_particle >= self.posy and y_particle < self.posy+self.height:
            return True
        else:
            return False
        
    def is_overlapping(self, _other):
        x1,y1 = _other.posx, _other.posy
        x2,y2 = _other.posx+_other.width, _other.posy
        x3,y3 = _other.posx+_other.width, _other.posy+_other.height
        x4,y4 = _other.posx, _other.posy+_other.height
        for (x,y) in [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]:
            if self.containsParticle((x,y)):
                return True
        return False

    def draw(self, screen, color=(0,0,0)):
        """dislpay the rect on the screen"""
        self.color = color
        pygame.draw.rect(screen, self.color, [self.posx, self.posy, self.width, self.height], self.line_thickness)
        