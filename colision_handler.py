from sprite import Sprite
from quadtree import Quadtree
import numpy as np

def get_quadtrees_from_a_sprite (sprite: Sprite, quadtree:Quadtree):
        """
        for a specific sprite, get each minimum quadtree where it is located
        """
        x = sprite.posx - sprite.width/2
        y = sprite.posy - sprite.height/2
        w = sprite.posx + sprite.width/2
        h = sprite.posy + sprite.height/2

        depth = 4
        quadtree_array = np.array([])
        quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((x,y),depth))
        quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((w,y),depth))
        quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((x,h),depth))
        quadtree_array = np.append(quadtree_array, quadtree.get_last_quadtree((w,h),depth))

        return quadtree_array