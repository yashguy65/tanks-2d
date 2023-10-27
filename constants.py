#quick copy from prev project, to be modified
import pygame
pygame.init()

VIEW_WIDTH = 1408
VIEW_HEIGHT = 768

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = COLORKEY = (0,0,0)
SKYBLUE = (135,206,235)

SCORE = 0
SCALEX = 4
SCALEY = 3

TILE_MAP = {
    " ": "dirt",
    "0": "treelarge",
    "1": "treesmall",
    "2": "grass",
    "3": "sand",
    
    "4": "oil",
    "5": "sandbagbeige",
}

TANK_MAP = {
    "A": "beige",   # alpha
    "B": "black",   # beta
    "C": "green",   # gamma
    "D": "red",     # delta
} #blue taken for player as .

tankvelc = 1
tanks = []
bullets = []


GAMEMODE = 'Starting'
bounceLimit = 4
bulletvelc = 0.1
