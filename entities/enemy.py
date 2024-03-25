from spritesheet import *
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__ (self, pos, groups, level, obstacle_sprites, interactable_sprites):
        super().__init__(groups)
        self.level = level
        
        self.anim_wake = SpriteSheet(pygame.image.load("./assets/player/wake.png").convert_alpha())
        self.idle = self.anim_wake.get_image(4, 26, 24, 2)
        
        self.image = self.idle
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        
        # add a weapon
        self.weapon = pygame.image.load('./assets/images/rifle.png').convert_alpha()
        self.weapon = pygame.transform.scale(self.weapon, (TILESIZE, TILESIZE))
        self.weaponRect = self.weapon.get_rect(topleft = pos)
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.groundHitbox = self.hitbox 
        self.groundHitbox.y += 1

        self.direction = pygame.math.Vector2()
        self.shootingDirection = pygame.math.Vector2()
        self.speed = 15

        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites = interactable_sprites
        
        self.lastInteracted = None
        self.didPressE = False
        self.isGrounded = False
        self.lookDir = 0
        self.order = 10
        self.isJumping = False
        self.mouse_click = False
        self.m = 1
        self.v = 15

    def input(self):
        # enemy AI
        
        pass
            
    def gravity(self):
        #if not self.isJumping:
        if self.isGrounded:
            self.direction.y = GRAVITY
        if not self.isJumping:
            self.direction.y += GRAVITY
        
    def jump(self, y):
        if self.isJumping:
            k = .5*self.m*self.v**1.9          
            y -= k
            self.v -= 1
            
            if self.v < 0:
                self.m -=1
                
            if self.v == -1:
                self.m = 1
                self.v = 15
                self.isJumping = False
            
        return y  
        
    def checkGrounded(self):
        grounded = False
        
        for sprite in self.obstacle_sprites:
            if sprite.rect.collidepoint(self.rect.centerx, self.rect.bottom+4):
                grounded = True
                break
                
        self.isGrounded = grounded

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.checkGrounded()
        self.gravity()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y = self.direction.y * speed + self.jump(self.hitbox.y)
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
        # inverse image if moving left
        if self.direction.x < 0 and self.lookDir == 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lookDir = 1
        elif self.direction.x > 0 and self.lookDir == 1:                
                self.image = pygame.transform.flip(self.image, True, False)
                self.lookDir = 0

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0 or self.isJumping:
                        self.hitbox.top = sprite.hitbox.bottom                  
                        
    def update(self):
        self.input()
        self.move(self.speed)
         
        # rotate weapon
        #angle = math.degrees(math.atan2(self.shootingDirection.y, self.shootingDirection.x))
        #self.weapon = pygame.transform.rotate(self.weapon, angle)
        
    def displayWeapon(self, surf, pos, angle):

        rotated_image = pygame.transform.rotate(self.weapon, angle)
        new_rect = rotated_image.get_rect(center = self.weapon.get_rect(topleft = pos).center)

        surf.blit(rotated_image, new_rect)
