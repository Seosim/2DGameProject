from sprite import Sprite
from MapData import *

width = 1200
height = 700

class Player(Sprite):
    speed = 4
    jumpPower = 150
    hp = 100

    jumpY = -1
    gravitySpeed = 1

    PushR = False
    PushL = False

    PushSpace = False
    stand = True

    def __init__(self):
        self.posX = 300
        self.posY = 300
        self.i_w = 16 * 4
        self.i_h = 25 * 4
        self.w = self.i_w
        self.h = self.i_h
        self.screenX = self.posX
        self.inv = 0 # 무적
        self.hitframe = 0
        self.cameraX = width/2

    def getScreenX(self):
        if width / 2 > self.posX: self.screenX = self.posX
        elif self.posX >= size * len(stage[6]) - width/2:
            self.screenX = width - (len(stage[6])*size-self.posX)
        else : self.screenX =  width / 2

    def Show(self):
        self.image.clip_draw(self.i_w * (self.hitframe+int(self.frame)), self.i_h * self.action, self.w, self.h, self.screenX,self.posY)
        self.frame = (self.frame + 0.1) % 4

    def move(self):
        if self.PushR and not self.collision(self.speed,0):
            self.posX += self.speed
            self.action = 1
        elif self.PushL and not self.collision(-1*self.speed,0):
            self.posX -= self.speed
            self.action = 0

        self.cameraX = player.posX - (1200 / 2)
        if self.cameraX <= 0:
            self.cameraX = 0
        elif size * len(stage[6]) - player.posX <= 600:
            self.cameraX = size * len(stage[6]) - 1200

    def jump(self):
        if self.PushSpace:
            if self.jumpY == -1:
                self.jumpY = self.posY

            if self.posY < self.jumpY + self.jumpPower and not self.collision(0,10):
                self.posY += 10
            else:
                self.PushSpace = False
                self.jumpY = -1

    def Gravity(self):
        if not self.PushSpace:
           # if self.posY > 160 and not collision(0,-10): self.posY -= 10
            if not self.collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 2

                #self.posY -= 10

            else: self.PushSpace = False

    def collision(self,valX, valY):
        sx = self.posX//size

        for _y in range(0,len(stage)):
            for _x in range(-2,2,1):
                x = sx + _x
                if stage[_y][x]:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                                self.posY - (y * size + (size / 2)) + valY) < size / 2 + self.h / 2 - 5:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - ((y + 1) * size)) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
        self.stand = False
        return False

    def ColtoMonster(self,mlist):
        for monster in mlist:
            if abs(self.posX - monster.posX) < (monster.w/2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - monster.posY) < (monster.h / 2) + (self.h / 2)-15:  # 세로줄 충돌
                    if self.inv == 0:
                        self.hp -= monster.power
                        print('player hp : ',self.hp)
                        self.inv = 2
                        return

    def invincibility(self):
        if self.inv :
            self.inv -= 0.015
            if self.hitframe == 0 : self.hitframe = 5
            else : self.hitframe = 0

        if self.inv <= 0 :
            self.hitframe = 0
            self.inv = 0




player = Player()

def playerUpdate():
    player.getScreenX()
    player.invincibility()
    player.move()
    player.jump()
    player.Gravity()
    player.Show()