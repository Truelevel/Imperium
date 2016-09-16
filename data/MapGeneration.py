import random
from data.Constants import *
#Class to control map and its generation
class World:
    def __init__(self,screen):
        self.screen = screen
        self.map = []
        for x in range(0,52):
            self.map.append(list())
            for y in range(0,38):
                self.map[x].append(random.randint(0,2))
        self.generate()
                
    def generate(self):
        for x in range(0,52):
            self.map.append(list())
            for y in range(0,38):
                self.map[x][y]=0
        for i in range(0,30):
            self.create_ground()
            self.create_desert()
            self.create_grass()
            
    def create_desert(self):
        size = random.randint(2,16)
        x = random.randint(0,WORLD_WIDTH-size)
        y = random.randint(0,WORLD_HEIGHT-size)
        for x1 in range(x,x+size):
            for y1 in range(y,y+size):
                self.map[x1][y1] = 2
    
    def create_ground(self):
        size = random.randint(2,18)
        x = random.randint(0,WORLD_WIDTH-size)
        y = random.randint(0,WORLD_HEIGHT-size)
        for x1 in range(x,x+size):
            for y1 in range(y,y+size):
                self.map[x1][y1] = 1
    
    def create_grass(self):
        size = random.randint(1,14)
        x = random.randint(0,WORLD_WIDTH-size)
        y = random.randint(0,WORLD_HEIGHT-size)
        for x1 in range(x,x+size):
            for y1 in range(y,y+size):
                self.map[x1][y1] = 0
    
    def render(self):
        for x in range(0,52):
            for y in range(0,38):
                self.screen.blit(TILES[self.map[x][y]],(x*TILE_SIZE,y*TILE_SIZE))