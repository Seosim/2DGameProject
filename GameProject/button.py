from pico2d import *
from mapData import width,height

class Button():
    image = None
    def __init__(self):
        Button.image = load_image('./res/title_button.png')
        self.xSize = 270
        self.ySize = 102
        self.posX = 0
        self.posY = 0
        self.frame = 0

    def setButton(self,x,y,f):
        self.posX = x
        self.posY = y
        self.frame = f

    def draw(self):
        self.image.clip_draw(0,self.ySize*self.frame,self.xSize,self.ySize,self.posX,self.posY)

    def InClick(self,x,y):
        y = height-1 - y
        if self.posX - self.xSize/2 < x < self.posX+self.xSize/2:
            if self.posY - self.ySize/2 < y < self.posY+self.ySize/2:
                return True
        return False