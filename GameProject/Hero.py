import pico2d
import game_framework
import time
import math

from sprite import Sprite
from MapData import width,height,Map,size

class Player(Sprite):

    def __init__(self):

        self.speed = 12
        self.jumpMax = 180
        self.jumpPower = 40
        self.hp = 100

        self.jumpY = -1
        self.gravitySpeed = 10

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
        self.hit = 0

        self.pushS = False
        self.fall = 0

        self.slowMotionDelay = 0
        self.slowMotionCD = 0
        self.PushT = False

        self.DashCnt = 0
        self.DashDirX = 0
        self.DashDirY = 0
        self.DashCD = 0

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

        SPEED = game_framework.getSpeed(self.speed)

        if self.PushR and not self.collision(SPEED,0):
            self.posX += SPEED
            self.action = 1
        elif self.PushL and not self.collision(-1*SPEED,0):
            self.posX -= SPEED
            self.action = 0

        self.cameraX = player.posX - (width / 2)
        if self.cameraX <= 0:
            self.cameraX = 0
        elif size * len(stage[6]) - player.posX <= width/2:
            self.cameraX = size * len(stage[6]) - width

        if self.hit: #카메라 진동효과
            if player.PushL:
                self.cameraX -= 5
            elif player.PushR:
                self.cameraX += 5
            else: self.cameraX += 4
            if time.time() - self.hit > 0.05:self.hit = 0


        self.cameraY = max(0,self.posY-height+250)

    def down(self):

        if self.pushS and self.PushSpace:
            self.PushSpace = False
            if not self.collision(0,-20):
                self.posY -= 20

        # if self.fall > 0: self.fall = (self.fall +1) % 25

    def jump(self):
        if self.pushS: return

        SPEED = game_framework.getSpeed(self.jumpPower)
        J_SPEED = game_framework.getSpeed(5)

        if self.PushSpace:
            if self.jumpY == -1:
                self.jumpY = self.posY

            if self.posY < self.jumpY + self.jumpMax and not self.collision(0, SPEED):
                self.posY += SPEED
                self.speed = 16
                if self.jumpPower > 20: self.jumpPower -= J_SPEED
            else:
                self.PushSpace = False
                self.jumpY = -1
                self.speed = 12
                self.jumpPower = 40

    def Flash(self):
        for i in range(5):
            if self.PushR and not self.collision(35, 0):
                self.posX += 35
                self.action = 1
            elif self.PushL and not self.collision(-35, 0):
                self.posX -= 35
                self.action = 0
        self.OutOfMap()

    def DashGet(self,x,y):
        self.inv = time.time()-1
        self.DashCD = time.time()
        self.DashCnt = 25/game_framework.MS
        self.DashDirX = x
        self.DashDirY = y

    def Dash(self,x,y):
        if time.time() - self.DashCD > 5: self.DashCD = 0

        if self.DashCnt:
            SPEEDX = game_framework.getSpeed(self.speed * 5 )
            SPEEDY = game_framework.getSpeed(self.speed * 5 )
            rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi
            if not self.collision(SPEEDX * math.cos(rad * math.pi / 180), SPEEDY * math.sin(rad * math.pi / 180)):
                self.posX += SPEEDX * math.cos(rad / 360 * 2 * math.pi)
                self.posY += SPEEDY * math.sin(rad / 360 * 2 * math.pi)
            self.DashCnt -= 1
        else:
            self.DashDirX = 0
            self.DashDirY = 0



    def SlowMotion(self):
        if not self.PushT:return

        if self.slowMotionDelay == 0:
            self.slowMotionCD = 0
            game_framework.PIXEL_PER_METER /= 5
            game_framework.MS /= 5
            self.slowMotionDelay = time.time()

        if player.slowMotionDelay != 0 and time.time() - player.slowMotionDelay > 5:
            player.slowMotionDelay = 0
            game_framework.PIXEL_PER_METER *= 5
            game_framework.MS *= 5
            player.slowMotionCD = time.time()
            self.PushT = False

    def Gravity(self):
        if self.DashCnt : return
        if not self.PushSpace:

            SPEED = game_framework.getSpeed(self.gravitySpeed)
            G_SPEED = game_framework.getSpeed(5)

            if not self.collision(0, -SPEED):
                self.posY -= SPEED
                if self.gravitySpeed < 75:
                    self.gravitySpeed += G_SPEED
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
                    if self.DashCnt:continue

                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5 :# 가로줄 충돌
                         # if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                         #         self.posY - (y * size + (size/2)) + valY) < 30/2 + self.h / 2 -5:  # 세로줄 충돌
                         if abs(self.posY + valY - (self.h / 2) - (y * size + (size / 2))) < 8:
                             if abs((y * size + (size / 2)) - (self.posY - (self.h / 2))) < 8:  # 포지션 조정처리(끼임방지)
                                 self.posY = (y * size + (size / 2)) + 9 + (self.h / 2)

                             if abs((self.posY - self.h / 2) - (y * size + 50 + 15)) <= 15:  # 땅에 착지
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
                        self.inv = time.time()
                        return

    def invincibility(self):
        if self.inv == 0 : return

        if time.time() - self.inv < 2 :
            if self.hitframe == 0 : self.hitframe = 5
            else : self.hitframe = 0
        else :
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
    player.SlowMotion()
    player.Dash(player.DashDirX,player.DashDirY)
    player.OutOfMap()
    player.frame = (player.frame + 4 * 2 * game_framework.frame_time*game_framework.MS) % 4


