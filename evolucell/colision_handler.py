import numpy as np
import pygame

from .sprite import Sprite
from .quadtree import Quadtree, contain
from .common import globals as globals

def get_maximal_depth(sprite: Sprite) :
    w = globals.playground_width
    h = globals.playground_height
    depth = -1
    while sprite.width < w and sprite.height < h :
        w /= 2
        h /= 2
        depth += 1
    return depth

def get_quadtrees_from_a_sprite (sprite: Sprite, quadtree: Quadtree, depth = 4):
    """
    From a specific sprite, get each quadtree where it could be located.
    The sprite has a volume, so it could fit in several quadtrees.\n
    sprite : can be any sprite
    quadtree : the first Quadtree where to look for
    depth : maximal subdivision of the initial Quadtree.\n
    Return a list of Quadtrees
    """
    x = sprite.posx - sprite.width/2
    y = sprite.posy - sprite.height/2
    w = sprite.posx + sprite.width/2
    h = sprite.posy + sprite.height/2
    quadtree_array = np.array([])
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree_from_pos((x,y),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree_from_pos((w,y),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree_from_pos((x,h),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree_from_pos((w,h),depth))
    return quadtree_array

def list_colision(_object:Sprite, quadtree: Quadtree, screen=None):
    """Finds which particles in the quadtree are colliding with the _object (which is also a Sprite)\n
    Return a list of particle.\n
    Warning : it only works if the quadtree contains Sprites as particles."""
    mask1 = pygame.mask.from_surface(_object.img)       
    list_colision = np.array([])
    quadtree_array = get_quadtrees_from_a_sprite(_object, quadtree, get_maximal_depth(_object))

    for qt in quadtree_array:
        for particle in qt.particles:
            mask2 = pygame.mask.from_surface(particle.img)
            if mask1.overlap(mask2, (particle.rect.x-_object.rect.x, particle.rect.y-_object.rect.y)) != None:
                if screen != None :
                    screen.blit(mask2.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), particle)
                
                if not contain(particle.pos, list_colision):
                    list_colision = np.append(list_colision, particle)
    return list_colision



