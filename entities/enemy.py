from spritesheet import *
import pygame
from settings import *
from level import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)

        self.image = pygame.image.load("./assets/images/monster_zombie_tall.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = self.rect
        self.groundHitbox = self.hitbox 
        self.groundHitbox.y += 1

