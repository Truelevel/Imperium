import pygame
from data.Constants import *
from data.Tile import *
from data.Building import *
#Class to control cities on the map
class City:
    def __init__(self,x,y,screen,map):
        #global info
        self.player = None
        self.x = x  #x,y - center of city
        self.y = y
        self.screen = screen
        self.corner = (self.x - 4,self.y-4) #coords top-left corner of the city
        self.image = pygame.image.load('resourses/city.png').convert_alpha()
        self.border_image = pygame.image.load('resourses/city_border.png').convert_alpha()
        self.tile_generate()
        self.tile_cost = BASE_TILE_COST
        
        
        #basic output - PROD in the center of the city, which depends on tiles under it
        #grass - +1 food, earth - +1 PROD, desert +1 gold
        self.basic_output = [0,0,0]
        for x in (-1,0,1):
            for y in (-1,0,1):
                if map[self.x + x][self.y + y] == 0:
                    self.basic_output[0] += 1
                if map[self.x + x][self.y + y] == 1:
                    self.basic_output[1] += 1
                if map[self.x + x][self.y + y] == 2:
                    self.basic_output[2] += 1

        #information about population and output
        
        self.pop = START_POP
        self.pop_idle = self.pop
        self.workers = [None,0,0,0] # [0] - blank, 1-food, 2-prod, 3-gold
        self.food = 0
        self.pop_next_food = int((10+self.pop*2)*(1+self.pop*0.4)) #food for every next point of population
        
        self.prod = 0
        self.buildings = [0,0,0,0]
        self.buildings_row = []
        self.maintance = 0
        
        
        
    def render(self):
        self.screen.blit(self.image,((self.x - 1)*TILE_SIZE,(self.y-1)*TILE_SIZE))
        self.screen.blit(self.border_image,((self.corner[X]*TILE_SIZE,self.corner[Y]*TILE_SIZE)))
        for i in self.map:
            i.render()
        #temp statistics about cities
        
    def render_info(self,menu):
        menu.blit(FONT02.render('Player ' + str(self.player.id),0,COLOR01),(830,10))
        menu.blit(FONT01.render('Food output: ' + str(self.food_output),0,GREEN),(830,55))
        menu.blit(FONT01.render('Population: ' + str(self.pop)+' '+str(self.food)+'/'+str(self.pop_next_food),0,GREEN),(830,80))
        menu.blit(FONT01.render('Prod output ' + str(self.prod_output),0,WOOD),(830,115))
        if len(self.buildings_row) > 0:
            menu.blit(FONT01.render(self.buildings_row[0].name + ' ' + str(self.prod) + '/' + str(self.buildings_row[0].cost),0,WOOD),(830,140))
        menu.blit(FONT01.render('Gold output: ' + str(self.gold_output),0,YELLOW),(830,175))
        menu.blit(FONT01.render('Total gold: ' + str(self.player.gold),0,YELLOW),(830,200))
        menu.blit(FONT01.render('Tile cost ' + str(self.tile_cost),0,YELLOW),(830,225))
        menu.blit(FONT01.render('Science output: ' + str(self.science_output),0,BLUE),(830,260))
        menu.blit(FONT01.render('Science rate: ' + str(self.player.science_rate),0,BLUE),(830,285))
        menu.blit(FONT01.render('Total science: ' + str(self.player.science),0,BLUE),(830,310))
        menu.blit(FONT02.render('Buildings: ',0,COLOR02),(830,350))
        temp = 1
        for i in self.buildings:
            if i != 0:
                menu.blit(FONT01.render(i.name + ' ' + str(i.level) + ' ' + str(i.output),0,COLOR02),(830,350+temp*25))
                temp += 1
    
##################TILES#############################
        
    def tile_add(self,type):
        if self.player.gold >= self.tile_cost:
            tile = self.tile_find(0)
            tile.type = type
            self.player.gold -= self.tile_cost
            self.tile_cost += 4
            return True
        return False
    
    def tile_sell(self,tile):
        if tile.type in (1,2,3):
            tile.type = 0
            if tile.worker == True:
                tile.worker = False
                self.pop_idle += 1
            self.player.gold += BASE_TILE_COST
            self.check_outputs()
    
    def tile_count(self,tile,worker = False): #DOTO
        summ = 0
        for i in self.map:
            if i.type == tile and i.worker == worker:
                summ += 1
        return summ
    
    def tile_find(self,tile,worker = False):
        for i in self.map:
            if i.type == tile and i.worker == worker:
                return i
        
        return False             
            

                
        
    def tile_generate(self):
        self.map = [Tile(self,y,x,0) for x in range(0,9) for y in range(0,9)]
        for i in (30,31,32,39,40,41,48,49,50):
            self.map[i].type = 'N'
        for i in (29,38,47):
            self.map[i].type = 1
        for i in (21,22,23):
            self.map[i].type = 2
        for i in (33,42,51):
            self.map[i].type = 3
            
###########################BUILDINGS###########################
    
    def build(self,type):
        self.buildings_row.append(Building(self,type))
        
    
    def building_done(self):
        a = self.buildings_row.pop(0)
        self.buildings[a.type] = a
        self.check_outputs()
        

############################CHECKS##############################
    def check_outputs(self):
        bo = self.check_buildings_output()
        self.check_maintance()
        self.food_output = self.basic_output[0] + 10 * self.workers[FOOD] + bo[0] - self.pop * 3
        self.prod_output = self.basic_output[1] + 10 * self.workers[PROD] + bo[1]
        self.gold_total = self.basic_output[2] + 10 * self.workers[GOLD] + bo[2] - self.maintance
        self.science_output = self.pop + self.gold_total * self.player.science_rate
        self.gold_output = self.gold_total - self.gold_total * self.player.science_rate
        
    
    def check_food(self):
        self.food += self.food_output
        if self.food >= self.pop_next_food:
            print('Player ',self.player.id,' population up!')
            self.food -= self.pop_next_food
            self.pop += 1
            self.pop_idle += 1
            self.pop_next_food = int((10+self.pop*2)*(1+self.pop*0.4))
        if self.food < 0:
            self.pop -= 1
            if self.pop_idle > 0:
                self.pop_idle -= 1
            else:
                for i in self.map:
                    if i.worker == True:
                        i.worker = False
                        self.check_outputs()
                        break
                    
    def check_prod(self):
        if len(self.buildings_row) > 0:
            self.prod += self.prod_output
            if self.prod >= self.buildings_row[0].cost:
                self.prod -= self.buildings_row[0].cost
                self.building_done()
                    
    def check_gold(self):
        self.player.gold += self.gold_output
        if self.player.gold < 0:
            self.player.science += self.player.gold
            self.player.gold = 0
    
    def check_maintance(self):
        self.maintance = 0
        for i in self.buildings:
            if i != 0:
                self.maintance += i.maintance
    
    def check_buildings_output(self):
        out = [0,0,0]
        for i in self.buildings:
            if i != 0:
                out[i.type] += i.output
        return out
    
    
    
    
            
        
            


           
    
        
    