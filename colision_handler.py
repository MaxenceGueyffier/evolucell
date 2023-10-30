from sprite import Sprite
from quadtree import Quadtree
import numpy as np
from data.default import *

def get_maximal_depth(sprite) :
    w = SCREEN_WIDTH
    h = SCREEN_HEIGHT
    depth = -1
    while sprite.width < w and sprite.height < h :
        w /= 2
        h /= 2
        depth += 1
    return depth

def get_quadtrees_from_a_sprite (sprite: Sprite, quadtree:Quadtree, depth:int = 4):
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