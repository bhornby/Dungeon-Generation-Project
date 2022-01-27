import pygame
import sys

WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (255, 0, 0)
LIGHT_RED = (255, 127, 127)

clock = pygame.time.Clock()

# core attributes
tile_size = 40

numrows = 18
numcols = 25

enemy_count = 10
key_count = 5
map_factor = 2
difficulty = "EASY"
life_count = 5


#black screen
screen_size = (1000,720)
#tile_size * numcols, tile_size * numrows

screen = pygame.display.set_mode(screen_size)

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
            text = font.render(self.text, True, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos = the mouse co-ords
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True    
        return False


def draw_text(text, font, color, surface ,screen):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    x = (screen.get_width()//2 - textobj.get_width()//2)
    y = (screen.get_height()//4 - textobj.get_height()//2)
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def options_menu():
    options = True
    
    screen_size_button = Button(screen.get_width()//2 - 200, screen.get_height()//3, 400, 50, RED,'Use Arrow Keys to Move')
    controls_button = Button(screen.get_width()//2 - 200, screen.get_height()//2.4, 400, 50, RED, 'Collect keys to open Portals!')
    audio_button = Button(screen.get_width()//2 - 200, screen.get_height()//2, 400, 50, RED, 'Avoid monsters at all costs!')
    hint_4_button = Button(screen.get_width()//2 - 200, screen.get_height()//1.7, 400, 50, RED, 'Press ESC key to go back')
    
    
    
    
    def display_options():
        
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Hints', font , BLACK, screen,screen)
        
        screen_size_button.draw(screen,BLACK)
        controls_button.draw(screen,BLACK)
        audio_button.draw(screen,BLACK)
        hint_4_button.draw(screen, BLACK)
            
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
                
                if hint_4_button.isOver(pos):
                    hint_4_button.color = LIGHT_RED
                    hint_4_button.draw(screen, BLACK)
                
                else:
                    hint_4_button.color = RED
                    hint_4_button.draw(screen, BLACK)
                
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_size_button.isOver(pos):
                    pass
                    
                if controls_button.isOver(pos):
                    pass
                
                if audio_button.isOver(pos):
                    pass
                
                if hint_4_button.isOver(pos):
                    pass
            
                    
        pygame.display.update()
        clock.tick(60)               

def difficulty_menu():
    
    global key_count
    global map_factor
    global difficulty
    global life_count 
    
    difficulty = True
    
    hard_button = Button(screen.get_width()//2 - 125, screen.get_height()//3, 250, 50, RED,'Hard')
    medium_button = Button(screen.get_width()//2 - 125, screen.get_height()//2.4, 250, 50, RED, 'Medium')
    easy_button = Button(screen.get_width()//2 - 125, screen.get_height()//2, 250, 50, RED, 'Easy')
    
    
    def display_difficulty():
        
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Difficulty', font , BLACK, screen,screen)
        
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
                    enemy_count = 25
                    key_count = 20
                    map_factor = 5
                    life_count = 1
                    difficulty = "Hard"
                    
                if medium_button.isOver(pos):
                    enemy_count = 15
                    key_count = 15
                    map_factor = 3
                    life_count = 5
                    difficulty = "Medium"
                    
                if easy_button.isOver(pos):
                    enemy_count = 2
                    key_count = 5
                    map_factor = 2
                    life_count = 5
                    difficulty = "Easy"
                    
        pygame.display.update()
        clock.tick(60)

def game_over_menu(level_reached):
    menu = True
    
    button_1 = Button(screen.get_width()//2 - 125, screen.get_height()//2.4, 250, 50, RED,('Level Reached: ') + str(level_reached))
    button_2 = Button(screen.get_width()//2 - 125, screen.get_height()//3, 250, 50, RED, ('Difficulty: ') + str(difficulty) )
    button_3 = Button(screen.get_width()//2 - 125, screen.get_height()//2, 250, 50, RED, 'Return To Menu')
    
    def display_menu():
        font = pygame.font.SysFont('m5x7', 100)
        screen.fill(WHITE)
        draw_text('Game Over', font , BLACK, screen,screen)

        button_1.draw(screen, BLACK)
        button_2.draw(screen, BLACK)
        button_3.draw(screen, BLACK)
    
    display_menu()
    while menu:
        
        pos = pygame.mouse.get_pos()
         
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("done")
                    menu = False
        
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
                if button_3.isOver(pos):
                    print("done")
                    menu = False
                    
        pygame.display.update()
        clock.tick(60)
        
        
def main_menu():
    from game import main_loop
    menu = True
    # self, x,y,width,height,color, text=''
    button_1 = Button(screen.get_width()//2 - 100, screen.get_height()//3, 200, 50, RED,'Start Game')
    button_2 = Button(screen.get_width()//2 - 100, screen.get_height()//2.4, 200, 50, RED, 'Hints')
    button_3 = Button(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50, RED, 'Difficulty')
    #should probably make a button class
    
    def display_menu():
        font = pygame.font.SysFont('m5x7', 70)
        screen.fill(WHITE)
        draw_text('Main Menu', font , BLACK, screen,screen)

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
                    exit_game = False
                    level = 1
                    while not exit_game:
                        (exit_game, level_reached) = main_loop(screen, clock, tile_size, numrows, numcols, key_count, map_factor, level, enemy_count, life_count)
                        if level_reached:
                            game_over_menu(level_reached)
                        else:
                            level = level + 1
                    display_menu()
                    
                if button_2.isOver(pos):
                    options_menu()   
                    display_menu()
                
                if button_3.isOver(pos):
                    difficulty_menu()
                    display_menu()
            
        pygame.display.update()
        clock.tick(60)
        

pygame.init()
main_menu()
pygame.quit()
