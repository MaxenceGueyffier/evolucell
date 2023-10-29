import pygame
from pygame.math import Vector2
from rectangle import *
import numpy as np


class Quadtree:
    '''
    A Quadtree is an object wich can subdivided into 4 parts, each Quadtree can contains a specific number of particles\n
    capcity: nbr of particles allowed into one Quadtree
    boundary: Rectangle in which the Quadtree is about to be created
    subdivision: nbr of times the Quadtree was split
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
                parent.width/2,
                parent.height/2
            )
        boundary_ne = Rectangle(
                parent.x + parent.width/2,
                parent.y,
                parent.width/2,
                parent.height/2
            )
        boundary_sw = Rectangle(
                parent.x,
                parent.y + parent.height/2,
                parent.width/2,
                parent.height/2
            )
        boundary_se = Rectangle(
                parent.x + parent.width/2,
                parent.y + parent.height/2,
                parent.width/2,
                parent.height/2
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
    def show(self, screen):
        self.boundary.Draw(screen)
        if self.northWest != None:
            self.northWest.show(screen)
            self.northEast.show(screen)
            self.southWest.show(screen)
            self.southEast.show(screen)