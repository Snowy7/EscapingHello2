import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, dir):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/images/weapon_bomb.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE / 2, TILESIZE / 2))
        self.order = 11
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = dir
        
    def update(self):
        
        self.rect.x += self.direction.x * 50
        self.rect.y += self.direction.y * 50
        
        
        
        #self.rect.x += self.direction.x * 10
        #self.rect.y += self.direction.y * 10