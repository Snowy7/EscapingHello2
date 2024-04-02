from entities.bullet import Bullet
from entities.player import AnimatedSprite
from spritesheet import *
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__ (self, pos, groups, level, obstacle_sprites):
        super().__init__(groups)
        self.visible_sprites = groups[0]
        self.level = level
        
        self.entities_sprites = groups[1]
        self.isAlive = True
        self.health = 100
        
        self.anim_wake = SpriteSheet(pygame.image.load("./assets/player/e_wake.png"))
        
        self.idle = self.anim_wake.get_image(4, (8, 0), (30, 26), 2)
        
        self.walk = AnimatedSprite("./assets/player/e_move with FX.png", (0, 0), (42, 26), 2, 8)
        
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
        self.range = TILESIZE * 5
        self.attackRange = TILESIZE * 2
        # How many bullets per second
        self.fireRate = 1
        self.lastShot = pygame.time.get_ticks()

        self.obstacle_sprites = obstacle_sprites
        
        self.isGrounded = False
        self.lookDir = 1
        self.order = 10
        self.isJumping = False
        self.mouse_click = False
        self.m = 1
        self.v = 15
        self.isMoving = False

    def input(self):
        self.direction.x = 0
        
        # move twoards the player if the player is in range
        distance = self.rect.centerx - self.level.player.rect.centerx
        if abs(distance) < self.range and abs(distance) > self.attackRange:
            if distance > 0:
                self.direction.x = -1
            else:
                self.direction.x = 1
            self.isMoving = True
        else:
            self.isMoving = False
                            
        if abs(distance) < self.attackRange and pygame.time.get_ticks() - self.lastShot > 1000 / self.fireRate:
            if distance > 0:
                self.shootingDirection = pygame.math.Vector2(-1, 0)
            else:
                self.shootingDirection = pygame.math.Vector2(1, 0)
            self.shoot()
            
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
        
        self.lastShot = pygame.time.get_ticks()
        Bullet(pos, [self.visible_sprites], self.shootingDirection, self.entities_sprites)
        
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

        self.lastX = self.hitbox.x
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.checkFall(self.lastX)
        
        self.hitbox.y = self.direction.y * speed + self.jump(self.hitbox.y)
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
    def checkFall(self, prevX):
        self.checkGrounded()
        if not self.isGrounded:
            # move back to the ground
            self.hitbox.x = prevX
            
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, "canCollide") and not sprite.canCollide:
                        continue
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, "canCollide") and not sprite.canCollide:
                        continue
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0 or self.isJumping:
                        self.hitbox.top = sprite.hitbox.bottom 
    def TakeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    
    def die(self):
        self.isAlive = False
        self.kill()
         
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
                    