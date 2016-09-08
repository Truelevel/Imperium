import pygame

SCREEN_WIDTH = 1124
SCREEN_HEIGHT = 600
BACKGROUND = 'resourses/background.jpg'

WORLD_WIDTH = 52
WORLD_HEIGHT = 38

CAMERA_WIDTH = 824
CAMERA_HEIGHT = 600

X = 0
Y = 1

CITY_RANGE = 14
PLAYERS = 4
HUMAN_PLAYERS = 0

#Fonts
pygame.font.init()
COLOR01 = (183,48,48)
COLOR02 = (143,172,88)
GREEN = (4,191,9)
WOOD = (189,94,1)
YELLOW = (239,220,10)
BLUE = (0,137,224)


FONT01 = pygame.font.Font('resourses/Cornerstone.ttf',18)
FONT02 = pygame.font.Font('resourses/Cornerstone.ttf',25)

#### TILES
TILE_SIZE = 16
TILES_DIR = 'resourses/tiles/'
GRASS = pygame.image.load(TILES_DIR + 'grass.jpg')
GROUND = pygame.image.load(TILES_DIR + 'ground.jpg')
DESERT = pygame.image.load(TILES_DIR + 'desert.jpg')
TILES = (GRASS,GROUND,DESERT)

#### CITY TILES
BASE_TILE_COST = 60
EMPTY = pygame.image.load(TILES_DIR + 'empty.jpg') #0
FOOD_0 = pygame.image.load(TILES_DIR+'food_inactive.jpg') #1
FOOD_1 = pygame.image.load(TILES_DIR+'food_active.jpg') #2
PROD_0 = pygame.image.load(TILES_DIR+'prod_inactive.jpg') #3
PROD_1 = pygame.image.load(TILES_DIR+'prod_active.jpg') #4
GOLD_0 = pygame.image.load(TILES_DIR+'gold_inactive.jpg') #5
GOLD_1 = pygame.image.load(TILES_DIR+'gold_active.jpg') #6

CITY_TILES = ((EMPTY,EMPTY),(FOOD_0,FOOD_1),(PROD_0,PROD_1),(GOLD_0,GOLD_1))

FOOD = 1
PROD = 2
GOLD = 3

#City constants

START_POP = 3

#BUILDINGS

GRANARY = 0
SAWMILL = 1
MARKET = 2
LIBRARY = 3

BUILDINGS_NAME = ['Granary','Sawmill','Market','Library']

