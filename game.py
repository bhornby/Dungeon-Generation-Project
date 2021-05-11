import random
import pygame
from dataclasses import dataclass
from typing import List
from typing import Object

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
WALL_IMAGE= pygame.image.load("stonebrick.png")

# core attributes
width = 40
height = 40
speed = 5
numcols = 25
numrows = 20

#black screen
size = (numcols * width, numrows * height)

screen = pygame.display.set_mode(size)

#exit game falg set to false
done = False

#screen refresh rate
clock = pygame.time.Clock()

@dataclass
class Node:
    parent: Object[Node] #cant be defaulted
    width: int
    height: int
    children: List[Node] = []
    room: Object[Room] = None
    
#     def __init__(self,width,height):
#         super().__init__()
#         self.width = width
#         self.height = height
    
      
@dataclass
class Tree:
    root: Object[Node]
    leaves: List[Node]
    margin: int
    
    def __init__(self,width,height,margin):
        super().__init__()
        #root will equal a node with this width and height
        self.root = Node(None, width, height)
        self.leaves = [self.root]
        slef.margin = margin
        
    def split(self):
        for n in self.leaves:
            p = random.randint(0,1)
            if p == 0:
                #0 means horizontal split 1 means vertical split
                width = random.randint(20,n.width-10)
                l = Node(n,width,n.height)
                
@dataclass 
class Room:
    
    

class Wall(pygame.sprite.Sprite):
    def __init__(self,colour,width,height,x,y):
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
    def __init__(self,colour,width,height,speed):
        super().__init__()
        
        #set player dimentions
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface([width,height])
        self.image.fill(colour)
        
        #set position of player need to make it so the player starts in a spot with no wall
        self.rect = self.image.get_rect()
        
        fini = False
        i = 0
        while not fini and i < len(map):
            j = 0
            while not fini and j < len(map[i]):
                if (map[i][j]) == 0:
                    self.rect.x,self.rect.y  = (i)*width,(j)*height
                    fini = True
                    print(map)
                    print(i,j,map[i][j])
                j += 1     #same as j = j + 1
            i += 1
        self.old_x =  self.rect.x
        self.old_y = self.rect.y
        
    def update(self):
        
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y
        
        wall_hit_list = pygame.sprite.spritecollide(my_player, wall_group, False)
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
        
# make it so limited number of walls so that there will always be a route. so there needs to be counter that loses one each time a wall is drawn
# rule that for a wall to be generated the previous free space must have at least one other free space connected
# create the grid and make the path first set values to 1 the create the map so its not touching the path.
# map = [[random.randint(0,1) for i  in range(numcols)]for j in range(numrows)]
 # a wall is drawn if the value in the array is == to 1
 
def generate():
    map = [[0]*numrows for i in range(numcols)]
    for i in range(numcols):
        for j in range(numrows):
            v = random.randint(0,1)
            map[i][j] = v
            if v == 1:
                my_wall = Wall(WHITE,width,height,i*width,j*height)
                all_sprite_group.add(my_wall)
                wall_group.add(my_wall)
            elif v== 0:
                my_floor = Floor(width,height,i*width,j*height)
                all_sprite_group.add(my_floor)
                floor_group.add(my_floor)
            #end if
        #next column 
    #next row
    return map

all_sprite_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
map = generate()
my_player = Player(YELLOW,width,height,speed)
all_sprite_group.add(my_player)


pygame.init()
#game loop
while not done:
    #user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
         
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#if left key is pressed
                my_player.player_set_speed(-1,0)
            elif event.key == pygame.K_RIGHT:
                my_player.player_set_speed(1,0)
            elif event.key == pygame.K_UP:
                my_player.player_set_speed(0,-1)
            elif event.key == pygame.K_DOWN:
                my_player.player_set_speed(0,1)
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                my_player.player_set_speed(0,0)
    
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
pygame.quit()