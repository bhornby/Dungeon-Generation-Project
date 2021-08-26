COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_GROUND = (50, 50, 150)


#change col and row to x and y
#prot over to pygame 

#row = y
#col = x

from random import random
from random import randrange
from random import choice

class DungeonSqr:
    def __init__(self, tile):
        self.tile = tile

    def get_colheight(self):
        return self.tile

class Room:
    def __init__(self, row, col,y , x):
        self.row = row
        self.col = col
        self.y = y
        self.x = x

class Corridor:
    def __init__(self, row, col, y, x):
        self.row = row
        self.col = col
        self.y = y
        self.x = x

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

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(DungeonSqr('#'))
                
                #filling out the dungeon with #'s

            self.dungeon.append(row)
        
    def split_on_horizontal(self, min_y, min_x, max_y, max_x):
        #using the choice module from random allows ease of code writing no need for large array and item selection code
        #choice provieds the random split it is the wild card
        split = (min_y + max_y) // 2 + round(randrange(-30, 30) / 100 * (max_y - min_y))
        self.random_split(min_y, min_x, split, max_x)
        #split in the rows
        self.random_split(split + 1, min_x, max_y, max_x)
        return (split, min_x + (max_x - min_x)//2)
        

    def split_on_vertical(self, min_y, min_x, max_y, max_x):        
        split = (min_x + max_x) // 2 + round(randrange(-30, 30) / 100 * (max_x - min_x))
        self.random_split(min_y, min_x, max_y, split)
         #split in the cols
        self.random_split(min_y, split + 1 , max_y, max_x)
        return (min_y + (max_y - min_y)//2, split)
    

    def random_split(self, min_y, min_x, max_y, max_x):
        # We want to keep splitting until the sections get down to the threshold set in self.MAX
        seg_height = max_y - min_y 
        seg_width = max_x - min_x

        split = None
        # boolean true for vertical and false for horizontal this is for use when making the corridor connections
        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_y, min_x, max_y, max_x)) #adding a new leaf
            
        elif seg_height < self.MAX and seg_width >= self.MAX:
            split = (True, self.split_on_vertical(min_y, min_x, max_y, max_x))
            
        elif seg_height >= self.MAX and seg_width < self.MAX:
            split = (False, self.split_on_horizontal(min_y, min_x, max_y, max_x))
            
            #depending on the value of max-row - min_y you can either get a vertical or horizontal row almost a 50/50 chance
        else:
            if random() < 0.5:
                split = (False, self.split_on_horizontal(min_y, min_x, max_y, max_x))
            else:
                split = (True, self.split_on_vertical(min_y, min_x, max_y, max_x))
        
        if split:
            self.splits.append(split)
        #at the end of the random split you are left with the self.MAX number of leaves in the self.leaves list
          
    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the  dungeon looks too uniform
            #if random() > 0.90: continue
            section_x = leaf[3] - leaf[1]
            section_y = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-90% of the 
            # available section.
            room_x = round(randrange(40, 90) / 100 * section_x)
            room_y = round(randrange(40, 90) / 100 * section_y)
            room_start_y = leaf[0] + round(randrange(0, 100) / 100 * (section_y - room_y))
            room_start_x = leaf[1] + round(randrange(0, 100) / 100 * (section_x - room_x))
    
            self.rooms.append(Room(room_start_y, room_start_x, room_y, room_x))
            
            for y in range(room_start_y, room_start_y + room_y):
                for x in range(room_start_x, room_start_x + room_x):
                    self.dungeon[y][x] = DungeonSqr('.')
    
    def carve_corridors(self):
        for (is_vert_split, (y, x)) in self.splits:
            
            obj=None
            if is_vert_split:
                start = x
                # find where it hits non-empty
                for i in range(x, 0, -1):
                    if self.dungeon[y][i].tile == '#':
                        start = i
                    else:
                        break
                
                end = None
                for i in range(x, self.width):
                    if self.dungeon[y][i].tile == '#':
                        end = i
                    else:
                        break
                if start and end:
                    obj = Corridor(y, start, 1, end-start+1)
                    self.corridors.append(obj)
            else:
                # horizontal split ,so vertical corridor
                start = y
                # find where it hits non-empty
                for i in range(y, 0, -1):
                    if self.dungeon[i][x].tile == '#':
                        start = i
                    else:
                        break
                
                end = None
                for i in range(y, self.height):
                    if self.dungeon[i][x].tile == '#':
                        end = i
                    else:
                        break
                if start and end:
                    obj = Corridor(start, x, end-start+1, 1)
                    self.corridors.append(obj)
            
            if obj:
                for y in range(obj.row, obj.row + obj.y):
                    for x in range(obj.col, obj.col + obj.x):
                        self.dungeon[y][x] = DungeonSqr('c')

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



    
    







 



