import pygame
from rectangle import *
import numpy as np

def contained(nptup,nparray):
    """check if the exact particule (or a slightly different) is already in the quadtree"""
    _set = set((x,y) for [x,y] in nparray)
    (x,y) = nptup
    for i in range(-1,2):
        for j in range(-1,2):
            if (x+i,y+j) in _set :
                return True
    return False

class Quadtree:
    '''
    A Quadtree is an object wich can subdivided into 4 parts, each Quadtree can contains a specific number of particles\n
    capcity: nbr of particles allowed into one Quadtree
    boundary: Rectangle in which the Quadtree is about to be created
    subdivision: nbr of times the Quadtree was split, usually starts at 0
    '''
    out_of_capacity = False
    
    def __init__(self, capacity: int, boundary: Rectangle , subdivision: int = 0):
        self.capacity = capacity
        self.boundary = boundary
        self.particles = np.array([])
        self.subdivision = subdivision

        self.northWest: Quadtree = None
        self.northEast: Quadtree = None
        self.southWest: Quadtree = None
        self.southEast: Quadtree = None

    def subdivide(self):
        """divide the Quadtree into 4 sub-Quadtree and assignated each particle to the correct sub-Quadtree"""
        
        # create 4 Rectangles
        parent = self.boundary
        boundary_nw = Rectangle(
                parent.x,
                parent.y,
                int(parent.width/2),
                int(parent.height/2)
            )
        boundary_ne = Rectangle(
                parent.x + int(parent.width/2),
                parent.y,
                parent.width - int(parent.width/2),
                int(parent.height/2)
            )
        boundary_sw = Rectangle(
                parent.x,
                parent.y + int(parent.height/2),
                int(parent.width/2),
                parent.height - int(parent.height/2)
            )
        boundary_se = Rectangle(
                parent.x + int(parent.width/2),
                parent.y + int(parent.height/2),
                parent.width - int(parent.width/2),
                parent.height - int(parent.height/2)
            )
        
        #Each Rectangle is assignated to the correct sub-Quadtree
        self.northWest = Quadtree(self.capacity, boundary_nw, self.subdivision+1)
        self.northEast = Quadtree(self.capacity, boundary_ne, self.subdivision+1)
        self.southWest = Quadtree(self.capacity, boundary_sw, self.subdivision+1)
        self.southEast = Quadtree(self.capacity, boundary_se, self.subdivision+1)

        #add the particles to the correct sub-Quadtree
        for i in range(len(self.particles)):
            self.northWest.insert(self.particles[i])
            self.northEast.insert(self.particles[i])
            self.southWest.insert(self.particles[i])
            self.southEast.insert(self.particles[i])

    def insert(self, particle):
        """add a particle (which is a tuple of coordinate) to this Quadtree"""

        #check this particle doesn't already exist or even a slightly different 
        #because it could create an infinte loop while trying to split the quadtree into smaller and smaller sub_quadtree 
        if(self.subdivision == 0):
            if len(self.particles)!=0 :
                if contained (particle, self.particles):
                    print("ERROR : you try to add a praticle already")
                    return False

        #check if you're in the right Quadtree
        if self.boundary.containsParticle(particle) == False:
            return False
        else :
            #add particle to the list of particles with the right format
            self.particles = np.append(self.particles, (particle))
            self.particles = np.reshape(self.particles, (-1, 2))

        

        #if the Quadtree is not out of capacity yet
        if len(self.particles) <= self.capacity:
            return True
        else:
            #if it's the first time the Quadtree is out of capacity, then subdivide it
            if self.out_of_capacity == False :
                self.out_of_capacity = True
                self.subdivide()
                return True
            #otherwise, add the particle to the correct sub-Quadtree
            else:
                if self.northWest.insert(particle):
                    return True
                if self.northEast.insert(particle):
                    return True
                if self.southWest.insert(particle):
                    return True
                if self.southEast.insert(particle):
                    return True
            return False

    #reveal each Quadtree
    def show(self, screen, color=(0,0,0)):
        if self.northWest != None:
            self.northWest.show(screen, color)
            self.northEast.show(screen, color)
            self.southWest.show(screen, color)
            self.southEast.show(screen, color)
        else :
            self.boundary.Draw(screen, color)


    """
    get the last quadtree to which the particle would have been assigned
    depth_max : only allows Quadtree with a maximal level of subdivision, a negative value means no maximal depth 
    """
    def get_last_quadtree(self, particle, depth_max:int = -1):
        if (depth_max>=0 and self.subdivision!=depth_max) or depth_max<0 :
            if self.northWest != None :
                if self.northWest.boundary.containsParticle(particle):
                    return self.northWest.get_last_quadtree(particle,depth_max)
                elif self.northEast.boundary.containsParticle(particle):
                    return self.northEast.get_last_quadtree(particle, depth_max)
                elif self.southWest.boundary.containsParticle(particle):
                    return self.southWest.get_last_quadtree(particle, depth_max)
                else:
                    return self.southEast.get_last_quadtree(particle, depth_max)
            else:
                return self
        else : 
            return self