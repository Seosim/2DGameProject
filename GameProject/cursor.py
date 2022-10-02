from sprite import Sprite

class Cursor(Sprite) :
    def __init__(self):
        self.i_w = 50
        self.i_h = 50
        self.w = 100
        self.h = 100

    def UpdateCursor(self,x,y):
        self.posX = x
        self.posY = y

    def Show(self):
        self.image.clip_draw(0,0,self.w,self.h,self.posX,699 - self.posY)

aim = Cursor()

