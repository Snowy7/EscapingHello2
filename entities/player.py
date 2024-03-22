import math
import pygame
from settings import *
from entities.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__ (self, pos, groups, level, obstacle_sprites, interactable_sprites):
        super().__init__(groups)
        self.level = level
        self.image = pygame.image.load('./assets/images/hero_basic.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.groundHitbox = self.hitbox 
        self.groundHitbox.y += 1

        self.direction = pygame.math.Vector2()
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
        self.v = 10

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            #self.direction.y = -1
           if self.isGrounded: 
               self.isJumping = True

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        # on Mouse Click
        if pygame.mouse.get_pressed()[0]:
            if self.mouse_click:
                return 
            self.mouse_click = True
            mouse_pos = pygame.mouse.get_pos()
            # player always on the center of the screen
            mx = mouse_pos[0] - WIDTH // 2
            my = mouse_pos[1] - HEIGHT // 2
            dirction = pygame.math.Vector2(mx, my)
            self.level.spawn_bullet(self.rect.center, dirction.normalize())
            
        else:
            self.mouse_click = False
            
    def gravity(self):
        #if not self.isJumping:
        if not self.isJumping:
            self.direction.y += GRAVITY
        
    def jump(self, y):
        if self.isJumping:
            k = .5*self.m*self.v**2
            y -= k
            self.v -= 1
            
            if self.v < 0:
                self.m -=1
                
            if self.v == -5:
                self.m = 1
                self.v = 10
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
        self.Interact()

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
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def Interact(self):
        isInteracting = False
        targetSprite = None
        for sprite in self.interactable_sprites:
            if sprite.hitbox.colliderect(self.hitbox) and sprite.canInteract:
                isInteracting = True
                targetSprite = sprite
                break
            
        if isInteracting:
            # Draw "Press E to interact" on the screen
            wind = pygame.display.get_surface()
            font = pygame.font.Font(None, 36)
            text = font.render("Press E to interact", True, 'white')
            wind.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
            # Check if E is down only once NOT HOLDING
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if not self.didPressE:
                    targetSprite.interact()
                    self.lastInteracted = targetSprite
                    self.didPressE = True
            else:
                self.didPressE = False
                
    def disableGravityFor(self, time = 0.5):
        self.gravityDisabled = True
        
            
    def update(self):
         self.input()
         self.move(self.speed)