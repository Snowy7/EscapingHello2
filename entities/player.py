import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__ (self, pos, groups, obstacle_sprites, interactable_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/images/hero_basic.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites = interactable_sprites
        
        self.lastInteracted = None
        self.didPressE = False
        self.lookDir = 0
        self.order = 10

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
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
            
    def update(self):
         self.input()
         self.move(self.speed)