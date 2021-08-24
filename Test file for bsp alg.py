COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_GROUND = (50, 50, 150)

from math import sqrt
from random import random
from random import randrange
from random import choice

class DungeonSqr:
    def __init__(self, sqr):
        self.sqr = sqr

    def get_ch(self):
        return self.sqr

class Room:
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w
        
class DungeonGenerator:
    def __init__(self, w, h):
        self.MAX = 1000 # Cutoff for when we want to stop splitting the tree
        self.width = w
        self.height = h
        self.leaves = [] #creating a list for each so we can split and add
        self.dungeon = []
        self.rooms = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(DungeonSqr('#'))
                
                #filling out the dungeon with #'s

            self.dungeon.append(row)


    def random_split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold set in self.MAX
        seg_height = max_row - min_row 
        seg_width = max_col - min_col

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col)) #adding a new leaf
            
        elif seg_height < self.MAX and seg_width >= self.MAX:
            self.split_on_vertical(min_row, min_col, max_row, max_col)
            
        elif seg_height >= self.MAX and seg_width < self.MAX:
            self.split_on_horizontal(min_row, min_col, max_row, max_col)
            
            #depending on the value of max-row - min_row you can either get a vertical or horizontal row almost a 50/50 chance
       








 



