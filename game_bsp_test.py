import random
import pygame
import sys
from random import randrange
from random import choice

from bsp_alg import DungeonGenerator


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

WALL_IMAGE = pygame.transform.scale(pygame.image.load("stonebrick.png").convert(),(width,height))

FLOOR_IMAGE = pygame.transform.scale(pygame.image.load("floor.png").convert(),(width,height))

class Wall(pygame.sprite.Sprite):
    def __init__(self,width,height,x,y):
        super().__init__()
        self.image = WALL_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Floor(pygame.sprite.Sprite):
    def __init__(self,width,heigh,x,y):
        super().__init__()
        self.image = FLOOR_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                
    
def render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group):        
    v = None
    
    for i in range(dungeon.height):
        for j in range(dungeon.width):
            v = dungeon.dungeon[i][j].tile
            if v == "#":
                my_wall = Wall(width,height,i*width,j*height)
                all_sprite_group.add(my_wall)
                wall_group.add(my_wall)
            elif v == "." or v == "c":
                my_floor = Floor(width,height,i*width,j*height)
                all_sprite_group.add(my_floor)
                floor_group.add(my_floor)
                #end if
        #next colum
    #next row
                               
def main_loop():
    all_sprite_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    
    dungeon = DungeonGenerator(width * (numcols), height * numrows)
    dungeon.generate_map()
    render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group)
    
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