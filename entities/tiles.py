import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, groups, layer = 2):
        super().__init__(groups)
        
        # load the image, convert to alpha
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale the image to the tilesize defined in settings
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        # get the rectangle of the image and set the topleft to the pos
        self.rect = self.image.get_rect(topleft = pos)
        
        self.hitbox = self.rect.inflate(0, -10)
        
        self.order = layer

class Interactable(Tile):
    def __init__(self, image_path, pos, groups):
        super().__init__(image_path, pos, groups)
        self.canInteract = True

    def interact(self):
        print("Interacted")
    
class Ground(Tile):
    def __init__(self, pos, groups):
        super().__init__("./assets/images/floor_plain.png", pos, groups, layer = 1)

class Wall2(Tile):
    def __init__(self, pos, groups):
        sprites = [
            "Wall_missing_brick_1",
            "Wall_missing_brick_2",
            "Wall_gratings",
            "Wall_pipe_1",
            "Wall_pipe_2",
            "Wall_goo"
        ]
        
        wallSprite = sprites[pygame.time.get_ticks() % len(sprites)]
        
        super().__init__("./assets/images/" + wallSprite + ".png", pos, groups)

class Wall():
    # a wall has three parts: start middle end
    def __init__(self, pos, groups):
        # draw three parts of the wall
        stain_images = [
            "./assets/images/floor_stain_1.png",
            "./assets/images/floor_stain_2.png",
            "./assets/images/floor_stain_3.png"
        ]
        center = Tile("./assets/images/wall_center.png", pos, groups)
        top = Tile("./assets/images/Wall_top_center.png", (pos[0], pos[1] - TILESIZE), [groups[0]])
        stain = Tile(stain_images[pygame.time.get_ticks() % len(stain_images)], (pos[0], pos[1] + TILESIZE), [groups[0]])

class TestInteractable(Interactable):
    def __init__(self, pos, groups):
        super().__init__("./assets/images/skull.png", pos, groups)

class BaseChest(Interactable):
    def __init__(self, pos, groups, closed_img, opened_img):
        super().__init__(closed_img, pos, groups)
        self.opened_img = opened_img
        
    def interact(self):
        print("Chest opened")
        self.image = pygame.image.load(self.opened_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        self.hitbox = self.rect.inflate(0, -10)
        
        self.canInteract = False


class Chest(BaseChest):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, "./assets/images/chest_closed.png", "./assets/images/chest_open_empty.png")

class GoldenChest(BaseChest):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, "./assets/images/chest_golden_closed.png", "./assets/images/chest_golden_open_full.png")
        