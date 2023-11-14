import pygame
import numpy as np
from functools import total_ordering

from .rectangle import *

def contain(coordinate,particles):
    """
    check if there is an object in particles located at coordinate.\n
    return True if there is one and False otherwise
    """
    
    _set = set(particle.pos for particle in particles)
    (x,y) = coordinate
    if (x,y) in _set :
        return True
    else:
        return False

@total_ordering
class Quadtree:
    '''
    A Quadtree is an object wich can subdivided into 4 parts, each Quadtree can contains a specific number of particles.
    A particle could be any object with an attribute pos (a tuple coordinate).\n
    capcity: nbr of particles allowed into one Quadtree
    boundary: Rectangle in which the Quadtree is about to be created
    subdivision: nbr of times the Quadtree was split, usually starts at 0
    '''
    out_of_capacity = False
    
    def __init__(self, capacity, boundary: Rectangle, subdivision: int = 0):
        self.capacity = capacity
        self.boundary = boundary
        self.particles = np.array([])
        self.subdivision = subdivision

        self.northWest: Quadtree = None
        self.northEast: Quadtree = None
        self.southWest: Quadtree = None
        self.southEast: Quadtree = None

    #add comparison
    def __lt__(self, other):
        """indicate if this_quadtree < other_quadtre"""
        return len(self.particles) < len(other.particles)
    def __gt__(self, other):
        """indicate if this_quadtree > other_quadtre"""
        return len(self.particles) > len(other.particles)

    def subdivide(self):
        """Divide the Quadtree into 4 sub-Quadtree and assignate each one its own particles to the correct sub-Quadtree."""     
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
        """add a particle to this Quadtree. Return True if it worked and False otherwise"""
        #if this particle already exists, delete it
        if(self.subdivision == 0):
            if len(self.particles)!=0 :
                if contain(particle.pos, self.particles):
                    print("particle already there")
                    #job has failed
                    return False
                
        #check if you're in the right Quadtree
        if self.boundary.containsParticle(particle.pos) == False:
            #job has failed
            return False
        
        #add particle to the list of particles
        self.particles = np.append(self.particles, (particle))

        #if the Quadtree is not out of capacity yet
        if len(self.particles) > self.capacity:
            #if it's the first time the Quadtree is out of capacity, then subdivide it
            #after 15 subdivision stop it in order to avoid infinte loop
            if self.subdivision <= 15 :
                if self.out_of_capacity == False:
                    self.out_of_capacity = True
                    self.subdivide()
                #otherwise, add the particle to the correct sub-Quadtree
                else:
                    for subqt in [self.northWest, self.northEast, self.southWest, self.southEast]:
                        subqt.insert(particle)
            else :
                self.delete(particle)
                print("ERROR : infinite subdivision")
                return False
        #job is done    
        return True

    def unify (self):
        """Remove every sub-Quadtree."""
        self.northWest = None
        self.northEast = None
        self.northWest = None
        self.northEast = None

    def delete(self, particle):
        """delete a particle from this Quadtree.\n
        Return True if it worked and False otherwise.""" 
        #for each particle       
        for i in range(len(self.particles)-1, -1, -1):
            #if its coordinates are the same as the one we need to delete
            if self.particles[i].pos==particle.pos:
                #delete it
                self.particles = np.delete(self.particles, i)
                #if the quadtree has a subdivision
                if self.northWest != None:
                    #for each subquadtree
                    for subqt in [self.northWest, self.northEast, self.southWest, self.southEast]:
                        #check if the subquadtree contains the particle
                        if subqt.boundary.containsParticle(particle.pos) :
                            #if the curent quadtre (not the subquadtree) has reached it limit 
                            if len(self.particles) <= self.capacity:
                                #delete all the subquadtrees
                                self.unify()
                                #initialize out_of_capacity
                                self.out_of_capacity = False
                            else:
                                #otherwise just call the function delete() in the subquadtree
                                subqt.delete(particle)
                            #job is done
                            return True
        #job has failed
        return False            
        
    def show(self, screen, color=(0,0,0)):
        """Reveal each Quadtree."""
        if self.northWest != None:
            self.northWest.show(screen, color)
            self.northEast.show(screen, color)
            self.southWest.show(screen, color)
            self.southEast.show(screen, color)
        else :
            self.boundary.Draw(screen, color)


    
    def get_last_quadtree_from_pos(self, pos, depth_max:int = -1):
        """Get the last quadtree to which a particle located at pos would have been assigned.\n
        pos : a tuple coordinate
        depth_max : only allows Quadtree with a maximal level of subdivision, a negative value means no maximal depth\n
        Return the last quadtree.
        """

        if (depth_max>=0 and self.subdivision!=depth_max) or depth_max<0 :
            if self.northWest != None :
                if self.northWest.boundary.containsParticle(pos):
                    return self.northWest.get_last_quadtree_from_pos(pos, depth_max)
                elif self.northEast.boundary.containsParticle(pos):
                    return self.northEast.get_last_quadtree_from_pos(pos, depth_max)
                elif self.southWest.boundary.containsParticle(pos):
                    return self.southWest.get_last_quadtree_from_pos(pos, depth_max)
                else:
                    return self.southEast.get_last_quadtree_from_pos(pos, depth_max)
            else:
                return self
        else : 
            return self