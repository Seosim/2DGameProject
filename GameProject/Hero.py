from sprite import Sprite
from map import collision
import map

width = 1200
height = 700

class Player(Sprite):
    speed = 5
    jumpPower = 150
    hp = 100

    jumpY = -1
    gravitySpeed = 1

    PushR = False
    PushL = False
    PushSpace = False

    stand = True

    def __init__(self):
        pass

    def Show(self):
        if  width/2 > self.posX: # 맵 가장 왼쪽으로 가게된다면 플레이어가 맵에서 좌로 움직임
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h,self.posX,self.posY)
        elif self.posX >= map.size * len(map.stage[6]) - width/2: # 맵 가장 오른쪽으로 가게된다면 플레이어가 맵에서 우로 움직임
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h,width - (len(map.stage[6])*map.size-self.posX) ,self.posY)
        else :
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h, width / 2, self.posY)
        self.frame = (self.frame + 0.1) % 4

    def move(self):
        if self.PushR and not collision(self.speed,0):
            self.posX += self.speed
            self.frameCnt = 4
            self.action = 1
        elif self.PushL and not collision(-1*self.speed,0):
            self.posX -= self.speed
            self.frameCnt = 4
            self.action = 0

    def jump(self):
        if self.PushSpace:
            if self.jumpY == -1:
                self.jumpY = self.posY

            if self.posY < self.jumpY + self.jumpPower and not collision(0,10):
                self.posY += 10
            else:
                self.PushSpace = False
                self.jumpY = -1

    def Gravity(self):
        if not self.PushSpace:
           # if self.posY > 160 and not collision(0,-10): self.posY -= 10
            if not collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5

                #self.posY -= 10

            else: self.PushSpace = False




player = Player()

player.posX = 300
player.posY = 300
player.i_w = 16*4
player.i_h = 25*4
player.w = player.i_w
player.h = player.i_h

def playerUpdate():
    player.Show()
    player.move()
    player.jump()
    player.Gravity()