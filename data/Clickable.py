from data.Constants import *

class Clickable():
    def __init__(self,x,y,width,height,obj):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obj = obj
    
    def check_click(self,click):
        if click[0] >= self.x and click[0] <= self.x+self.width and click[1] >= self.y and click[1] <= self.y + self.height:
            return self.obj
        return None