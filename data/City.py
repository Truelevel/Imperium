import pygame
from data.Constants import *
from data.Tile import *
from data.Building import *
from data.Tech import *
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
        
        self.science = 0
        self.techs = [0] #list of technologies
        self.techs_avaible = []
        self.techs_row = []
        self.check_avaible_techs()
        
        self.pop = START_POP
        self.pop_idle = self.pop
        self.workers = [None,0,0,0] # [0] - blank, 1-food, 2-prod, 3-gold
        self.food = 0
        self.pop_next_food = int((10+self.pop*2)*(1+self.pop*0.4)) #food for every next point of population
        
        self.prod = 0
        self.buildings = []  #all buildings in the city
        self.buildings_avaible = [] #what owner can to build right now
        self.buildings_row = [] #buildings row
        self.maintance = 0 #gold on buildings maintance
        self.check_avaible_buildings()
        
        
    def end_of_turn(self):
        self.check_food()
        self.check_prod()
        self.check_gold()
        self.check_science()
        self.check_avaible_buildings()    
        self.check_avaible_techs()
        
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
        if len(self.techs_row) > 0:
            menu.blit(FONT01.render(TECH_TREE[self.techs_row[0]].name + ': ' + str(self.science)+'/'+str(TECH_TREE[self.techs_row[0]].cost),0,BLUE),(830,310))
        menu.blit(FONT02.render('Buildings: ',0,COLOR02),(830,350))
        for i in self.buildings:
                menu.blit(FONT01.render(i.name + ' ' + str(i.level) + ' ' + str(i.output),0,COLOR02),(830,375+self.buildings.index(i)*25))

    
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
    
    def build(self,num):
        temp = self.buildings_avaible.pop(num)
        self.buildings_row.append(temp)
        self.check_avaible_buildings()
        
    
    def building_done(self):
        a = self.buildings_row.pop(0)
        self.prod -= a.cost
        for i in self.buildings:
            if i.type == a.type:
                self.buildings.remove(i)
        self.buildings.append(a)
    
    def building_find(self,type):
        for i in self.buildings:
            if i.type == type:
                return i
        NONE_BUILDING = Building(self,type)
        NONE_BUILDING.output = 0
        return NONE_BUILDING
        
############################TECHNOLOGIES########################

    def tech_learn(self,num):
        temp = self.techs_avaible.pop(num)
        self.techs_row.append(temp)
        self.check_avaible_techs()
    
    def tech_done(self):
        self.science -= TECH_TREE[self.techs_row[0]].cost
        self.techs.append(self.techs_row.pop(0))

############################CHECKS##############################
    def check_outputs(self):
        self.check_maintance()
        self.food_output = self.basic_output[0] + 10 * self.workers[FOOD] + self.building_find(0).output - self.pop * 3
        self.prod_output = self.basic_output[1] + 10 * self.workers[PROD] + self.building_find(1).output
        self.gold_total = self.basic_output[2] + 10 * self.workers[GOLD] + self.building_find(2).output
        self.science_output = int((self.pop + self.gold_total * self.player.science_rate) * (1 + self.building_find(3).level*0.2))
        self.gold_output = int(self.gold_total - self.gold_total * self.player.science_rate)
        
    
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
                self.building_done()
                    
    def check_gold(self):
        self.player.gold += self.gold_output
        if self.player.gold < 0:
            self.player.science += self.player.gold
            self.player.gold = 0
    
    def check_science(self):
        self.science += self.science_output
        if self.science >= TECH_TREE[self.techs_row[0]].cost:
            self.tech_done()
            
    
    def check_maintance(self):
        self.maintance = 0
        for i in self.buildings:
            self.maintance += i.maintance
    
    def check_row(self,type): 
        for i in self.buildings_row:
            if i.type == type:
                return False
        return True
        
    
    def check_avaible_buildings(self):
        self.buildings_avaible = []
        for type in range(len(BUILDINGS_DICT)):
            if BUILDINGS_DICT[type][2] in self.techs:
                if self.check_row:
                    if self.building_find(type).level <= BUILDINGS_DICT[type][MAXLVL]:
                        self.buildings_avaible.append(Building(self,type))
                    
                    
    def check_avaible_techs(self):
        self.techs_avaible = []
        for id in range(1, len(TECH_TREE)):
            if id not in self.techs:
                if all(techs in self.techs for techs in TECH_TREE[id].required_tech):
                    self.techs_avaible.append(id)