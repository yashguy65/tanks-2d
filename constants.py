#quick copy from prev project, to be modified
import pygame
pygame.init()

SCREEN_WIDTH = 12500
SCREEN_HEIGHT = 1250
START_TIME = None

VIEW_WIDTH = 700
VIEW_HEIGHT = 500

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = COLORKEY = (0,0,0)
SKYBLUE = (135,206,235)

SCORE = 0

TILE_MAP = {
    " ": None,
    "0": "treeLarge",
    "1": "treeSmall",
    "2": "dirt",
    "3": "grass",
    "4": "sand"    
}

TANK_MAP = {
    #"5": ""#"alpha",
    #"6": ""#"beta",
    #"7": ""#"gamma"
    #"8": ""#delta
}

tankvelc = 1
birdlist = []

FLAGS = pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.SHOWN #| pygame.NOFRAME

PLAYER_ARGS = { 'x':325, 'y':250, 'w':89, 'h':20,
                            'rot_angle_constant':0.5, 'max_thrust_mag':0.5}

RUN_PLANE_PHY = RUN_PLAYER_UPDATE = RUN_SIDESCROLL = True

GAMEMODE = 'Starting'
