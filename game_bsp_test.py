import random
import pygame
import sys
from random import randrange
from random import choice


WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255, 0, 0)
LIGHT_RED = (255, 127, 127)
WALL_IMAGE= pygame.image.load("stonebrick.png")

# core attributes
width = 40
height = 40
speed = 5
numcols = 25
numrows = 20

#black screen
screen_size = (width * (numcols), height * numrows)

screen = pygame.display.set_mode(screen_size)

#screen refresh rate
clock = pygame.time.Clock()


 
    
class Wall(pygame.sprite.Sprite):
    def __init__(self,width,height,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("stonebrick.png").convert(),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Floor(pygame.sprite.Sprite):
    def __init__(self,width,heigh,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("floor.png").convert(),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                
class Player(pygame.sprite.Sprite): 
    def __init__(self,colour,width,height,speed,wall_group):
        super().__init__()
        
        #set player dimentions
        self.wall_group = wall_group
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface([width,height])
        self.image.fill(colour)
        
        #set position of player need to make it so the player starts in a spot with no wall
        self.rect = self.image.get_rect()
        
        fini = False
        i = 0
        while not fini and r < len(dungeon.dungeon):
            c = 0
            while not fini and c < len(dungeon.dungeon[r]):
                if (dungeon.dungeon[r][c]) == 0:
                    self.rect.x,self.rect.y  = (r)*width,(c)*height
                    fini = True
                j += 1     #same as j = j + 1
            i += 1
        self.old_x =  self.rect.x
        self.old_y = self.rect.y
        
    def update(self):
        
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y
        
        wall_hit_list = pygame.sprite.spritecollide(self, self.wall_group, False)
        for x in wall_hit_list:
            self.rect.x =  self.old_x 
            self.rect.y =  self.old_y 
            self.speed_x = 0
            self.speed_y = 0

        self.old_y = self.rect.y 
        self.old_x = self.rect.x 
            
    def player_set_speed(self,x,y):
        self.speed_x = x
        self.speed_y = y
        



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
        
class DungeonSqr:
    def __init__(self, tile):
        self.tile = tile

    def get_colheight(self):
        return self.tile

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
            if random.randint(0, 9) < 5:
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
        self.random_split(1, 1, self.height - 1, self.width - 1)
        # - 1 from the height and the width to allow for full boarder walls
        self.carve_rooms()
        self.carve_corridors()
    
    def generate_pygame_map(self,floor_group,wall_group,all_sprite_group):        
        v = None
        for r in range(self.height):
            for c in range(self.width):
                self.dungeon[r][c]= v
                
                if v == "#":
                    my_wall = Wall(WHITE,width,height,i*width,j*height)
                    all_sprite_group.add(my_wall)
                    wall_group.add(my_wall)
                elif v == ".":
                    my_floor = Floor(width,height,i*width,j*height)
                    all_sprite_group.add(my_floor)
                    floor_group.add(my_floor)
                    #end if
            #next column 
        #next row
                               
def main_loop():
    all_sprite_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    dungeon = DungeonGenerator(width * (numcols), height * numrows)
    dungeon.generate_map()
    dungeon.generate_pygame_map(floor_group,wall_group,all_sprite_group)
    
    
    #exit game falg set to false
    done = False
    while not done:
        #user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
             
        
        #update all sprites    
        all_sprite_group.update()
        #screen background is black
        screen.fill(BLACK)
        #draw function
        all_sprite_group.draw(screen)
        #flip display to show new position of objects
        
        
        
        pygame.display.flip()
        clock.tick(240)
#end game loop
# end function

pygame.init()
main_loop()
pygame.quit()