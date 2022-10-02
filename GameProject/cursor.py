from sprite import Sprite

class Cursor(Sprite) :
    def __init__(self):
        self.i_w = 50
        self.i_h = 50
        self.w = 50
        self.h = 50

    def UpdateCursor(self,x,y):
        self.posX = x
        self.posY = y

    def Show(self):
        self.image.clip_draw(0,0,50,50,self.posX,699 - self.posY)

aim = Cursor()

