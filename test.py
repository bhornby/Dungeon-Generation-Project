import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)

YELLOW = (255,255,0)
#black screen
size = (1000,720)

# width of each tile
width = 40
height = 40

screen = pygame.display.set_mode(size)

#exit game falg set to false
done = False

#screen refresh rate
clock = pygame.time.Clock()

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
        for i in range(len(map)):
            for j in range(len(map[i])):
                if j == 0:
                    self.rect.x,self.rect.y  = x,y
            
                
        
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

class Wall(pygame.sprite.Sprite):
    def __init__(self,colour,width,height,x,y):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
all_sprite_group = pygame.sprite.Group()

wall_group = pygame.sprite.Group()

wall_count = 100
numcols = 24
numrows = 24
# make it so limited number of walls so that there will always be a route. so there needs to be counter that loses one each time a wall is drawn
# rule that for a wall to be generated the previous free space must have at least one other free space connected
# create the grid and make the path first set values to 1 the create the map so its not touching the path.
while wall_count >= 0:
    map = [[random.randint(0,1) for i  in range(numcols)]for j in range(numrows)]
    wall_count = wall_count-1
    '''for i in range(len(map)):
        for j in range(len(map[i])):
            if j == 1:s
                next '''
            
            
                
    
# next i
print(map)


x = 0
y = 0
    

for row in map:
    for column in row:
        if column == 1:
#             a wall is drawn if the value in the array is = to 1
            my_wall = Wall(WHITE,width,height,x,y)
            all_sprite_group.add(my_wall)
            wall_group.add(my_wall)
        x = x + 40
        #end if
    #next column 
    x = 0
    y = y + 40
#next row

my_player = Player(YELLOW,20,20,5)
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