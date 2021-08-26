COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_GROUND = (50, 50, 150)


#change col and row to x and y
#prot over to pygame 


from random import random
from random import randrange
from random import choice

class DungeonSqr:
    def __init__(self, tile):
        self.tile = tile

    def get_colheight(self):
        return self.tile

class Room:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width

class Corridor:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width

class DungeonGenerator:
    def __init__(self, width, height):
        self.MAX = 25 # Cutoff for when we want to stop splitting the tree
        self.width = width
        self.height = height
        self.leaves = [] #creating a list for each so we can split and add
        self.splits = []
        self.dungeon = []
        self.rooms = []
        self.corridors = []

        for height in range(self.height):
            row = []
            for width in range(self.width):
                row.append(DungeonSqr('#'))
                
                #filling out the dungeon with #'s

            self.dungeon.append(row)
        
    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        #using the choice module from random allows ease of code writing no need for large array and item selection code
        #choice provieds the random split it is the wild card
        split = (min_row + max_row) // 2 + round(randrange(-30, 30) / 100 * (max_row - min_row))
        self.random_split(min_row, min_col, split, max_col)
        #split in the rows
        self.random_split(split + 1, min_col, max_row, max_col)
        return (split, min_col + (max_col - min_col)//2)
        

    def split_on_vertical(self, min_row, min_col, max_row, max_col):        
        split = (min_col + max_col) // 2 + round(randrange(-30, 30) / 100 * (max_col - min_col))
        self.random_split(min_row, min_col, max_row, split)
         #split in the cols
        self.random_split(min_row, split + 1 , max_row, max_col)
        return (min_row + (max_row - min_row)//2, split)
    

    def random_split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold set in self.MAX
        seg_height = max_row - min_row 
        seg_width = max_col - min_col

        split = None
        # boolean true for vertical and false for horizontal this is for use when making the corridor connections
        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col)) #adding a new leaf
            
        elif seg_height < self.MAX and seg_width >= self.MAX:
            split = (True, self.split_on_vertical(min_row, min_col, max_row, max_col))
            
        elif seg_height >= self.MAX and seg_width < self.MAX:
            split = (False, self.split_on_horizontal(min_row, min_col, max_row, max_col))
            
            #depending on the value of max-row - min_row you can either get a vertical or horizontal row almost a 50/50 chance
        else:
            if random() < 0.5:
                split = (False, self.split_on_horizontal(min_row, min_col, max_row, max_col))
            else:
                split = (True, self.split_on_vertical(min_row, min_col, max_row, max_col))
        
        if split:
            self.splits.append(split)
        #at the end of the random split you are left with the self.MAX number of leaves in the self.leaves list
          
    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the  dungeon looks too uniform
            #if random() > 0.90: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-90% of the 
            # available section.
            room_width = round(randrange(40, 90) / 100 * section_width)
            room_height = round(randrange(40, 90) / 100 * section_height)
            room_start_row = leaf[0] + round(randrange(0, 100) / 100 * (section_height - room_height))
            room_start_col = leaf[1] + round(randrange(0, 100) / 100 * (section_width - room_width))
    
            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            
            for row in range(room_start_row, room_start_row + room_height):
                for col in range(room_start_col, room_start_col + room_width):
                    self.dungeon[row][col] = DungeonSqr('.')
    
    def carve_corridors(self):
        for (is_vert_split, (row, col)) in self.splits:
            
            obj=None
            if is_vert_split:
                start = col
                # find where it hits non-empty
                for i in range(col, 0, -1):
                    if self.dungeon[row][i].tile == '#':
                        start = i
                    else:
                        break
                
                end = None
                for i in range(col, self.width):
                    if self.dungeon[row][i].tile == '#':
                        end = i
                    else:
                        break
                if start and end:
                    obj = Corridor(row, start, 1, end-start+1)
                    self.corridors.append(obj)
            else:
                # horizontal split ,so vertical corridor
                start = row
                # find where it hits non-empty
                for i in range(row, 0, -1):
                    if self.dungeon[i][col].tile == '#':
                        start = i
                    else:
                        break
                
                end = None
                for i in range(row, self.height):
                    if self.dungeon[i][col].tile == '#':
                        end = i
                    else:
                        break
                if start and end:
                    obj = Corridor(start, col, end-start+1, 1)
                    self.corridors.append(obj)
            
            if obj:
                for row in range(obj.row, obj.row + obj.height):
                    for col in range(obj.col, obj.col + obj.width):
                        self.dungeon[row][col] = DungeonSqr('c')

    def generate_map(self):
        self.random_split(1, 1, self.height - 5, self.width - 5)
        # - 1 from the height and the width to allow for full boarder walls
        self.carve_rooms()
        self.carve_corridors()

    def print_map(self):
        for r in range(self.height):
            row = ''
            for c in range(self.width):
                row += self.dungeon[r][c].get_colheight() #either adding in a # = wall or a | = floor space
            print(row)



    
    







 



