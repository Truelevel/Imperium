import pygame
import random
from data.Constants import *
from data.City import *

class Player:
    def __init__(self,id,city, ai):
        self.id = id
        self.ai = ai
        self.gold = 0
        self.science = 0
        self.city = city
        #for AI
        self.global_strat = None
        self.global_strats = {
                              0: 'Passive_Grow',
                              1: 'Passive_Production',
                              2: 'Passive_Gold',
                              3: 'Aggresive'
                              }
        self.science_rate = 0.4
        self.need_gold = 0
        self.buildings_plan = []
    
    def ai_turn(self):
        self.report('making turn')
        if self.global_strat == None: #choose game plan
            self.choose_strategy()
        if self.city.food_output < 0: #if city starving
            self.stop_starve()
        if self.city.pop_idle > 0: #remove all idle pop
            self.choose_idle_pop()
        if len(self.city.buildings_row) == 0: #what to build in city?
            self.choose_building()
        self.science_rate_config()
        print('My city: Food: ',self.city.food_output,' Production: ',self.city.prod_output,' Gold: ',self.city.gold_output,' Science: ',self.city.science_output)
        
    def report(self,text):
        print('Player ',self.id,' ',text)
    
    def science_rate_config(self):
        x = 0.4
        if self.global_strat == 'Passive_Gold':
            x += 0.2
        if self.need_gold == 1:
            x = 0
            self.need_gold = 0
        self.science_rate = x
    
    def stop_starve(self):
        print('STARVING!')
        while self.city.food_output < 0:
            if self.city.tile_count(FOOD) <= 0:
                if self.gold >= self.city.tile_cost:
                    self.city.tile_add(FOOD)
                else:
                    self.report('cant fix starving :(')
                    break
            else: 
                choose = self.city.tile_find(FOOD)
                if self.city.pop_idle > 0:
                    choose.worker_add()
                elif self.city.tile_count(GOLD,True) > 0:
                        choose.worker_swap(self.city.tile_find(GOLD,True))
                else: choose.worker_swap(self.city.tile_find(PRODUCTION,True))
            
            
    def add_worker_or_tile(self,type):
        #add worker to a tile, if there are no free work tiles
        #trying to add tile
        #if not enought gold return false 
        if self.city.tile_count(type) <= 0 and self.gold < self.city.tile_cost:
            self.need_gold = 1
            self.report('need gold!')
        if self.city.tile_count(type) <= 0 and self.gold >= self.city.tile_cost:
            self.city.tile_add(type)
        if self.city.tile_count(type) > 0:
            choose = self.city.tile_find(type)
            choose.worker_add()
            return True
        else:
            return False
    
        
    
    def basic_strat(self, T1,T2,T3, add):
        if self.city.tile_count(T1,True) < self.city.tile_count(T2,True)*2 + add and self.add_worker_or_tile(T1) == True:
            pass
        elif self.city.tile_count(T2,True) < self.city.tile_count(T3,True) + 1 and self.add_worker_or_tile(T2) == True:
                pass
        elif self.add_worker_or_tile(T3) == False:
            self.report('impossible to fix workless population :(')
            self.impossible = True
                
                    
    def choose_idle_pop(self):
        self.impossible = False
        while self.city.pop_idle > 0 and self.impossible == False:
            if self.city.food_output < 10+self.city.pop*2:
                if self.city.tile_count(FOOD) > 0:
                    choose = self.city.tile_find(FOOD)
                    choose.worker_add()
                elif self.gold >= self.city.tile_cost:
                    self.city.tile_add(FOOD)
            if self.global_strat == 'Passive_Grow':
                self.basic_strat(FOOD, PROD, GOLD, self.seed)
            
            if self.global_strat == 'Passive_Production':
                self.basic_strat(PROD, GOLD, FOOD, self.seed)

            if self.global_strat == 'Passive_Gold':
                self.basic_strat(GOLD, PROD, FOOD, self.seed)
    
    def choose_strategy(self):
        i = random.randint(0,2)
        self.seed = random.randint(0,2)
        self.global_strat = self.global_strats[i]
        self.report('has chosen ' + self.global_strat + ' strategy!')
        i = random.randint(0,3)
        if i == 0:
            self.buildings_plan = [1,0,2,0,1,2,0,1,2,0,1,2,0,1,2]
        elif i == 1:
            self.buildings_plan = [0,1,0,1,0,2,0,1,2,0,1,2,1,2,2]
        elif i == 2:
            self.buildings_plan = [0,1,2,2,0,2,1,0,1,2,0,1,2,0,1]
        else:
            self.buildings_plan = [1,0,1,0,2,0,0,1,0,2,2,1,2,1,2]
    
    
    def choose_building(self):
        if len(self.buildings_plan) > 0:
            i = self.buildings_plan.pop(0)
            self.city.build(i)
        else:
            self.city.build(random.randint(0,2))
        
        
                    
                
                
                
                    
                