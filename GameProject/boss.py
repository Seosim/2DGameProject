import pico2d
from sprite import Sprite
import random
from Hero import player
import math

class Boss(Sprite):
    def __init__(self):
        self.image = pico2d.load_image('./res/Skull.png')
        self.hp = 1000
        self.i_w = 510
        self.i_h = 0
        self.posX = 600
        self.posY = 400
        self.w = 510
        self.h = 558
        self.l_hand = Sprite()
        self.r_hand = Sprite()
        self.ldir = 250
        self.rdir = 250
        self.skillDelay = 0
        self.s_list = []

    def UpdateHand(self):
        self.ldir = random.randint(100,500)
        self.rdir = random.randint(100,500)

    def MoveHand(self):
        if self.ldir > self.l_hand.posY : self.l_hand.posY += 1
        elif  self.ldir < self.l_hand.posY : self.l_hand.posY -= 1

        if self.rdir > self.r_hand.posY : self.r_hand.posY += 1
        elif  self.rdir < self.r_hand.posY : self.r_hand.posY -= 1

    def CreateGhost(self):
        s = [Ghost() for i in range(5)]
        self.s_list += s



    def update(self):
        self.MoveHand()
        self.skillDelay += 1
        self.frame = (self.frame+ 0.05) % 2
        if self.skillDelay % 300 == 0:
            self.UpdateHand()
        if self.skillDelay % 500 == 0:
            self.CreateGhost()
        for s in self.s_list:
            s.update()


    def Draw(self):
        self.Show(player.cameraX)
        self.r_hand.image.clip_composite_draw(0,0,self.r_hand.w,self.r_hand.h,0,'h',self.r_hand.posX-player.cameraX,self.r_hand.posY,\
                                              self.r_hand.w,self.r_hand.h)
        self.l_hand.Show(player.cameraX)

        for s in self.s_list:
            s.Show(player.cameraX)

skul = Boss()

class Ghost(Sprite):
    def __init__(self):
        self.image = pico2d.load_image('./res/Ghost.png')
        self.w = 30
        self.h = 30
        self.posX = random.randint(200,1000)
        self.posY = random.randint(200,1000)
        self.damage = 5
        self.ready = 0
        self.rad = 0
        self.dir = 0
        self.speed = 5

    def update(self):
        self.ready += 1
        self.setRad()
        self.Attack()

    def setRad(self):
            if self.posX > player.posX: #우측
                self.dir = -1
                self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi  # + 180
            elif self.posX <= player.posX: #좌측
                self.dir = 1
                self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi

    def Attack(self):
        if self.ready > 250:
            self.posX += self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += self.speed * math.sin(self.rad / 360 * 2 * math.pi)


def InitBoss():
    skul.l_hand.imageLoad('./res/Lhand.png')
    skul.r_hand.imageLoad('./res/Lhand.png')
    skul.l_hand.i_w = 111
    skul.r_hand.i_w = 111
    skul.l_hand.i_h = 0
    skul.r_hand.i_h = 0
    skul.l_hand.w =  111
    skul.l_hand.h = 102
    skul.r_hand.w =  111
    skul.r_hand.h = 102
    skul.l_hand.posX = skul.posX - 300
    skul.r_hand.posX = skul.posX + 300





