from data.Constants import *

class Tile():
    def __init__(self,city,x,y,type):
        self.x = x
        self.y = y
        self.city = city
        self.type = type
        self.worker = False
        self.hp = 50
        self.icon = CITY_TILES[self.type][self.worker]
        self.output = 10
    
    def render(self):
        if self.type != 'N':
            self.city.screen.blit(CITY_TILES[self.type][self.worker],((self.city.corner[X]+self.x)*TILE_SIZE,(self.city.corner[Y]+self.y)*TILE_SIZE))
    
    def worker_remove(self):
        if self.worker == True:
            self.worker = False
            self.city.pop_idle += 1
            self.city.workers[self.type] -=1
            self.city.check_outputs()
            return True
        return False
    
    def worker_add(self):
        if self.worker == False and self.city.pop_idle > 0:
            self.worker = True
            self.city.pop_idle -= 1
            self.city.workers[self.type] += 1
            self.city.check_outputs()
            return True
        return False
    
    def worker_swap(self,tile):
        if tile.worker == True and self.worker == False:
            tile.worker = False
            self.worker = True
            self.city.workers[tile.type] -= 1
            self.city.workers[self.type] += 1
            self.city.check_outputs()
            return True
        return False
            