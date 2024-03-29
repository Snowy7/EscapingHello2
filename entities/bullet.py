import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, dir, entities_sprites):
        super().__init__(groups)
        
        self.entities_sprites = entities_sprites
        
        # line
        self.og_pos = pos
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 225, 0))
        
        self.born = pygame.time.get_ticks()
        self.lifeTime = 1000
        
        self.order = 11
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = dir
        
    def update(self):
        # increase bullet width over time
        self.image = pygame.transform.scale(self.image, (self.rect.width + 50, self.rect.height))
        
        
        self.rect.x += self.direction.x * 50
        self.rect.y += self.direction.y * 50
        
        if pygame.time.get_ticks() - self.born > self.lifeTime:
            self.kill()
            
        # check for collision
        hits = pygame.sprite.spritecollide(self, self.entities_sprites, False)
        for hit in hits:
            if hit != self:
                hit.TakeDamage(10)
                self.kill()