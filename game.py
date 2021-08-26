import random
import pygame
import sys
from bsp_alg import DungeonGenerator

YELLOW = (255,255,0)
BLACK = (0,0,0)
    
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
    def __init__(self,colour,width,height,speed,dungeon,wall_group):
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
        while not fini and i < dungeon.width:
            j = 0
            while not fini and j < dungeon.height:
                if dungeon.tiles[j][i].tile != '#':
                    self.rect.x  = (j) * width  
                    self.rect.y  = (i) * height  
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

def render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group, tile_size):        
    v = None
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("stonebrick.png").convert(),(tile_size,tile_size))
    FlOOR_IMAGE = pygame.transform.scale(pygame.image.load("floor.png").convert(),(tile_size,tile_size))
    for i in range(dungeon.height):
        for j in range(dungeon.width):
            x = j*tile_size
            y = i*tile_size
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
    dungeon = DungeonGenerator(numrows*10, numcols*10)
    dungeon.generate_map()
    render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group, tile_size)
    #my_player = Player(YELLOW,tile_size,tile_size,speed, dungeon,wall_group)
    #all_sprite_group.add(my_player)
    
    
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
