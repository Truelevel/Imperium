import pygame
from data.Constants import *
import random
#Camera = control surface, with all ingame process, except menu
class Camera:
    def  __init__(self,window):
        self.window = window
        self.width = CAMERA_WIDTH
        self.height = CAMERA_HEIGHT
        self.state = [0,0]
        self.screen = pygame.Surface((self.width,self.height))
    
    def render(self):
        self.window.blit(self.screen,(0,0))
        