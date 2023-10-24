import pygame
from game_sprites import *
#beautifulsoup4-4.12.2 soupsieve-2.5 mysql.connector-2.2.9 pygame-2.5.1
pygame.init()

# Set up the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tanks")
player = Tank(tanksprite, playerx, playery, playerw, playerh, tankvelc, bulletSprite )
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire()

    # Update game state

    # Draw the screen
    screen.fill((255, 255, 255))
    pygame.display.flip()

# Clean up
pygame.quit()
