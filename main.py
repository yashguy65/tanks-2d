import pygame
from constants import *
screen = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
from gamemenu import *
from spritesheetHandler import *
from game_sprites import *
import time
pygame.init()

imageSprite = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(imageSprite)
pygame.display.set_caption("Tanks!")

clock  = pygame.time.Clock() 
bg_layer = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

for x in range(0, VIEW_WIDTH, SCALEX):
		for y in range(0, VIEW_HEIGHT, SCALEY):
			bg_layer.blit(spritelist["dirt"], (x, y))
   
   
tank_sprites = {}
for i in spritelist.keys():
    if 'tank' in i and 'outline' in i:
        key = (i.replace("_outline", "").replace("tank","")).lower()
        tank_sprites[key] = spritelist[i]


player = Tank("blue", 0, 0, True)

game_map, tanks = load_map(1, tanks)
peaceful = True
running = True

while running:
    
    shotsFired = 0
    bulletLimit = 6
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                else:
                    player.move(event.key)
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if shotsFired < bulletLimit:
                player.shoot()
                shotsFired += 1

                start_time = time.time()
                while running:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    
                    if elapsed_time >= 60:
                        peaceful = False
                        break
                    
                    for i in tanks:
                        if i.dead:
                            peaceful = False
                            break
                    else:
                        peaceful = True
                        
    for i in tanks:
        i.render(bg_layer)
        i.update(bg_layer)
        #if (not i.player) and peaceful:
           # i.beta_peaceful()
        
    for j in bullets:
        j.update(bg_layer)
        j.render(bg_layer)
        
    
    screen.blit(bg_layer, (0,0))
    pygame.display.flip()
    pygame.event.pump()
    #clock.tick(60)
