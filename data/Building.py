ID = 0
NAME = 1
TECH = 2
MAXLVL = 3

BUILDINGS_DICT = { 
                  0 : (0, 'Granary',0,5), #(id, name, required tech, maxlvl)
                  1 : (1, 'Sawmill',0,5),
                  2 : (2, 'Market',0,5),
                  3 : (3, 'Library',3, 4),
                  4 : (4, 'Barracks',2,1)
                  }


class Building:
    def __init__(self,city,type):
        self.city = city
        self.type = type
        self.name = BUILDINGS_DICT[type][1]
        self.check_level()
        self.check_output()
        self.check_cost()
        self.check_maintance()
                
    def __str__(self):
        return self.name
        
    def check_output(self):
        if self.type in (0,1,2):
            self.output = self.level * (6 + self.level * 4)
        else:
            self.output = 0
                
    def check_maintance(self):
        if self.type in (0,1,2,3,4):
            self.maintance = self.level
            
    def check_level(self):
        self.level = 1
        for i in self.city.buildings:
            if i.type == self.type:
                self.level = i.level + 1
            
    def check_cost(self):
        if self.type in (0,1,2):
            self.cost = self.level * 40 * ( 1 + self.level * 0.6)
        elif self.type == 3:
            self.cost = self.level * 40 * (1 + self.level * 1.5)
        elif self.type == 4:
            self.cost = 80