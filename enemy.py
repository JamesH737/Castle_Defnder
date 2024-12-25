import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #select starting image
        self.image = self.animation_list[self.action]

