import math
import sys
import pygame
from entities.bullet import Bullet
from settings import *
from entities.tiles import Ground, Wall, TestInteractable, Chest, GoldenChest
from entities.player import Player

class Level:
    def __init__(self):
        
        # 0 => MainMenu
        # 1 => Game
        # 2 => GameOver
        # 3 => Win
        # 4 => Pause
        self.gameState = 0
        
        self.mainMenuSelectedItem = 0
        
        # get the display surface 
        self.display_surface = pygame.display.get_surface()
    

        # sprite group set up
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        # sprite set up
        #self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                if col == 'w':
                    Wall((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self, self.obstacle_sprites, self.interactable_sprites)
                if col == "t":
                    TestInteractable((x, y), [self.visible_sprites, self.interactable_sprites])
                if col == "c":
                    Chest((x, y), [self.visible_sprites, self.interactable_sprites])
                if col == "g":
                    GoldenChest((x, y), [self.visible_sprites, self.interactable_sprites])
                    
    def spawn_bullet(self, pos, dir):
        Bullet(pos, [self.visible_sprites], dir)
    def run(self, events):
        if self.gameState == 0:
            self.MainMenu(events)
        elif self.gameState == 1:
            self.Game()
        elif self.gameState == 2:
            pass
        #etc..
        
    def MainMenu(self, events):
        menu_items = ['Start Game', 'Options', 'Quit']
        
        # input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.mainMenuSelectedItem = (self.mainMenuSelectedItem - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    self.mainMenuSelectedItem = (self.mainMenuSelectedItem + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.mainMenuSelectedItem == 0:
                        self.StartGame()
                    elif self.mainMenuSelectedItem == 1:
                        print("Options yay!")
                    elif self.mainMenuSelectedItem == 2:
                        pygame.quit()
                        sys.exit()
                
        
        font = pygame.font.Font(None, 40)
        for index, item in enumerate(menu_items):
            text = font.render(item, True, (255, 0, 0) if index == self.mainMenuSelectedItem else (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 50))
            
            self.display_surface.blit(text, text_rect)
    
    def StartGame(self):
        self.create_map()
        self.gameState = 1
    
    def Game(self):
        # update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_with = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        if player is None:
            return
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_with
        self.offset.y = player.rect.centery - self.half_height
        
        sprites_to_draw = []
    
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_post = sprite.rect.topleft - self.offset
            sprites_to_draw.append((sprite, offset_post))
            
        # sort by the order
        sprites_to_draw.sort(key = lambda sprite: sprite[0].order)
        
        for sprite, offset_post in sprites_to_draw:
            self.display_surface.blit(sprite.image, offset_post)
            
        # draw player's weapon
        # ROTATE THE WEAPON
        
        angle = player.shootingDirection.angle_to(pygame.math.Vector2(1, 0))
        
        pos = (self.half_with - TILESIZE // 2) + 10, (self.half_height - TILESIZE // 2) + 10
        player.displayWeapon(self.display_surface, pos, angle)
        

            
        