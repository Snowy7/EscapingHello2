import sys
import pygame
from entities.bullet import Bullet
from settings import *
from entities.tiles import CenterWall, Door, Ground, LeftWall, RightWall, Wall, TestInteractable, Chest, GoldenChest
from entities.player import Player
from entities.enemy import Enemy

# This will handle the level of the game
class Level:
    def __init__(self):
        
        # 0 => MainMenu
        # 1 => Game
        # 2 => GameOver
        # 3 => Win
        self.gameState = 0
        
        # main menu selected item
        self.mainMenuSelectedItem = 0
        
        # get the display surface 
        # the frames will be drawn on this surface
        self.display_surface = pygame.display.get_surface()
    

        # sprite group set up
        # the obstacle sprites are the sprites that the player can't pass through
        self.obstacle_sprites = pygame.sprite.Group()
        # the player can interact with these sprites
        self.interactable_sprites = pygame.sprite.Group()
        # the background sprites are the sprites that are drawn in the background
        self.background_sprites = pygame.sprite.Group()
        # the entities sprites are the enemies and the player
        self.entities_sprites = pygame.sprite.Group()
        # this is just all the sprites that are visible
        self.visible_sprites = YSortCameraGroup()
        
        self.done = False
        self.door = False

        # sprite set up
        #self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                if col == 'w' or col == "." or col == "s" or col == "e" or col == "x":
                    Wall((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == "dr":
                    self.door = Door((x, y), [self.visible_sprites, self.interactable_sprites, self.obstacle_sprites])
                if col == "lw":
                    LeftWall((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == "rw":
                    RightWall((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == "cw":
                    CenterWall((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites, self.entities_sprites], self, self.obstacle_sprites, self.interactable_sprites)
                if col == "t":
                    TestInteractable((x, y), [self.visible_sprites, self.interactable_sprites])
                if col == "c":
                    Chest((x, y), [self.visible_sprites, self.interactable_sprites])
                if col == "gc":
                    GoldenChest((x, y), [self.visible_sprites, self.interactable_sprites], self.gold_chest)
                if col == 'g':
                    Ground((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'z':
                    self.enemy = Enemy((x, y), [self.visible_sprites, self.entities_sprites], self, self.obstacle_sprites)
                
    def gold_chest(self):
        if self.door != False:
            self.door.msg = "Press 'E' to open the door"
            self.door.canOpen = True
            self.door.func = self.finish
            
    def finish(self):
        self.gameState = 3
        
    def get_player(self):
        return self.player

    def spawn_bullet(self, pos, dir):
        Bullet(pos, [self.visible_sprites], dir)
    
    def run(self, events):
        if self.gameState == 0:
            self.MainMenu(events)
        elif self.gameState == 1:
            self.Game()
        elif self.gameState == 2:
            self.GameOver()
        elif self.gameState == 3:
            self.GameWin()
        
    def MainMenu(self, events):
        menu_items = ['Start Game', 'Quit']
        
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
                        pygame.quit()
                        sys.exit()
                
        
        # This is drawing the main menu
        # Here we define the font and the size of the text
        # Font module is used to render text on the screen
        font = pygame.font.Font(None, 40)
        for index, item in enumerate(menu_items):
            text = font.render(item, True, (255, 0, 0) if index == self.mainMenuSelectedItem else (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 50))
            
            # this is drawing the text on the screen
            self.display_surface.blit(text, text_rect)
    
    def StartGame(self):
        self.create_map()
        self.gameState = 1
    
    def Game(self):
        # update and draw game
        self.visible_sprites.custom_draw(self.player, self.entities_sprites)
        #self.visible_sprites.custom_draw_z(self.enemy)
        self.visible_sprites.update()
        
        if not self.player.isAlive:
            self.gameState = 2
        
    def GameOver(self):
        print('Game over!')

        # Game over screen
        game_over_font = pygame.font.Font(None, 60)
        game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Display game over screen
        self.display_surface.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        # Wait for a few seconds before restarting the game
        pygame.time.wait(2000)  # 2000 milliseconds = 2 seconds

        # Restart the game
        self.done = True
        
    def GameWin(self):
        print('You win!')

        # Game win screen
        game_win_font = pygame.font.Font(None, 60)
        game_win_text = game_win_font.render('You win!', True, (0, 255, 0))
        game_win_rect = game_win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Display game win screen
        self.display_surface.blit(game_win_text, game_win_rect)
        pygame.display.flip()

        # Wait for a few seconds before restarting the game
        pygame.time.wait(2000)
        
        self.done = True

zombie_group = pygame.sprite.Group()           

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, entities_sprites):
        if player is None:
            return
        
        # getting the offset
        # this is the offset of the player from the center of the screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # this is the list of sprites that will be drawn
        # this list contains tuples (... , ...)
        # the first element is the sprite
        # the second element is the offset of the sprite from the player offset
        sprites_to_draw = []

        # this sorts the sprites using the y coordinate
        for sprite in self.sprites():
            offset_post = sprite.rect.topleft - self.offset
            sprites_to_draw.append((sprite, offset_post))
            
        # this sorts the sprites using the order attribute
        # the lower the order, the lower the sprite is drawn
        # the higher ones are in the front
        sprites_to_draw.sort(key = lambda sprite: sprite[0].order)
        
        for sprite, offset_post in sprites_to_draw:
            sprite.image.set_colorkey((0, 0, 0))
            self.display_surface.blit(sprite.image, offset_post)
        
            
        for sprite in entities_sprites:
            # health bar
            pygame.draw.rect(self.display_surface, (255, 0, 0), (sprite.rect.x - self.offset.x, sprite.rect.y - self.offset.y - 10, TILESIZE, 5))
            pygame.draw.rect(self.display_surface, (0, 255, 0), (sprite.rect.x - self.offset.x, sprite.rect.y - self.offset.y - 10, TILESIZE * sprite.health / 100, 5))