#quick copy from my previous pygame project, just added mysql, needs more work

import pygame
import pygame.freetype
import os, sys, psutil, logging #os, sys and logging are inbuilt
from constants import *
from math import sqrt
import csv
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
    return surface.convert_alpha()

def highscore(SCORE):
    file1 = open('highscores.csv', 'r+', newline = '')       
    r = csv.reader(file1, delimiter=',')
    row1 = next(r)
    if int(SCORE)>int(row1[0]):
        w = csv.writer(file1, delimiter=',')
        file1.seek(0)
        w.writerow([int(SCORE)])
        return int(SCORE)
    else:
        return int(row1[0])
    file1.close()

def restart_program():
    try:
        psy = psutil.Process(os.getpid())  #gives id of memory process
        for handler in psy.open_files() + psy.connections():    #sees files open using memory id
            os.close(handler.fd)     #closes the files given by loop
    except Exception as exc:  #wildcard* exception
        logging.error(exc)    #should give a summary of what made program crash 
    python = sys.executable   #path for executable binary python (bytecode for specific processor)
    os.execl(python, python, *sys.argv)  #execl causes running process 'python' to be replaced by program passed as arguments

def play_game(screen):
    global SCORE
    max = highscore(SCORE)
    #try:
    text1 = 'SCORE: ' + SCORE+', HIGHEST: '+str(max)+ ' Click to try again.'
    #except:
        #text1 = 'SCORE:'+SCORE+ 'Click to try again'
    #text1 = 'CLICK ANYWHERE TO PLAY AGAIN'
    playagainbox = print_text(text1, 17, WHITE, None, False)
    againrect = playagainbox.get_rect(center = (screen.get_width()/2, screen.get_height()/2))
    screen.blit(playagainbox, againrect)

def quit_program():
    pygame.time.wait(1000)
    pygame.quit()
    sys.exit()

def newgame(screen):
    newgame_box = print_text('SKYWING SOAR', 46, BLACK, None, True)
    helpmsg = print_text('ESC: exit | A: accelerate | D: decelerate | UP, DOWN: Rotate | F11: Fullscreen', 10, BLUE, None, False)
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
    text1 = 'SCORE: ' + SCORE
    score = print_text(text1, 16, WHITE, None, True)
    wt = screen.get_width()
    ht = screen.get_height()
    scorebox = score.get_rect(center = (wt*34/40, ht*39/40))
    screen.blit(score, scorebox)
    flightscore.finalscore = str(int(time))
    
def showfps(screen, fps):
    text1 = 'FPS: ' + str(int(fps))
    fps_text = print_text(text1, 16, WHITE, None, True)
    wt = screen.get_width()
    ht = screen.get_height()
    fps_rect = fps_text.get_rect(center = (wt*34/40, ht*1/40))
    screen.blit(fps_text, fps_rect)


def set_highscore(score):
        mycursor.execute("INSERT INTO scores (score) VALUES (%s)", (score,))
        mydb.commit()
        return mycursor.lastrowid

def update_highscore(score_id, new_score):
        mycursor.execute("UPDATE scores SET score = %s WHERE id = %s", (new_score, score_id))
        mydb.commit()


