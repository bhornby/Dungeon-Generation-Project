import random
import pygame
import sys
from bsp_alg import DungeonGenerator

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255, 0, 0)
LIGHT_RED = (255, 127, 127)
COLOUR_DARK_WALL = (0, 0, 100)
COLOUR_DARK_GROUND = (50, 50, 150)

# core attributes
width = 10
height = 10
speed = 5
numcols = 25
numrows = 20

#black screen
screen_size = (1000,720)

screen = pygame.display.set_mode(screen_size)

#screen refresh rate
clock = pygame.time.Clock()
    
    
class Wall(pygame.sprite.Sprite):
    
    WALL_IMAGE = pygame.transform.scale(pygame.image.load("stonebrick.png").convert(),(width,height))
    
    def __init__(self,width,height,x,y):
        super().__init__()
        self.image = Wall.WALL_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Floor(pygame.sprite.Sprite):
    
    FlOOR_IMAGE = pygame.transform.scale(pygame.image.load("floor.png").convert(),(width,height))

    def __init__(self,width,heigh,x,y):
        super().__init__()
        self.image = Floor.FlOOR_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Button():
    def __init__(self, x,y,width,height,color, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        
    def draw(self,screen,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('m5x7', 40)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos = the mouse co-ords
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True    
        return False
         
        
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
                if dungeon.dungeon[i][j].tile != '#':
                    self.rect.x  = (i) * width
                    self.rect.y  = (j) * height
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
        

def draw_text(text, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    x = (screen.get_width()//2 - textobj.get_width()//2)
    y = (screen.get_height()//4 - textobj.get_height()//2)
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def options_menu():
    options = True
    
    screen_size_button = Button(screen.get_width()//2 - 100, screen.get_height()//3, 200, 50, RED,'Screen Size')
    controls_button = Button(screen.get_width()//2 - 100, screen.get_height()//2.4, 200, 50, RED, 'Controls')
    audio_button = Button(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50, RED, 'Audio')
    
    
    def display_options():
        
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Options', font , BLACK, screen,)
        
        screen_size_button.draw(screen,BLACK)
        controls_button.draw(screen,BLACK)
        audio_button.draw(screen,BLACK)
            
    display_options()
    while options:
        
        pos = pygame.mouse.get_pos()
         
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("bye")
                    options = False
            
            if event.type == pygame.MOUSEMOTION:
                if screen_size_button.isOver(pos):
                    screen_size_button.color = LIGHT_RED
                    screen_size_button.draw(screen, BLACK)
                
                else:
                    screen_size_button.color = RED
                    screen_size_button.draw(screen, BLACK)
                    
                    
                if controls_button.isOver(pos):
                    controls_button.color = LIGHT_RED
                    controls_button.draw(screen, BLACK)
                
                else:
                    controls_button.color = RED
                    controls_button.draw(screen, BLACK)
                
                if audio_button.isOver(pos):
                    audio_button.color = LIGHT_RED
                    audio_button.draw(screen, BLACK)
                
                else:
                    audio_button.color = RED
                    audio_button.draw(screen, BLACK)
                
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_size_button.isOver(pos):
                    pass
                    
                if controls_button.isOver(pos):
                    pass
                
                if audio_button.isOver(pos):
                    pass
            
                    
        pygame.display.update()
        clock.tick(60)               

def difficulty_menu():
    
    difficulty = True
    
    hard_button = Button(screen.get_width()//2 - 100, screen.get_height()//3, 200, 50, RED,'Hard')
    medium_button = Button(screen.get_width()//2 - 100, screen.get_height()//2.4, 200, 50, RED, 'Medium')
    easy_button = Button(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50, RED, 'Easy')
    
    
    def display_difficulty():
        
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Difficulty', font , BLACK, screen,)
        
        hard_button.draw(screen,BLACK)
        medium_button.draw(screen,BLACK)
        easy_button.draw(screen,BLACK)
            
    display_difficulty()
    
    while difficulty:
        
        pos = pygame.mouse.get_pos()
         
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("done")
                    difficulty = False
            
            if event.type == pygame.MOUSEMOTION:
                if hard_button.isOver(pos):
                    hard_button.color = LIGHT_RED
                    hard_button.draw(screen, BLACK)
                
                else:
                    hard_button.color = RED
                    hard_button.draw(screen, BLACK)
                    
                    
                if medium_button.isOver(pos):
                    medium_button.color = LIGHT_RED
                    medium_button.draw(screen, BLACK)
                
                else:
                    medium_button.color = RED
                    medium_button.draw(screen, BLACK)
                
                if easy_button.isOver(pos):
                    easy_button.color = LIGHT_RED
                    easy_button.draw(screen, BLACK)
                
                else:
                    easy_button.color = RED
                    easy_button.draw(screen, BLACK)
                
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hard_button.isOver(pos):
                    pass
                    
                if medium_button.isOver(pos):
                    pass
                
                if easy_button.isOver(pos):
                    pass
            
                    
        pygame.display.update()
        clock.tick(60)               
    

def main_menu():
    
    menu = True
    # self, x,y,width,height,color, text=''
    button_1 = Button(screen.get_width()//2 - 100, screen.get_height()//3, 200, 50, RED,'Start Game')
    button_2 = Button(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50, RED, 'Options')
    button_3 = Button(screen.get_width()//2 - 100, screen.get_height()//2.4, 200, 50, RED, 'Difficulty')
    #should probably make a button class
    
    def display_menu():
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Main Menu', font , BLACK, screen,)

        button_1.draw(screen, BLACK)
        button_2.draw(screen, BLACK)
        button_3.draw(screen, BLACK)
        
    display_menu()
    while menu:
        
        pos = pygame.mouse.get_pos()        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("bye")
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEMOTION:
                if button_1.isOver(pos):
                    button_1.color = LIGHT_RED
                    button_1.draw(screen, BLACK)
                
                else:
                    button_1.color = RED
                    button_1.draw(screen, BLACK)
                    
                    
                if button_2.isOver(pos):
                    button_2.color = LIGHT_RED
                    button_2.draw(screen, BLACK)
                
                else:
                    button_2.color = RED
                    button_2.draw(screen, BLACK)
                
                if button_3.isOver(pos):
                    button_3.color = LIGHT_RED
                    button_3.draw(screen, BLACK)
                
                else:
                    button_3.color = RED
                    button_3.draw(screen, BLACK)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.isOver(pos):
                    main_loop()
                    display_menu()
                    
                if button_2.isOver(pos):
                    options_menu()   
                    display_menu()
                
                if button_3.isOver(pos):
                    difficulty_menu()
                    display_menu()
            
        pygame.display.update()
        clock.tick(60)
        
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
    dungeon = DungeonGenerator(70,70)
    dungeon.generate_map()
    render_pygame_map(dungeon, floor_group, wall_group, all_sprite_group)
    my_player = Player(YELLOW,width,height,speed, dungeon,wall_group)
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

pygame.init()
main_menu()
pygame.quit()