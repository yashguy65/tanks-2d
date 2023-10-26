import pygame
import gamemenu
from constants import *
import spritesheetHandler
import game_sprites
#beautifulsoup4-4.12.2 soupsieve-2.5 mysql.connector-2.2.9 pygame-2.5.1
pygame.init()

# Set up the window
resizablesurface = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
imageSprite = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(imageSprite)
screen = resizablesurface.copy()
pygame.display.set_caption("Tanks!")
clock  = pygame.time.Clock()

#load sprite with img, dimensions

def load_tanks():
    ss = spritesheetHandler.SpriteSheet("sheet_tanks.png")
    spritelist = ss.loadXML()
    assets = {}
    for i in spritelist.keys:
        if 'tank' in i and 'outline' in i:
            key = i.replace(".png", "")
            assets[key] = spritelist[i]
    return assets

sprites = load_tanks()

#player = Tank(tanksprite, playerx, playery, playerw, playerh, sprites["bulletBlue"] )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #player.fire()
            pass

    # Update game state

    # Draw the screen
    pygame.display.update()
    pygame.event.pump()
    clock.tick(60)

# Clean up
pygame.quit()
