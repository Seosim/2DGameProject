from pico2d import load_image
from MapData import Map
from MapData import size

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
    gravitySpeed = 10
    stand = True
    #def __init__(self):
     #   pass

    def imageLoad(self,name):
        self.image = load_image(name)

    def Show(self,x):
        self.image.clip_draw(self.i_w*int(self.frame),self.i_h*self.action,self.w,self.h,self.posX-x,self.posY)


    def OutOfMap(self):
        if self.posX < 40: self.posX = 40
        if self.posX > width - 40: self.posX = width - 40

    def collision(self,valX, valY):
        stage = Map.stageData[Map.number]

        sx = self.posX//size
        if sx > len(Map.stageData[Map.number][0]) : return False

        for _y in range(0,len(stage)):
            for _x in range(-2,2,1):
                x = int(sx) + _x
                if x >= len(stage[_y]): continue
                if stage[_y][x]:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(self.posY - (y * size + (size / 2)) + valY) < size / 2 + self.h / 2 - 5:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - ((y + 1) * size)) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
        self.stand = False
        return False
