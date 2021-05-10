import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)

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

numcols = 25
numrows = 25
map = [[random.randint(0,1) for i  in range(numcols)]for j in range(numrows)]
print(map)

x = 0
y = 0
    

for row in map:
    for column in row:
        if column == 1:
            my_wall = Wall(WHITE,width,height,x,y)
            all_sprite_group.add(my_wall)
            wall_group.add(my_wall)
        x = x + 40
        #end if
    #next column
    x = 0
    y = y + 40
#next row



pygame.init()
#game loop
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
pygame.quit()