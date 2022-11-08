import pico2d

from sprite import Sprite
from MapData import Map
from MapData import size

width = 1200
height = 700

class Player(Sprite):

    def __init__(self):

        self.speed = 4
        self.jumpMax = 180
        self.jumpPower = 15
        self.hp = 100

        self.jumpY = -1
        self.gravitySpeed = 1

        self.PushR = False
        self.PushL = False

        self.PushSpace = False
        self.stand = True

        self.posX = 300
        self.posY = 200
        self.i_w = 16 * 4
        self.i_h = 25 * 4
        self.w = self.i_w
        self.h = self.i_h
        self.inv = 0 # 무적
        self.hitframe = 0
        self.screenX = self.posX
        self.cameraX = width/2
        self.cameraY = 0
        self.hit = False

        self.pushS = False
        self.fall = 0

    def getScreenX(self):
        stage = Map.stageData[Map.number]

        if width / 2 > self.posX: self.screenX = self.posX
        elif self.posX >= size * len(stage[6]) - width/2:
            self.screenX = width - (len(stage[6])*size-self.posX)
        else : self.screenX =  width / 2



    def Show(self):
        self.image.clip_draw(self.i_w * (self.hitframe+int(self.frame)), self.i_h * self.action, self.w, self.h, self.screenX,self.posY-self.cameraY)


    def move(self):
        stage = Map.stageData[Map.number]

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

        if self.hit:
            if player.PushL: self.cameraX -= 12
            elif player.PushR: self.cameraX += 12
            else: self.cameraX += 10
            self.hit = False


        self.cameraY = max(0,self.posY-height+250)

    def down(self):

        if self.pushS and self.PushSpace:
            self.PushSpace = False
            if not self.collision(0,-20):
                self.posY -= 20

        # if self.fall > 0: self.fall = (self.fall +1) % 25

    def jump(self):
        if self.pushS: return

        if self.PushSpace:
            if self.jumpY == -1:
                self.jumpY = self.posY

            if self.posY < self.jumpY + self.jumpMax and not self.collision(0, self.jumpPower):
                self.posY += self.jumpPower
                self.speed = 6
                if self.jumpPower > 5: self.jumpPower -= 0.7
            else:
                self.PushSpace = False
                self.jumpY = -1
                self.speed = 4
                self.jumpPower = 15

    def Flash(self):
        for i in range(5):
            if self.PushR and not self.collision(35, 0):
                self.posX += 35
                self.action = 1
            elif self.PushL and not self.collision(-35, 0):
                self.posX -= 35
                self.action = 0



    def Gravity(self):
        if not self.PushSpace:
            if not self.collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5

            else: self.PushSpace = False

    def collision(self,valX, valY):

        stage = Map.stageData[Map.number]

        sx = self.posX//size
        sy = self.posY//size
        if sx > len(Map.stageData[Map.number][0]) : return False

        for __y in range(-1,2):
            _y = len(stage)-1 - max(0,int(sy+__y))
            if _y != pico2d.clamp(0,_y,len(stage)-1): continue
            for _x in range(-2,2,1):
                x = int(sx + _x)
                if x != pico2d.clamp(0, x, len(stage[0]) - 1): continue
                if stage[_y][x] and stage[_y][x] != 3:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                                self.posY - (y * size + (size / 2)) + valY) < size / 2 + self.h / 2 - 5:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - (y * size + size)) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
                elif stage[_y][x] == 3:

                    if self.PushSpace:continue

                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5 :# 가로줄 충돌
                         # if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                         #         self.posY - (y * size + (size/2)) + valY) < 30/2 + self.h / 2 -5:  # 세로줄 충돌
                         if abs(self.posY+valY - (self.h/2) - (y * size + (size/2))) < 8 :
                            if abs((self.posY - self.h / 2) - (y * size + 50+15) ) <= 15:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
        self.stand = False
        return False

    def ColtoMonster(self,mlist):
        for monster in mlist:
            if abs(self.posX - monster.posX)+35 < (monster.w/2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - monster.posY) < (monster.h / 2) + (self.h / 2)-15:  # 세로줄 충돌
                    if self.inv == 0:
                        self.hp -= monster.power
                        self.inv = 2
                        return

    def invincibility(self):
        if self.inv == 0 : return

        if self.inv :
            self.inv -= 0.015
            if self.hitframe == 0 : self.hitframe = 5
            else : self.hitframe = 0

        if self.inv <= 0 :
            self.hitframe = 0
            self.inv = 0

    def KeyReset(self):
        self.PushL = False
        self.PushR = False

player = Player()

def playerInit():
    player.__init__()
    player.imageLoad('./res/idle.png')


def playerUpdate():
    player.getScreenX()
    player.invincibility()
    player.move()
    player.jump()
    player.down()
    player.Gravity()
    player.OutOfMap()
    player.frame = (player.frame + 0.1) % 4
