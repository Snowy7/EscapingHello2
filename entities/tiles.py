# pygame is a library that makes it easier to make games in python
# it has a lot of built in functions that make it easier to make games
import pygame
from settings import *

# This is the base class for most of the tiles/sprites in the environment of the game.
# inherits from pygame.sprite.Sprite
# all other tiles inherit thier logic from this class
class Tile(pygame.sprite.Sprite):
    # it takes the image path, the position, the groups and the layer
    def __init__(self, image_path, pos, groups, layer = 2):
        super().__init__(groups)
        
        # (r, g, b, a) = (0, 0, 0, 0)
        # a => transparency, opacity, alpha, 1 is opaque, 0 is transparent
        # 255 is the maximum value for a color
        # 255 is white, 0 is black
        # 255 is obaque and 0 is transparent
        # loads the image, convert to alpha meaning it has transparency
        # from pygame grap the image (module)
        # the image module it controls the loading of images and saving of images
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale the image to the tilesize defined in settings
        # from pygame we grap transform (module)
        # the transform module it controls the scale, rotate, flip, etc of the image
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        
        # get the rectangle of the image and set the topleft to the pos.
        # the rect is the rectangle that the image is in.
        # the sprite class has a rect attribute => get_rect() method.
        self.rect = self.image.get_rect(topleft = pos)
        
        # now we create a hitbox for the tile
        # the hitbox is the area that the player can collide with
        # the hitbox is a rectangle that is a little bit smaller than the image on the y-axis
        # why? for the 3d effect and better gameplay (forgiving hitboxes)
        self.hitbox = self.rect.inflate(0, -10)
        
        # this one is for the player to collide with the tile
        # if true, the player will be able to collide with the tile
        # if false, the player will not be able to collide with the tile
        self.canCollide = True
        
        # this is the order of which the tile will be drawn
        self.order = layer
    

# This is the base class for most of the interactable tiles/sprites in the environment of the game.
# inherits from Tile class
# all other interactable tiles inherit thier logic from this class
class TileInteractable(Tile):
    def __init__(self, image_path, pos, groups):
        # super() is used to call the parent class constructor
        # in this case it calls the constructor of the Tile class.
        # we are passing the image_path, pos and groups to the Tile class
        super().__init__(image_path, pos, groups)
        
        # this is similar to self.canCollider
        # if true, the player will be able to interact with the tile
        # if false, the player will not be able to interact with the tile
        self.canInteract = True

        # this is the area that the player can interact with the tile
        # it is a rectangle that is a little bit bigger than the hitbox
        # this is for the player to know that they can interact with the tile
        self.interactBox = self.hitbox.inflate(40, 40)
        
        # this is the message that will be displayed to the player when they can interact with the tile
        self.msg = "Press [E] to interact!"

    # the function that will be called when the player interacts with the tile
    def interact(self):
        print("Interacted")

# THE SIMPLEST EXAMPLE OF A TILE
# THIS IS A GROUND TILE
class Ground(Tile):
    # it takes the pos, and the groups
    def __init__(self, pos, groups):
        # it calls the constructor of the Tile class, with the ground image path, and the given pos and groups
        super().__init__("./assets/images/floor_plain.png", pos, groups, layer = 1)

class Wall():
    # A wall contains two tiles, a center tile, a top shade tile
    def __init__(self, pos, groups):
        self.center = Tile("./assets/images/wall_center.png", pos, groups)
        # the top part pos is the same as the center pos but the y is -TILESIZE
        # - means up, + means down
        self.top = Tile("./assets/images/Wall_top_center.png", (pos[0], pos[1] - TILESIZE), groups)
        # we disable the collision for the top part
        self.top.canCollide = False

# THE SIMPLEST EXAMPLE OF AN INTERACTABLE TILE
# THIS IS A TEST INTERACTABLE TILE
class TestInteractable(TileInteractable):
    # it takes the pos, and the groups
    def __init__(self, pos, groups):
        # it calls the constructor of the TileInteractable class, with the test interactable image path, and the given pos and groups
        super().__init__("./assets/images/skull.png", pos, groups)

class BaseChest(TileInteractable):
    def __init__(self, pos, groups, closed_img, opened_img, func = None):
        super().__init__(closed_img, pos, groups)
        self.opened_img = opened_img
        # This is the function that will be called when the chest is interacted with
        # it can do logic outside of the class
        self.func = func
        self.order = 20
        
    def interact(self):
        print("Chest opened")
        self.image = pygame.image.load(self.opened_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        self.hitbox = self.rect.inflate(0, -10)
        
        self.canInteract = False
        if self.func is not None: self.func()

class Chest(BaseChest):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, "./assets/images/chest_closed.png", "./assets/images/chest_open_empty.png")

class GoldenChest(BaseChest):
    def __init__(self, pos, groups, func = None):
        super().__init__(pos, groups, "./assets/images/chest_golden_closed.png", "./assets/images/chest_golden_open_full.png", func=func)

class LeftWall():
    # a wall has three parts: start middle end
    def __init__(self, pos, groups):
        # draw three parts of the wall
        center = Tile("./assets/images/Wall_outer_w2.png", pos, groups)
        # make it so it is 10px on width
        center.hitbox = center.rect.inflate(-TILESIZE + 10, 0)
        # move the hitbox to the right
        center.hitbox.move_ip(10, 0)
    
class RightWall():
    # a wall has three parts: start middle end
    def __init__(self, pos, groups):
        # draw three parts of the wall
        center = Tile("./assets/images/Wall_outer_e2.png", pos, groups)
        # make it so it is 10px on width
        center.hitbox = center.rect.inflate(-TILESIZE + 10, 0)
        # move the hitbox to the left
        center.hitbox.move_ip(-10, 0)
        
class CenterWall(Tile):
    # a wall has three parts: start middle end
    def __init__(self, pos, groups):
        super().__init__("./assets/images/wall_center.png", pos, groups)

class BaseDoor(TileInteractable):
    def __init__(self, pos, groups, closed_img, opened_img, canBeInteracted = False):
        super().__init__(closed_img, pos, groups)
        self.opened_img = opened_img
        self.closed_img = closed_img

        # scaling the image
        # because the door sprite is wierd
        self.image = pygame.transform.scale(self.image, size=(TILESIZE*2.5, TILESIZE*2))
        # because the door sprite is flipped
        self.image = pygame.transform.flip(self.image, True, False)
        
        # fixing position, because the door sprite is wierd
        # for y => - is up, + is down
        # for x => - is left, + is right
        self.rect.topleft = (pos[0] - TILESIZE*1.9, pos[1] - TILESIZE)
        
        self.func = None
        self.pos = pos
        self.canBeInteracted = canBeInteracted

        self.order = 20
        
        # if the door can open or nah!
        self.canOpen = False
        
    def interact(self):
        # You are not allowed to open the door.
        if not self.canOpen:
            print(self.msg)
            return
        
        self.Open()
        pass 
    
    def Open(self):
        self.image = pygame.image.load(self.opened_img).convert_alpha()
        # flip
        self.image = pygame.transform.scale(self.image, size=(TILESIZE*2.5, TILESIZE*2))
        self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect.topleft = (self.pos[0] - TILESIZE*1.9, self.pos[1] - TILESIZE)
        
        self.canInteract = False    
        self.canCollide = False
        
        if self.func is not None: self.func()
        
        # play open sound
        #if self.audio_manager is not None: self.audio_manager.queue(self.open_sound, True)
    
    def Close(self):
        self.image = pygame.image.load(self.closed_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, size=(TILESIZE*2.5, TILESIZE*2))
        self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect.topleft = (self.pos[0] - TILESIZE*1.9, self.pos[1] - TILESIZE)
        
        self.canInteract = True
        self.canCollide = True 
        
        #if self.audio_manager is not None: self.audio_manager.queue(self.close_sound, True)

class Door(BaseDoor):
    def __init__(self, pos, groups, audio_manager = None):
        super().__init__(pos, groups, "./assets/images/side_door.png", "./assets/images/side_door_open.png")
        self.msg = "The door is locked"
