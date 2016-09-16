import pygame
import random
from pygame.locals import *
from data.Constants import *
from data.Camera import *
from data.MapGeneration import *
from data.City import *
from data.Player import *
from data.Clickable import *

class Main():
    def __init__(self,screen):
        self.screen = screen
        self.running = True
        self.camera = Camera(screen)
        self.world = World(self.camera.screen)  
        self.city = []
        self.players = []
        self.hitbox = []
        self.choosen = None
        self.player_generation(PLAYERS, HUMAN_PLAYERS)
        self.background = pygame.image.load(BACKGROUND)
        self.turn= 0
        self.main_loop()
        
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.event.clear()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.world.generate()
                if event.key == K_LEFT:
                    if self.choosen != None:
                        for i in self.choosen.map:
                            print(i.type)
                if event.key == K_SPACE:
                    self.end_of_turn()
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[0]<CAMERA_WIDTH:
                    for i in self.hitbox:
                        x = i.check_click(event.pos)
                        if x != None:
                            self.choosen = x
    
    def render(self):
        #draw everything on the screen
        self.screen.blit(self.background,(CAMERA_WIDTH,0))
        self.world.render()
        for i in self.city: 
            i.render()
        if self.choosen != None:
            self.choosen.render_info(self.screen)
        self.camera.render()
        pygame.display.flip()
    
    def main_loop(self):
        while self.running == True:
            self.handle_events()
            self.render()
    
    def end_of_turn(self):
        for ai in self.players:
            if ai.ai == True:
                ai.ai_turn()
            ai.city.end_of_turn()
        self.turn += 1
        print('Next Turn! (',    str(self.turn),')')
        
    
    def create_city(self):
        #Create city at random location
        #minimum distance between cities centers = CITY_RANGE
        created = False
        while created == False:
            created = True
            x = random.randint(4,WORLD_WIDTH-5)
            y = random.randint(4,WORLD_HEIGHT-5)
            for i in self.city:
                if x + CITY_RANGE > i.x and y + CITY_RANGE > i.y and  x - CITY_RANGE < i.x and y - CITY_RANGE < i.y:  
                    created = False
        self.city.append(City(x,y,self.camera.screen,self.world.map))
        self.hitbox.append(Clickable((x-4)*16,(y-4)*16,9*16,9*16,self.city[-1]))
        
    
    def create_player(self, id, ai = True):
        self.create_city()
        self.players.append(Player(id,self.city[-1],ai))
        self.city[-1].player = self.players[-1]
        self.city[-1].check_outputs()
        
    def player_generation(self,num,humans):
        humans_count = 0
        if num < 1 or num > 4:
            num = 4
        for id in range(0,num):
            if humans_count < humans:
                self.create_player(id, ai = False) 
                humans_count += 1
            else:
                self.create_player(id)
    
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
g = Main(screen)
