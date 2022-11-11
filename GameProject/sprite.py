from pico2d import load_image
from MapData import Map,size,width,height
import pico2d

class Sprite:
    image = None
    posX = 0
    posY = 0
    w = 0
    h = 0
    i_w = 0
    i_h = 0
    frame = 0
    frameCnt = 0
    frameTime = 0
    action = 1
    gravitySpeed = 10
    stand = True
    #def __init__(self):
     #   pass

    def imageLoad(self,name):
        self.image = load_image(name)

    def Show(self,x,y):
        self.image.clip_draw(self.i_w*int(self.frame),self.i_h*int(self.action),self.i_w,self.i_h,self.posX-x,self.posY-y,self.w,self.h)

    def flipShow(self,x,y):
        self.image.clip_composite_draw(self.i_w*int(self.frame),self.i_h*self.action,self.i_w,self.i_h,0,'h',self.posX-x,self.posY-y,self.w,self.h)

    def OutOfMap(self):
        if self.posX < 40: self.posX = 40
        if self.posX > (len(Map.stageData[Map.number][0])*size) - 40:
            self.posX = (len(Map.stageData[Map.number][0])*size) - 41

    def collision(self,valX, valY):
        stage = Map.stageData[Map.number]

        sx = self.posX//size
        sy = self.posY//size
        if sx > len(Map.stageData[Map.number][0]) : return False
        if sy > len(stage) : return False

        for __y in range(-2,2):
            _y = len(stage)-1 - max(0,int(sy+__y))
            if _y != pico2d.clamp(0,_y,len(stage)-1): continue
            for _x in range(-2,2,1):
                x = int(sx + _x)
                if x != pico2d.clamp(0, x, len(stage[0]) - 1): continue
                if stage[_y][x] and stage[_y][x] != 3:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(self.posY - (y * size + (size / 2)) + valY) < size / 2 + self.h / 2 - 5:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - ((y + 1) * size)) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
                elif stage[_y][x] == 3:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                                self.posY - (y * size + (size/2)) + valY) < 30/2 + self.h / 2:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - (y * size + 50+15) ) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
        self.stand = False
        return False
