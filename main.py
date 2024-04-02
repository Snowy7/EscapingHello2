import pygame, sys # importing the pygame and system libraries
from settings import * # importing the settings from the settings file
from level import Level # Level is the main class that will be running the game

# This is the main class that will be running the game
class Game:  
    def __init__(self):
        # Initialize the pygame library
        pygame.init()
        
        # We are setting the screen to the width and height defined in the settings
        # the display is a module in pygame that controls the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        # we are setting the title of the game to the GAME_TITLE defined in the settings
        pygame.display.set_caption(GAME_TITLE)
        
        # the clock is used to control the frames per second of the game
        self.clock = pygame.time.Clock()
        
        # we are creating a level object
        # this is where the whole logic of the game will be
        self.level = Level()
        
        # change cursor
        # setting it to invisible
        pygame.mouse.set_visible(False)
        # loading the cursor image
        self.cursor = pygame.image.load('./assets/images/aim.png').convert_alpha()
        # we are scaling the cursor to 32x32
        self.cursor = pygame.transform.scale(self.cursor, (32, 32))
        
        
    def run(self):
        # this is the main loop of the game
        # the try/except block is used to catch and ignore any errors that might occur
        try:
            # while True: to keep it running until the user quits
            while True:
                # hazard: this handles the game quit buttons (do not remove)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        # this to shutdown the game window
                        pygame.quit()
                        # this to shutdown the python program
                        sys.exit()

                # fill the screen with the color defined
                self.screen.fill('#1c1117') # rgb(28, 17, 23)
                # run the level logic
                self.level.run(events)

                # "RESTART"
                # here we check if the level is done
                # if it is done, we create a new level
                if self.level.done:
                    self.level = Level()

                # draw cursor
                # WE ARE DRAWING THE CURSOR LAST SO IT CAN BE ON TOP OF EVERYTHING
                # WE ARE DRAWING IT ON THE MOUSE POSITION
                self.screen.blit(self.cursor, pygame.mouse.get_pos())

                pygame.display.update()
                self.clock.tick(FPS)
        except:
            print("Something wrong happened, but wdc, we continue...")

if __name__ == '__main__':
    game = Game()
    game.run()