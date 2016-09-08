from data.Constants import *

class Building:
    def __init__(self,city,type):
        self.city = city
        self.type = type
        self.name = BUILDINGS_NAME[type]
        self.output = 0
        self.previous_building = self.city.buildings[self.type] #checks level of that kind of building city already has
        self.check_cost()
        self.check_output()
        self.maintance = self.level
    
    def check_cost(self):
        if self.previous_building == 0:
            self.level = 1
        else:
            self.level = self.previous_building.level + 1
        if self.type in (0,1,2):
            self.cost = self.level * 40 * (1 + (self.level - 1) * 0.85)
        elif self.type == 4:
            self.cost = (80 + (self.level - 1) * 100) * (1 + (self.level - 1) * 0.2)
    
    def check_output(self):
        if self.type in (0,1,2):
            self.output = self.level * (6 + self.level * 4)
             