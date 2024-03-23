import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Main Menu')

# Fonts
font = pygame.font.Font(None, 40)
menu_items = ['Start Game', 'Options', 'Quit']
selected_item = 0

def draw_menu():
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        text = font.render(item, True, WHITE if index == selected_item else RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 50))
        screen.blit(text, text_rect)

def start_game():
    print('Starting game...')
    
    # Initialize game variables
    player_x = WIDTH // 2
    player_y = HEIGHT - 50
    player_speed = 5
    obstacle_speed = 3
    obstacles = []

    # Game loop
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Spawn obstacles
        if len(obstacles) < 5:  # Limit the number of obstacles on the screen
            obstacle = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)
            obstacles.append(obstacle)

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:  # Remove obstacles that are off-screen
                obstacles.remove(obstacle)

            # Check for collision with player
            if obstacle.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                game_over()

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (player_x, player_y, 50, 50))  # Draw player
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, obstacle)  # Draw obstacles

        pygame.display.flip()
        clock.tick(FPS)

def game_over():
    print('Game over!')
    
    # Reset game variables
    player_x = WIDTH // 2
    player_y = HEIGHT - 50
    player_speed = 5
    obstacle_speed = 3
    obstacles = []

    # Game over screen
    game_over_font = pygame.font.Font(None, 60)
    game_over_text = game_over_font.render('Game Over', True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Display game over screen
    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    # Wait for a few seconds before restarting the game
    pygame.time.wait(2000)  # 2000 milliseconds = 2 seconds

    # Restart the game
    start_game()



# Main Menu Loop
clock = pygame.time.Clock()
menu_running = True
game_running = False
while menu_running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_running = False
                break
            elif event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:
                    start_game()
                    game_running = True
                    menu_running = False
                elif selected_item == 1:
                    print('Options menu')
                elif selected_item == 2:
                    pygame.quit()
                    sys.exit()

    draw_menu()
    pygame.display.flip()

# Game Loop (if game started from main menu)
if game_running:
    while game_running:
        # Add your game loop code here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Quit Pygame
pygame.quit()
sys.exit()
