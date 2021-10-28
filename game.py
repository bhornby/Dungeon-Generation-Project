import random
import pygame
import sys
from bsp_alg import DungeonGenerator
from pygame import gfxdraw
from bsp_alg import DungeonSqr

YELLOW_ISH = (238,238,204)
YELLOW = (255,255,0)
RED = (255,0,0)
BLUE = (173, 216, 230)
BLACK = (0,0,0)
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
    def __init__(self, image, x, y, player, key_count, screen, clock, tile_size, numrows, numcols, map_factor):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.key_count = key_count
        self.screen = screen
        self.clock = clock
        self.tile_size = tile_size
        self.numrows = numrows
        self.numcols = numcols
        self.map_factor = map_factor
    
    def update(self):
        portal_hit_list = pygame.sprite.spritecollide(self, [self.player],False )
        for x in portal_hit_list:
            if self.player.key_inventory == self.key_count:
                main_loop(self.screen, self.clock, self.tile_size, self.numrows, self.numcols, self.key_count, self.map_factor)
                print("hit_portal_level_up")
            else:
              break  
                
                
            

class Key(pygame.sprite.Sprite):
    def __init__(self,image,x,y,col,row, dungeon, player):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.col = col
        self.row = row
        self.player = player
        self.dungeon = dungeon
        
    def update(self):
        key_hit_list = pygame.sprite.spritecollide(self, [self.player],False )
        for x in key_hit_list:
            self.dungeon.tiles[self.col][self.row] = DungeonSqr('.')
            self.player.key_inventory = self.player.key_inventory + 1
            print(self.player.key_inventory)
            
class Player(pygame.sprite.Sprite): 
    def __init__(self,colour,tile_size,speed,dungeon,wall_group,offset_x, offset_y, window_width, window_height):
        super().__init__()
        
        #set player dimentions
        self.wall_group = wall_group
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface([tile_size//2,tile_size//2])
        self.image.fill(colour)
        self.key_inventory = 0
        
        self.rect = self.image.get_rect()              
        self.window_width = window_width
        self.window_height = window_height
        self.detection_zone = tile_size * 5
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.old_x = 0
        self.old_y = 0
        self.step_size= 10
        
    def locate(self, dungeon, tile_size):        
        a = 0
        b = dungeon.height - 1
        c = 0
        d = dungeon.width - 1
            
        for my in range(a, b):
            for mx in range(c, d):
                v = dungeon.tiles[mx][my].tile
                if v == "p":
                    self.rect.x = (mx * tile_size) 
                    self.rect.y = (my * tile_size)  
                    self.old_x = self.rect.x
                    self.old_y = self.rect.y
                    return
                    #end if
            #next colum
        #next row            
        
        
    def shift(self):
        if self.rect.x > self.window_width - self.detection_zone:
            self.offset_x += self.step_size
            self.rect.x -= self.step_size
                    
        elif self.rect.x < self.detection_zone:
            self.offset_x -= self.step_size
            self.rect.x += self.step_size
        
        elif self.rect.y > self.window_height - self.detection_zone:
            self.offset_y +=  self.step_size
            self.rect.y -= self.step_size
            
        elif self.rect.y < self.detection_zone:
            self.offset_y -= self.step_size
            self.rect.y += self.step_size
        else:
            self.step_size = 2

        
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
        
        if b >= dungeon.height:
            b = dungeon.height - 1
        
        if d >= dungeon.width:
            d = dungeon.width - 1
            
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
                elif v == "ep":
                    colour = RED
                elif v == "k":
                    colour = YELLOW_ISH 
                gfxdraw.pixel(self.mini, j, i, colour)
        
        gfxdraw.pixel(self.mini, (player_x + offset_x)// tile_size, (player_y + offset_y) // tile_size, YELLOW)
        self.image = pygame.transform.scale(self.mini, (self.scale * self.width, self.scale * self.height)) 
        
                             
                    
def render_pygame_map(dungeon, wall_img, floor_img, portal_img, end_portal_img, key_img, tile_size,window_width, window_height, my_player, key_count, screen, clock, numrows, numcols, map_factor):        
    walls = []
    floors = []
    s_portal = []
    e_portal = []
    keys = []
    
    a = ((my_player.offset_y // tile_size))
    b = (((my_player.offset_y + window_height) // tile_size)) + 1 
    c = ((my_player.offset_x // tile_size))
    d = (((my_player.offset_x + window_width) // tile_size)) + 1
    
    if b >= dungeon.height:
        b = dungeon.height - 1
        
    if d >= dungeon.width:
        d = dungeon.width - 1
    
    for i in range(a, b):
        for j in range(c, d):
            x = (j * tile_size - my_player.offset_x) 
            y = (i * tile_size - my_player.offset_y)
            v = dungeon.tiles[j][i].tile
            if v == "#":
                walls.append(Wall(wall_img, x, y))
            elif v == "." or v == "c":
                floors.append(Floor(floor_img, x, y))
            elif v == "p":
                start_portal = Portal(portal_img, x, y, my_player, key_count, screen, clock, tile_size, numrows, numcols, map_factor)
                s_portal.append(start_portal)
            elif v == "ep":
                end_portal = Portal(end_portal_img, x, y, my_player, key_count, screen, clock, tile_size, numrows, numcols, map_factor)
                e_portal.append(end_portal)
            elif v == "k":
                keys.append(Key(key_img, x, y, j, i, dungeon, my_player))
                
                #end if
        #next colum
    #next row
    return (walls, floors, s_portal, e_portal, keys)

def show_keys_left(key_count,my_player,screen):
    x = 10
    y = 10
    font = pygame.font.SysFont('m5x7', 40, True, False)
    text = font.render("Keys Left: " + str(key_count - my_player.key_inventory),True,YELLOW_ISH)
    screen.blit(text, (x,y))
    
def main_loop(screen, clock, tile_size, numrows, numcols, key_count, map_factor):
    speed = 5
    
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("brick.png").convert(),(tile_size,tile_size))
    FLOOR_IMAGE = pygame.transform.scale(pygame.image.load("floorcolour.png").convert(),(tile_size,tile_size))
    PORTAL_IMAGE = pygame.transform.scale(pygame.image.load("PORTAL_final.png").convert(),(tile_size,tile_size))
    END_PORTAL_IMAGE = pygame.transform.scale(pygame.image.load("END_PORTAL.png").convert(),(tile_size,tile_size))
    KEY_IMAGE = pygame.transform.scale(pygame.image.load("REAL_KEY.png").convert(),(tile_size,tile_size))
    
    window_width = numcols * tile_size
    window_height = numrows * tile_size
    
    background_sprite_group = pygame.sprite.Group()
    foreground_sprite_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    s_portal_group = pygame.sprite.Group()
    e_portal_group = pygame.sprite.Group()
    key_group = pygame.sprite.Group()
    
    dungeon = DungeonGenerator(numcols * map_factor, numrows * map_factor, key_count)
    print(key_count)
    dungeon.generate_map()
    
    my_player = Player(YELLOW,tile_size,speed, dungeon, wall_group, 0, 0, window_width, window_height)
    my_player.locate(dungeon, tile_size)
    foreground_sprite_group.add(my_player)
    
    dungeon_mini = MiniMap(dungeon.width,dungeon.height,BLACK, dungeon, tile_size, my_player.offset_x, my_player.offset_y, window_width, window_height)
    foreground_sprite_group.add(dungeon_mini)
   
    
    
    #exit game flag set to false
    done = False
    old_walls = []
    old_floors = []
    old_s_portal = []
    old_e_portal = []
    old_keys = []
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
        
        (walls, floors, s_portal, e_portal, keys) = render_pygame_map(dungeon, WALL_IMAGE, FLOOR_IMAGE, PORTAL_IMAGE, END_PORTAL_IMAGE, KEY_IMAGE, tile_size, window_width, window_height, my_player, key_count, screen, clock, numrows, numcols, map_factor)
        dungeon_mini.reveal(dungeon, tile_size, my_player.offset_x, my_player.offset_y, window_width, window_height,my_player.rect.x, my_player.rect.y)
        # TODO remove old walls and floors, then add new ones and reset old ones
        
        background_sprite_group.remove(old_walls)
        background_sprite_group.remove(old_floors)
        background_sprite_group.remove(old_s_portal)
        background_sprite_group.remove(old_e_portal)
        background_sprite_group.remove(old_keys)
        
        background_sprite_group.add(walls)
        background_sprite_group.add(floors)
        background_sprite_group.add(s_portal)
        background_sprite_group.add(e_portal)
        background_sprite_group.add(keys)
        
        wall_group.remove(old_walls)
        wall_group.add(walls)
        
        s_portal_group.remove(old_s_portal)
        s_portal_group.add(s_portal)
        
        e_portal_group.remove(old_e_portal)
        e_portal_group.add(e_portal)
        
        key_group.remove(old_keys)
        key_group.add(keys)
        
        old_walls = walls
        old_floors = floors
        old_s_portal = s_portal
        old_e_portal = e_portal
        old_keys = keys
        
        
        
        #update all sprites
        foreground_sprite_group.update()
        background_sprite_group.update()
        #screen background is black
        screen.fill(BLACK)
        #draw function
        background_sprite_group.draw(screen)
        foreground_sprite_group.draw(screen)
        #flip display to show new position of objects
        show_keys_left(key_count,my_player,screen)
        
        
        pygame.display.flip()
        clock.tick(240)
#end game loop
# end function
