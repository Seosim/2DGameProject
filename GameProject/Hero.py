from sprite import Sprite
from map import collision
import map

width = 1200
height = 700

class Player(Sprite):
    speed = 15
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

    def getScreenX(self):
        if width / 2 > self.posX: self.screenX = self.posX
        elif self.posX >= map.size * len(map.stage[6]) - width/2:
            self.screenX = width - (len(map.stage[6])*map.size-self.posX)
        else : self.screenX =  width / 2

    def Show(self):
        self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h, self.screenX,self.posY)
        self.frame = (self.frame + 0.1) % 4

    def move(self):
        if self.PushR and not collision(self.speed,0):
            self.posX += self.speed
            self.action = 1
        elif self.PushL and not collision(-1*self.speed,0):
            self.posX -= self.speed
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

def playerUpdate():
    player.Show()
    player.getScreenX()
    player.move()
    player.jump()
    player.Gravity()