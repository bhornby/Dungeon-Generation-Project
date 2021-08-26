import random
import pygame
import sys
from bsp_alg import DungeonGenerator

YELLOW = (255,255,0)
BLACK = (0,0,0)

offset_x = -100
offset_y = -200
window_width = 1000
window_height = 720
    
class Wall(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Floor(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite): 
    def __init__(self,colour,tile_size,speed,dungeon,wall_group,offset_x, offset_y, window_width, window_height):
        super().__init__()
        
        #set player dimentions
        self.wall_group = wall_group
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface([tile_size//2,tile_size//2])
        self.image.fill(colour)
        
        #set position of player need to make it so the player starts in a spot with no wall
        self.rect = self.image.get_rect()
        
        
        for i in range(offset_y // tile_size, window_height // tile_size):
            for j in range(offset_x // tile_size, window_width // tile_size):
                v = dungeon.tiles[j][i].tile
                if v == "#":
                    continue
                elif v == ".":
                    self.rect.x  = (j) * tile_size + offset_x % tile_size  
                    self.rect.y  = (i) * tile_size + offset_y % tile_size 
                       
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

def render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group, tile_size, offset_x, offset_y, window_width, window_height):        
    v = None
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("stonebrick.png").convert(),(tile_size,tile_size))
    FlOOR_IMAGE = pygame.transform.scale(pygame.image.load("floor.png").convert(),(tile_size,tile_size))
    for i in range(offset_y // tile_size, window_height // tile_size):
        for j in range(offset_x // tile_size, window_width // tile_size):
            x = j*tile_size + offset_x % tile_size
            y = i*tile_size + offset_y % tile_size
            v = dungeon.tiles[j][i].tile
            if v == "#":
                my_wall = Wall(WALL_IMAGE, x, y)
                all_sprite_group.add(my_wall)
                wall_group.add(my_wall)
            elif v == "." or v == "c":
                my_floor = Floor(FlOOR_IMAGE, x, y)
                all_sprite_group.add(my_floor)
                floor_group.add(my_floor)
                #end if
        #next colum
    #next row
                
def main_loop(screen, clock, tile_size, numrows, numcols):
    speed = 5
    all_sprite_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    dungeon = DungeonGenerator(numcols*10,numrows*10)
    dungeon.generate_map()
    render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group, tile_size,offset_x, offset_y, window_width, window_height)
    my_player = Player(YELLOW,tile_size,speed, dungeon,wall_group,offset_x, offset_y, window_width, window_height)
    all_sprite_group.add(my_player)
    
    
    #exit game falg set to false
    done = False
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
                elif event.key == pygame.K_ESCAPE:
                    done = True
                    
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
# end function
