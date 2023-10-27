import pygame
from spritesheetHandler import *
from constants import *
from game_sprites import *
import mysql.connector

pygame.init()
pygame.font.init()

'''mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS game_scores")
mycursor.execute("USE game_scores")
mycursor.execute("CREATE TABLE IF NOT EXISTS scores (id INT AUTO_INCREMENT PRIMARY KEY, score INT)")'''

def print_text(text, fontsize, textcolor, bgcolor, isbold):
    
    font = pygame.freetype.SysFont("Consolas", fontsize, bold=isbold)
    surface, _ = font.render(text=text, fgcolor=textcolor, bgcolor=bgcolor)
    return surface.convert()

def play_game(screen):
    
    #SCORE = get_highscore()
    text1 = 'SCORE: ' + SCORE+', HIGHEST: '+str(max)+ ' Click to try again.'
    
    playagainbox = print_text(text1, 17, WHITE, None, False)
    againrect = playagainbox.get_rect(center = (screen.get_width()/2, screen.get_height()/2))
    screen.blit(playagainbox, againrect)

def newgame(screen):
    
    newgame_box = print_text('TANKS', 46, BLACK, None, True)
    helpmsg = print_text('ESC: exit| Arrow keys to move | F11: Fullscreen', 10, BLUE, None, False)
    presskeymsg = print_text('PRESS ANY KEY TO START', 9, RED, None, True)
    wt, ht = screen.get_width(), screen.get_height()
    keymsg_rect = presskeymsg.get_rect(center = (wt/2, ht*2/3))
    newgame_rect = newgame_box.get_rect(center=(wt/2, ht*1/3))
    help_rect = helpmsg.get_rect(center = (wt/2, ht*3/4))
    screen.blit(newgame_box, newgame_rect)
    screen.blit(presskeymsg, keymsg_rect)
    screen.blit(helpmsg, help_rect)
    
def score(screen, time):
    global SCORE
    SCORE = str(int(time))
    return str(int(time))

'''def get_highscore():

    mycursor.execute("SELECT MAX(score) FROM scores")
    highscore = mycursor.fetchone()[0]
    return highscore

def update_highscore(new_score):

    mycursor.execute("UPDATE scores SET score = %s", (new_score))
    mydb.commit()'''
        
def load_map(level, tanks_list):
    
    with open(f"level{level}.txt") as file:
        
        game_map = [[0 for y in range(VIEW_HEIGHT)] for x in range(VIEW_WIDTH)]
        map_data = file.read().splitlines()
        map_data += [" " * VIEW_WIDTH] * (VIEW_HEIGHT - len(map_data))
        
        for y, i in enumerate(map_data):
            
            for x, j in enumerate(i):
                
                if j in TILE_MAP.keys():
                    game_map[x][y] = TILE_MAP[j]
                    
                elif j in TANK_MAP.keys():
                    tanks.append(Tank(TANK_MAP[j], x, y, False))
                    
                elif j == ".":
                    tanks[0].x = x
                    tanks[0].y = y
                    
    return game_map, tanks_list


