from pico2d import load_image

width = 1200
height = 700

class Sprite:
    image = None
    posX = 0
    posY = 0
    w = 0
    h = 0
    i_w = 0
    i_h = 0
    frame = 0
    action = 1

    def __init__(self):
        pass

    def imageLoad(self,name):
        self.image = load_image(name)

    def Show(self):
        self.image.clip_draw(self.i_w*int(self.frame),self.i_h*self.action,self.w,self.h,self.posX,self.posY)
        #self.frame = (self.frame + 0.1) % 4

    def Gravity(self):
            if self.posY > 160: self.posY -= 10

    def OutOfMap(self):
        if self.posX < 40: self.posX = 40
        if self.posX > width - 40: self.posX = width - 40