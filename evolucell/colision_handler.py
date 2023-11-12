import numpy as np
import pygame

from .sprite import Sprite
from .quadtree import Quadtree, contain
from .common import globals as globals

def get_maximal_depth(sprite) :
    w = globals.SCREEN_WIDTH
    h = globals.SCREEN_HEIGHT
    depth = -1
    while sprite.width < w and sprite.height < h :
        w /= 2
        h /= 2
        depth += 1
    return depth

def get_quadtrees_from_a_sprite (sprite, quadtree, depth = 4):
    """
    from a specific sprite, get each minimum quadtree where it is located.\n
    sprite : can be any sprite
    quadtree : the first Quadtree where to look for
    depth : maximal subdivision of the initial Quadtree.
    """
    x = sprite.posx - sprite.width/2
    y = sprite.posy - sprite.height/2
    w = sprite.posx + sprite.width/2
    h = sprite.posy + sprite.height/2
    quadtree_array = np.array([])
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((x,y),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((w,y),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((x,h),depth))
    quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((w,h),depth))
    return quadtree_array

def is_colision(object1, type_object2, quadtree, screen=None):
    mask1 = pygame.mask.from_surface(object1.img)       
    list_colision = np.array([])
    quadtree_array = get_quadtrees_from_a_sprite(object1, quadtree, get_maximal_depth(object1))

    for qt in quadtree_array:
        for [posx, posy] in qt.particles:
            object2 = type_object2(int(posx), int(posy))
            mask2 = pygame.mask.from_surface(object2.img)
            if mask1.overlap(mask2, (object2.rect.x-object1.rect.x, object2.rect.y-object1.rect.y)) != None:
                if screen != None :
                    screen.blit(mask2.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), object2)
                list_colision = np.reshape(list_colision, (-1, 2))
                
                if not contain(object2.pos, list_colision):
                    list_colision = np.append(list_colision, object2.pos)
    return list_colision


