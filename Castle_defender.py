# import libraries
import pygame
import math

#initializes pygame 
pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender')

clock = pygame.time.Clock()
FPS = 60


# load images 
bg = pygame.image.load('img/bg.png').convert_alpha()
castle_image_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()

#bullet image
bullet_img = pygame.image.load('img/bullet.png')
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

#load enemies 

enemy_animations = []
enemy_types = ['knight']
enemy_health = [75]

animation_types = ['walk', 'attack', 'death']

for enemy in enemy_types:
    # load animation
    animation_list = []
    for animation in animation_types:
        #reset temporary list of images 
        temp_list = []
        #define number of frames
        num_of_frames = 20
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

#define coloours
WHITE = (255, 255, 255)

class Castle():
    def __init__(self, image100, x, y, scale):
        self.health = 1000
        self.max_health = self.health

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale))) 
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = - (pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        #get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)    
        #rest mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False    

    def draw(self):
        self.image = self.image100
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):

        pygame.sprite.Sprite.__init__(self)
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10
        # calculate the horizonal and vertical speed based on angles 
        self.dx = math.cos(self.angle) * self.speed
        self.dy = - (math.sin(self.angle) * self.speed)

    def update(self):
        # check if bullet has gone off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        #move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy


#create castle 
castle = Castle(castle_image_100, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# create bullet group
bullet_group = pygame.sprite.Group()

#game loop
run = True
while run:

    clock.tick(FPS)
    screen.blit(bg, (0, 0))

    #draw castle
    castle.draw()
    castle.shoot()

    #draw bullets
    bullet_group.update()
    bullet_group.draw(screen)

    #event handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update the display window
    pygame.display.update()

pygame.quit()            