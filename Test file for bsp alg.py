COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_GROUND = (50, 50, 150)

from math import sqrt
from random import random
from random import randrange
from random import choice

class DungeonSqr:
    def __init__(self, sqr):
        self.sqr = sqr

    def get_colheight(self):
        return self.sqr

class Room:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        
class DungeonGenerator:
    def __init__(self, width, height):
        self.MAX = 10 # Cutoff for when we want to stop splitting the tree
        self.width = width
        self.height = height
        self.leaves = [] #creating a list for each so we can split and add
        self.dungeon = []
        self.rooms = []

        for height in range(self.height):
            row = []
            for width in range(self.width):
                row.append(DungeonSqr('#'))
                
                #filling out the dungeon with #'s

            self.dungeon.append(row)
    
    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        #using the choice module from random allows ease of code writing no need for large array and item selection code
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    def split_on_vertical(self, min_row, min_col, max_row, max_col):        
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)
        #the plus ones allow for extra spacing in between rooms otherwise there will either be overlaps between rooms or the rooms will be too close together


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
        else:
            if random() < 0.5:
                self.split_on_horizontal(min_row, min_col, max_row, max_col)
                
            else:
                self.split_on_vertical(min_row, min_col, max_row, max_col)
        
        #at the end of the random split you are left with the self.MAX number of leaves in the self.leaves list
          
    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the  dungeon looks too uniform
            if random() > 0.80: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-100% of the 
            # available section. 
            room_width = round(randrange(60, 100) / 100 * section_width)
            room_height = round(randrange(60, 100) / 100 * section_height)
            room_start_row = leaf[0]
            room_start_col = leaf[1]
    
            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            for row in range(room_start_row, room_start_row + room_height):
                for col in range(room_start_col, room_start_col + room_width):
                    self.dungeon[row][col] = DungeonSqr('|')

    def generate_map(self):
        self.random_split(1, 1, self.height - 1, self.width - 1)
        self.carve_rooms()

    def print_map(self):
        for r in range(self.height):
            row = ''
            for c in range(self.width):
                row += self.dungeon[r][c].get_colheight()
            print(row)

dungeon = DungeonGenerator(75, 40)
dungeon.generate_map()
dungeon.print_map()

    
    







 



