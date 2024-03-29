import pygame
import math
from bsp_alg import DungeonGenerator
from pygame import gfxdraw
from bsp_alg import DungeonSqr
from random import randint

YELLOW_ISH = (238,238,204)
YELLOW = (255,255,0)
RED = (255,0,0)
BLUE = (173, 216, 230)
BLACK = (0,0,0)
COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_FLOOR = (50, 50, 150)
GREY = (192,192,192)
WHITE = (255,255,255)


class Wall(pygame.sprite.Sprite):
    def __init__(self,image,x,y,col,row):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.col = col
        self.row = row

class Floor(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Portal(pygame.sprite.Sprite):
    def __init__(self, image, x, y, player, key_count):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.key_count = key_count
        
    
    def update(self):
        portal_hit_list = pygame.sprite.spritecollide(self, [self.player],False )
        for _x in portal_hit_list:
            if self.player.key_inventory == self.key_count:
                self.player.key_inventory = None
 
            
class Key(pygame.sprite.Sprite):
    def __init__(self,image,x,y,col,row, dungeon, player):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.col = col
        self.row = row
        self.player = player
        self.dungeon = dungeon
        
    def update(self):
        key_hit_list = pygame.sprite.spritecollide(self, [self.player],False )
        for _x in key_hit_list:
            self.dungeon.tiles[self.col][self.row] = DungeonSqr('.')
            self.player.key_inventory = self.player.key_inventory + 1
   
class Sword (pygame.sprite.Sprite):
    def __init__(self,colour,x,y,player, damage, tile_size):
        super().__init__()
        
        self.colour = colour
        self.image = pygame.Surface((tile_size,tile_size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x  = x
        self.rect.y = y
        self.player = player
        self.damage = damage

class Monster(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, tile_size, wall_group, col, row, player):
        super().__init__()
        
        self.colour  = colour
        self.image = pygame.Surface((tile_size,tile_size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.col = col
        self.row = row
        
        self.wall_group = wall_group
        self.speed_x = 0
        self.speed_y = 0
        self.old_x = x
        self.old_y = y
        self.health = 2
        self.tile_size = tile_size
        self.tracking_count = 0
        
    def has_hit_wall(self):
        wall_hit_list = pygame.sprite.spritecollide(self, self.wall_group, False)
        for w in wall_hit_list:
            return w
        return False
    
    
    def update(self, player):
        w = self.has_hit_wall()
        if w:
            self.speed_x *= -1
            self.speed_y *= -1
            self.rect.x = self.old_x
            self.rect.y = self.old_y
            w = self.has_hit_wall()
            if w:
                x_diff = self.rect.x - w.rect.x 
                y_diff = self.rect.y - w.rect.y
                if x_diff > 0 and x_diff < w.rect.width:
                    self.rect.x += w.rect.width - x_diff
                elif x_diff < 0 and x_diff > -w.rect.width:
                    self.rect.x -= w.rect.width + x_diff
                if y_diff > 0 and y_diff < w.rect.height:
                    self.rect.y += w.rect.height - y_diff
                elif y_diff < 0 and y_diff > -w.rect.height:
                    self.rect.y -= w.rect.height + y_diff
                self.old_x = self.rect.x
                self.old_y = self.rect.y
    
        else:
            self.direction(player)
                
            self.old_x = self.rect.x
            self.old_y = self.rect.y       
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
    
    
    def direction(self, player):
        # -1 means dont change direction
        dir = -1
        
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(abs(dx), abs(dy))
        speed = 2
        tracking_colour = WHITE
        radius = 0
        
        if self.tracking_count < 20:
            radius = self.tile_size * 4
            tracking_colour = YELLOW
        else:
            radius = self.tile_size * 2
        
        if self.tracking_count > 0 and self.speed_x == 0 and self.speed_y == 0:
            self.tracking_count -= 1
        else:
            if dist < radius:
                # home in on player
                self.tracking_count += 1
                self.image.fill(tracking_colour)
                speed = 1
                if abs(dy) > abs(dx):
                    if dy > 0:
                        dir = 2
                    else:
                        dir = 3
                else:
                    if dx > 0:
                        dir = 0
                    else:
                        dir = 1
            else:
                if self.tracking_count > 0:
                    self.tracking_count -= 1
                self.image.fill(RED)
                # far enough away for random movement
                change_dir = randint(0,19)
                if change_dir == 1:
                    dir = randint(0,3)
            
                
        if dir == 0:
            self.speed_x = speed
            self.speed_y = 0
        elif dir == 1:
            self.speed_x = -speed
            self.speed_y = 0 
        elif dir == 2:
            self.speed_y = speed
            self.speed_x = 0 
        elif dir == 3:
            self.speed_y = -speed
            self.speed_x = 0



class Player(pygame.sprite.Sprite): 
    def __init__(self,player_image,tile_size,wall_group,offset_x, offset_y, window_width, window_height, monster_group, life_count):
        super().__init__()
        
        #set player dimentions
        self.wall_group = wall_group
        self.monster_group = monster_group
        self.speed_x = 0
        self.speed_y = 0
        self.image = player_image
#         pygame.Surface([tile_size//2,tile_size//2])
#         self.image.fill(colour)
        self.key_inventory = 0
        
        self.rect = self.image.get_rect()              
        self.window_width = window_width
        self.window_height = window_height
        self.detection_zone = tile_size * 5
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.old_x = 0
        self.old_y = 0
        self.step_size = 10
        self.life_count = life_count
        
        
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
             
             
    def has_hit_wall(self):
        wall_hit_list = pygame.sprite.spritecollide(self, self.wall_group, False)
        return len(wall_hit_list) > 0
    
    def has_hit_monster(self):
        monster_hit_list = pygame.sprite.spritecollide(self, self.monster_group, False)
        for m in monster_hit_list:
            m.rect.x = m.old_x
            m.rect.y = m.old_y
            m.speed_x = 0
            m.speed_y = 0
        return len(monster_hit_list) > 0
     
    def update(self):
        if self.has_hit_wall():
            self.rect.x = self.old_x
            self.rect.y = self.old_y
            self.speed_x = 0
            self.speed_y = 0
            
        elif self.has_hit_monster():
            self.life_count = self.life_count  - 1
            self.rect.x = self.old_x
            self.rect.y = self.old_y
            self.speed_x = 0
            self.speed_y = 0
            
        else:
            self.old_x = self.rect.x
            self.old_y = self.rect.y
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def set_speed(self,x,y):
        self.speed_x = x
        self.speed_y = y


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, width,height,colour, window_width):
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
        
        
    def reveal(self, dungeon, tile_size,window_width, window_height, player):
        colour = None
        a = ((player.offset_y // tile_size))
        b = (((player.offset_y + window_height) // tile_size)) + 1
        c = ((player.offset_x // tile_size))
        d = (((player.offset_x + window_width) // tile_size)) + 1
        
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
                elif v == "e":
                    colour = BLUE
                elif v == "k":
                    colour = YELLOW_ISH
                elif v == "m":
                    colour = RED
                gfxdraw.pixel(self.mini, j, i, colour)
        
        gfxdraw.pixel(self.mini, (player.rect.x + player.offset_x)// tile_size, (player.rect.y + player.offset_y) // tile_size, YELLOW)
        self.image = pygame.transform.scale(self.mini, (self.scale * self.width, self.scale * self.height)) 
       
                             
def shift(player, monster_group, wall_group):
    if player.has_hit_wall():
        return
        
    if player.rect.x > player.window_width - player.detection_zone:
        player.offset_x += player.step_size
        player.rect.x -= player.step_size
        for i in monster_group:
            i.old_x -= player.step_size
            i.rect.x -= player.step_size
        for i in wall_group:
            i.rect.x -= player.step_size
                
    elif player.rect.x < player.detection_zone:
        player.offset_x -= player.step_size
        player.rect.x += player.step_size
        for i in monster_group:
            i.old_x += player.step_size
            i.rect.x += player.step_size
        for i in wall_group:
            i.rect.x += player.step_size
    
    elif player.rect.y > player.window_height - player.detection_zone:
        player.offset_y +=  player.step_size
        player.rect.y -= player.step_size
        for i in monster_group:
            i.old_y -= player.step_size
            i.rect.y -= player.step_size
        for i in wall_group:
            i.rect.y -= player.step_size
        
    elif player.rect.y < player.detection_zone:
        player.offset_y -= player.step_size
        player.rect.y += player.step_size
        for i in monster_group:
            i.old_y += player.step_size
            i.rect.y += player.step_size
        for i in wall_group:
            i.rect.y += player.step_size
    else:
        player.step_size = 2
        
                             
                             
def render_pygame_map(dungeon, wall_img, floor_img, portal_img, end_portal_img, key_img, tile_size, window_width, window_height, my_player, wall_group, monster_group):        
    walls = []
    floors = []
    s_portal = []
    e_portal = []
    keys = []
    monsters = []
    
    buffer = 1
    a = ((my_player.offset_y // tile_size))
    b = (((my_player.offset_y + window_height) // tile_size)) + buffer
    c = ((my_player.offset_x // tile_size))
    d = (((my_player.offset_x + window_width) // tile_size)) + buffer
    
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
                existing = False
                for w in wall_group:
                    if w.col == j and w.row == i:
                        walls.append(w)
                        existing=True
                        break
                if not existing:
                    walls.append(Wall(wall_img, x, y, j, i))
            elif v == "." or v == "c":
                floors.append(Floor(floor_img, x, y))
            elif v == "p":
                start_portal = Portal(portal_img, x, y, my_player, dungeon.key_count)
                s_portal.append(start_portal)
            elif v == "e":
                end_portal = Portal(end_portal_img, x, y, my_player, dungeon.key_count)
                e_portal.append(end_portal)
            elif v == "k":
                keys.append(Key(key_img, x, y, j, i, dungeon, my_player))
            elif v == "m":
                existing = False
                floors.append(Floor(floor_img, x, y))
                for m in monster_group:
                    if m.col == j and m.row == i:
                        monsters.append(m)
                        existing=True
                        break
                if not existing:
                    monsters.append(Monster(RED, x, y, tile_size, wall_group, j, i, my_player))
                #end if
        #next colum
    #next row
    return (walls, floors, s_portal, e_portal, keys, monsters)

def show_keys_left(key_count,my_player,screen):
    x = 10
    y = 10
    font = pygame.font.SysFont('m5x7', 40, True, False)
    text = font.render("Keys Left: " + str(key_count - my_player.key_inventory),True,YELLOW_ISH)
    screen.blit(text, (x,y))
    
def show_level(screen, level):
    x = 10
    y = 50
    font = pygame.font.SysFont('m5x7', 40, True, False)
    text = font.render("Level: " + str(level),True,YELLOW_ISH)
    screen.blit(text, (x,y))

def show_life(screen, life_count):
    x = 10
    y = 90
    font = pygame.font.SysFont('m5x7', 40, True, False)
    text = font.render("Hearts: " + str(life_count),True,YELLOW_ISH)
    screen.blit(text, (x,y))
    
    
def main_loop(screen, clock, tile_size, numrows, numcols, keys_asked, map_factor, level, enemy_count, life_count):
    print(life_count)
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("brick.png").convert(),(tile_size,tile_size))
    FLOOR_IMAGE = pygame.transform.scale(pygame.image.load("floorcolour.png").convert(),(tile_size,tile_size))
    PORTAL_IMAGE = pygame.transform.scale(pygame.image.load("PORTAL_final.png").convert(),(tile_size,tile_size))
    END_PORTAL_IMAGE = pygame.transform.scale(pygame.image.load("END_PORTAL.png").convert(),(tile_size,tile_size))
    KEY_IMAGE = pygame.transform.scale(pygame.image.load("REAL_KEY.png").convert(),(tile_size,tile_size))
    PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("Hero_cropped.png").convert(),(30,30)) 
    
    window_width = numcols * tile_size
    window_height = numrows * tile_size
    
    background_sprite_group = pygame.sprite.Group()
    mini_map_sprite_group = pygame.sprite.Group()
    player_sprite_group = pygame.sprite.Group()
    
    wall_group = pygame.sprite.Group()
    s_portal_group = pygame.sprite.Group()
    e_portal_group = pygame.sprite.Group()
    key_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    
    dungeon = DungeonGenerator(numcols * map_factor, numrows * map_factor, keys_asked, enemy_count)
    dungeon.generate_map()
    
    my_player = Player(PLAYER_IMAGE,tile_size, wall_group, 0, 0, window_width, window_height, monster_group, life_count)
    my_player.locate(dungeon, tile_size)
    player_sprite_group.add(my_player)
    
    iron_sword = Sword(GREY,0,0,my_player, 1, tile_size)
    
    dungeon_mini = MiniMap(dungeon.width, dungeon.height, BLACK, window_width)
    mini_map_sprite_group.add(dungeon_mini)

    old_walls = []
    old_floors = []
    old_s_portal = []
    old_e_portal = []
    old_keys = []
    old_monsters = []
    while True:
        #user input
        if my_player.key_inventory is None:
            my_player.key_inventory = 0
            return (False, None)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (True, None)
            
        
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:#if left key is pressed
                    my_player.set_speed(-my_player.step_size,0)    
                elif event.key == pygame.K_RIGHT:
                    my_player.set_speed(my_player.step_size,0)       
                elif event.key == pygame.K_UP:
                    my_player.set_speed(0,-my_player.step_size)        
                elif event.key == pygame.K_DOWN:
                    my_player.set_speed(0,my_player.step_size)       
                elif event.key == pygame.K_ESCAPE:
                    return (True,None)
#                 elif event.key == pygame.K_SPACE:
#                     for m in monster_group: #An array that holds instances of enemies 
#                         if  m.rect.x #Using distance forumla to calculate player x and y values in corresondance to an enemies x and y position 
#                             m.health -= iron_sword.damage #subtracts the enemies health by the amount of damage that the woodenSword does 

                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    my_player.set_speed(0,0)
        
        
        #update all sprites
        mini_map_sprite_group.update()
        background_sprite_group.update()
        player_sprite_group.update()
        monster_group.update(my_player)
        
        # modify offset
        shift(my_player, monster_group, wall_group)
        (walls, floors, s_portal, e_portal, keys, monsters) = render_pygame_map(dungeon, WALL_IMAGE, FLOOR_IMAGE, PORTAL_IMAGE, END_PORTAL_IMAGE, KEY_IMAGE, tile_size, window_width, window_height, my_player, wall_group, monster_group)
        dungeon_mini.reveal(dungeon, tile_size, window_width, window_height, my_player)
        
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
        
        monster_group.remove(old_monsters)
        monster_group.add(monsters)
        
        old_walls = walls
        old_floors = floors
        old_s_portal = s_portal
        old_e_portal = e_portal
        old_keys = keys
        old_monsters = monsters
     
        #screen background is black
        screen.fill(BLACK)
        
        #draw function
        background_sprite_group.draw(screen)
        mini_map_sprite_group.draw(screen)
        player_sprite_group.draw(screen)
        monster_group.draw(screen)
        
        #flip display to show new position of objects
        if my_player.key_inventory is not None:
            show_keys_left(dungeon.key_count,my_player,screen)
        show_level(screen, level)
        show_life(screen, my_player.life_count)
        
        if my_player.life_count <= 0:
            print("died")
            return (True, level)
        
        pygame.display.flip()
        clock.tick(60)
#end game loop
# end function
