
class Tech():
    def __init__(self,id,name,req,cost):
        self.id = id
        self.name = name
        self.cost = cost
        self.required_tech = req
        
    def __str__(self):
        return self.name

TECH_TREE = (
             Tech(0,'Agriculture',None,0),           
             Tech(1,'Division of labour',(0,),20),    
             Tech(2,'Warfare',(0,),20),               
             Tech(3,'Writing',(1,),80),                
             Tech(4,'Engineering',(1,2),80),          
             Tech(5,'Storage',(4,),320),               
             Tech(6,'Horse Riding',(2,),320),           
             Tech(7,'Iron Working',(5,6),1280),        
             Tech(8,'Siege tactics',(6,),1280),          
             Tech(9,'Industrial revolution',(7,),2560)       
             )

