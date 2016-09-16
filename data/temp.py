BUILDINGS_DICT = { 
                  0 : ('Granary',None,5), #(name, required tech, maxlvl)
                  1 : ('Sawmill',None,5),
                  2 : ('Market',None,5),
                  3 : ('Library',3, 4)
                  }

class Building:
    def __init__(self,city,type):
        self.city = city
        self.type = type
        self.name = BUILDINGS_DICT[type][0]
        self.level = self.city.buildings[type]
        
    def __str__(self):
        return self.name
        
    def check_output(self):
        if self.type in (0,1,2):
            self.output = self.level * (6 + self.level * 4)
    
    def check_maintance(self):
        if self.type in (0,1,2,3):
            self.maintance = self.level