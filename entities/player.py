from entities.bullet import Bullet
from spritesheet import *
import pygame
from settings import *

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, path, offset, w_h, scale, framesCount):
        super().__init__()
        
        self.anim = SpriteSheet(pygame.image.load(path))
        self.frames = [
            self.anim.get_image(i, offset, w_h, scale) for i in range(framesCount)
        ]
        self.image = self.frames[0]
        self.current_frame = 0
        self.last_update = 0
        self.frame_rate = 60
    
    def animate(self, dir):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            
            if dir == 0:
                self.image = pygame.transform.flip(self.image, True, False)
        

class Player(pygame.sprite.Sprite):
    def __init__ (self, pos, groups, level, obstacle_sprites, interactable_sprites):
        super().__init__(groups)
        self.visible_sprites = groups[0]
        self.level = level
        
        self.anim_wake = SpriteSheet(pygame.image.load("./assets/player/wake.png"))
        
        self.idle = self.anim_wake.get_image(4, (8, 0), (30, 26), 2)
        
        self.walk = AnimatedSprite("./assets/player/move with FX.png", (0, 0), (42, 26), 2, 8)
        
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
        self.lookDir = 1
        self.order = 10
        self.isJumping = False
        self.mouse_click = False
        self.m = 1
        self.v = 15
        self.isMoving = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            #self.direction.y = -1
           if self.isGrounded: 
               self.isJumping = True

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        self.isMoving = self.direction.x != 0
        
        # set the shooting direction depending on where the player is looking
        if self.lookDir == 0:
            self.shootingDirection = pygame.math.Vector2(-1, 0)
        elif self.lookDir == 1:
            self.shootingDirection = pygame.math.Vector2(1, 0)
        
        # on Mouse Click
        if pygame.mouse.get_pressed()[0]:
            if self.mouse_click:
                return 
            self.mouse_click = True
            self.shoot()
            
        else:
            self.mouse_click = False
            
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
        
    def shoot(self):
        # bullet pos is the player pos + some offset to the right or left depending on the direction
        pos = (self.rect.left, self.rect.centery - 5)
        if self.lookDir == 0:
            pos = (self.rect.left - (TILESIZE/2 - 20), self.rect.centery - 5)
        else:
            pos = (self.rect.left + TILESIZE, self.rect.centery - 5)
        Bullet(pos, [self.visible_sprites], self.shootingDirection)
        
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
                    if self.direction.y < 0 or self.isJumping:
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
        
        if self.isMoving:
            self.walk.animate(self.lookDir)
            self.image = self.walk.image
        else:
            self.image = self.idle
            if self.lookDir == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            
            
        # inverse image if moving left
        # print(self.direction.x, self.lookDir)
        if self.direction.x < 0 and self.lookDir == 1:
            #self.image = pygame.transform.flip(self.image, True, False)
            self.lookDir = 0
        elif self.direction.x > 0 and self.lookDir == 0:                
            #self.image = pygame.transform.flip(self.image, True, False)
            self.lookDir = 1
        
