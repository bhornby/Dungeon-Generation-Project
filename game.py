import random
import pygame
import sys
from bsp_alg import DungeonGenerator
from pygame import gfxdraw


YELLOW = (255,255,0)
BLUE = (173, 216, 230)
BLACK = (0,0,0)
offset_x = 80
offset_y = 40
COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_FLOOR = (50, 50, 150)


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
        
class Portal(pygame.sprite.Sprite):
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
        self.old_x = None
        self.old_y = None
        
        #set position of player need to make it so the player starts in a spot with no wall
        self.rect = self.image.get_rect()
    
        for i in range(offset_y // tile_size, window_height // tile_size):
            for j in range(offset_x // tile_size, window_width // tile_size):
                v = dungeon.tiles[j][i].tile
                if v == "p":
                    self.rect.x  = (j) * tile_size + offset_x % tile_size - offset_x 
                    self.rect.y  = (i) * tile_size + offset_y % tile_size - offset_y
                    self.old_x = self.rect.x
                    self.old_y = self.rect.y
                elif v == "#":
                    continue
                elif v == ".":
                    continue
                elif v == "c":
                    continue
                
           
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        self.window_width = window_width
        self.window_height = window_height
        self.detection_zone = tile_size * 4
           
    def shift(self):
        global offset_x
        global offset_y
        
        step_size = 2
        if self.rect.x > self.window_width - self.detection_zone:
            offset_x += step_size
            self.rect.x -= step_size
                    
        elif self.rect.x < self.detection_zone:
            offset_x -= step_size
            self.rect.x += step_size
        
        elif self.rect.y > self.window_height - self.detection_zone:
            offset_y +=  step_size
            self.rect.y -= step_size
            
        elif self.rect.y < self.detection_zone:
            offset_y -= step_size
            self.rect.y += step_size

        
    def update(self):     
        self.rect.x = self.rect.x + self.speed_x
        self.rect.y = self.rect.y + self.speed_y
        
        wall_hit_list = pygame.sprite.spritecollide(self, self.wall_group, False)
        for x in wall_hit_list:
            self.rect.x =  self.old_x 
            self.rect.y =  self.old_y 
            self.speed_x = 0
            self.speed_y = 0
        
        self.shift()
        self.old_x = self.rect.x
        self.old_y = self.rect.y
    
                    
    def player_set_speed(self,x,y):
        self.speed_x = x
        self.speed_y = y

class MiniMap(pygame.sprite.Sprite):
    def __init__(self, width,height,colour, dungeon, tile_size, offset_x, offset_y, window_width, window_height):
        super().__init__()
        self.width = width
        self.height = height
        self.mini = pygame.Surface([width, height])
        self.scale=2
        self.image = pygame.transform.scale(self.mini, (self.scale * self.width, self.scale * self.height)) 
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = window_width - self.width * self.scale - 10
        self.rect.y = 10
        
        
    def reveal(self, dungeon, tile_size, offset_x, offset_y, window_width, window_height,player_x, player_y):
        colour = None
        a = ((offset_y // tile_size))
        b = (((offset_y + window_height) // tile_size)) + 1
        c = ((offset_x // tile_size))
        d = (((offset_x + window_width) // tile_size)) + 1
        for i in range(a, b):
            for j in range(c, d):
                v = dungeon.tiles[j][i].tile
                if v == "#":
                    colour = COLOUR_DARK_FLOOR
                elif v == ".":
                    colour = COLOUR_DARK_WALL
                elif v == "c":
                    colour = COLOUR_DARK_WALL
                elif v == "p":
                    colour = BLUE
                gfxdraw.pixel(self.mini, j, i, colour)
        
        gfxdraw.pixel(self.mini, (player_x + offset_x)// tile_size, (player_y + offset_y) // tile_size, YELLOW)
        self.image = pygame.transform.scale(self.mini, (self.scale * self.width, self.scale * self.height)) 
        
                             
                    
def render_pygame_map(dungeon, wall_img, floor_img, portal_img, tile_size, offset_x, offset_y, window_width, window_height):        
    walls = []
    floors = []
    portal = []
    
    a = ((offset_y // tile_size))
    b = (((offset_y + window_height) // tile_size)) + 1 
    c = ((offset_x // tile_size))
    d = (((offset_x + window_width) // tile_size)) + 1
    
    if b >= dungeon.height:
        b = dungeon.height - 1
        
    if d >= dungeon.width:
        d = dungeon.width - 1
    
    for i in range(a, b):
        for j in range(c, d):
            x = (j * tile_size - offset_x) 
            y = (i * tile_size - offset_y)
            v = dungeon.tiles[j][i].tile
            if v == "#":
                walls.append(Wall(wall_img, x, y))
            elif v == "." or v == "c":
                floors.append(Floor(floor_img, x, y))
            elif v == "p":
                portal.append(Portal(portal_img, x, y))
                #end if
        #next colum
    #next row
    return (walls, floors, portal)
                
def main_loop(screen, clock, tile_size, numrows, numcols):
    speed = 5
    
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("brick.png").convert(),(tile_size,tile_size))
    FLOOR_IMAGE = pygame.transform.scale(pygame.image.load("floorcolour.png").convert(),(tile_size,tile_size))
    PORTAL_IMAGE = pygame.transform.scale(pygame.image.load("PORTAL_final.png").convert(),(tile_size,tile_size))
    
    window_width = numcols * tile_size
    window_height = numrows * tile_size
    
    background_sprite_group = pygame.sprite.Group()
    foreground_sprite_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    
    dungeon = DungeonGenerator(numcols*5, numrows*5)
    dungeon.generate_map()
    
    my_player = Player(YELLOW,tile_size,speed, dungeon,wall_group,offset_x, offset_y, window_width, window_height)
    foreground_sprite_group.add(my_player)
    
    dungeon_mini = MiniMap(dungeon.width,dungeon.height,BLACK, dungeon, tile_size, offset_x, offset_y, window_width, window_height)
    foreground_sprite_group.add(dungeon_mini)
   
    
    
    #exit game flag set to false
    done = False
    old_walls = []
    old_floors = []
    old_portal = []
    while not done:
        #user input
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:#if left key is pressed
                    my_player.player_set_speed(-2,0)    
                elif event.key == pygame.K_RIGHT:
                    my_player.player_set_speed(2,0)       
                elif event.key == pygame.K_UP:
                    my_player.player_set_speed(0,-2)        
                elif event.key == pygame.K_DOWN:
                    my_player.player_set_speed(0,2)       
                elif event.key == pygame.K_ESCAPE:
                    done = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    my_player.player_set_speed(0,0)
        
        (walls, floors, portal) = render_pygame_map(dungeon, WALL_IMAGE, FLOOR_IMAGE, PORTAL_IMAGE, tile_size, offset_x, offset_y, window_width, window_height)
        dungeon_mini.reveal(dungeon, tile_size, offset_x, offset_y, window_width, window_height,my_player.rect.x, my_player.rect.y)
        # TODO remove old walls and floors, then add new ones and reset old ones
        
        background_sprite_group.remove(old_walls)
        background_sprite_group.remove(old_floors)
        background_sprite_group.remove(old_portal)
        
        background_sprite_group.add(walls)
        background_sprite_group.add(floors)
        background_sprite_group.add(portal)
        
        wall_group.remove(old_walls)
        wall_group.add(walls)
        
        portal_group.remove(old_portal)
        portal_group.add(portal)
        
        old_walls = walls
        old_floors = floors
        old_portal = portal
        
        
        #update all sprites
        background_sprite_group.update()
        foreground_sprite_group.update()
        #screen background is black
        screen.fill(BLACK)
        #draw function
        background_sprite_group.draw(screen)
        foreground_sprite_group.draw(screen)
        #flip display to show new position of objects
        
        
        
        pygame.display.flip()
        clock.tick(240)
#end game loop
# end function
