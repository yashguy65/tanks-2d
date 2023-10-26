#quick copy from my previous pygame project, just added mysql, needs more work

import pygame
import os
from constants import *
from game_sprites import *
import mysql.connector

pygame.init()
pygame.font.init()

mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS game_scores")
mycursor.execute("USE game_scores")
mycursor.execute("CREATE TABLE IF NOT EXISTS scores (id INT AUTO_INCREMENT PRIMARY KEY, score INT)")

def print_text(text, fontsize, textcolor, bgcolor, isbold):
    font = pygame.freetype.SysFont("Consolas", fontsize, bold=isbold)
    surface, _ = font.render(text=text, fgcolor=textcolor, bgcolor=bgcolor)
    return surface.convert()

def play_game(screen):
    scores = get_highscore()
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
    
def flightscore(screen, time):
    global SCORE
    SCORE = str(int(time))
    wt = screen.get_width()
    ht = screen.get_height()
    flightscore.finalscore = str(int(time))

def get_highscore():
    mycursor.execute("SELECT MAX(score) FROM scores")
    highscore = mycursor.fetchone()[0]
    return highscore

def update_highscore(new_score):
    mycursor.execute("UPDATE scores SET score = %s", (new_score))
    mydb.commit()
        
def load_map(level, game_map, tanks_list, screen):
    with open(f"level{level}.txt") as file:
        map_data = file.read().splitlines()
        map_data += [" " * screen.get_width()] * (screen.get_height() - len(map_data))
        for y in range(screen.get_height()):
            for x in range(screen.get_width()):
                char = map_data[y][x]
                if char in TILE_MAP:
                    game_map[x][y] = TILE_MAP[char]
                elif char in TANK_MAP:
                    tanks_list.append(Tank(TANK_MAP[char], x, y, stop=True))    
                elif char == ".":
                    tanks_list[0].x, tanks_list[0].y = x, y
    return game_map, tanks_list


