import pico2d
from sprite import Sprite
from Hero import player
from MapData import Map

import random
import math

class Boss(Sprite):
    def __init__(self):
        self.image = pico2d.load_image('./res/belial.png')
        self.hp = 50
        self.i_w = 100
        self.i_h = 130
        self.posX = 600
        self.posY = 500
        self.w = self.i_w*5
        self.h = self.i_h*5
        self.l_hand = Sprite()
        self.r_hand = Sprite()
        self.ldir = 250
        self.rdir = 250
        self.skillDelay = 0
        self.action = 1
        self.s_list = []
        self.e_list = []

        self.ignore = False

    def UpdateHand(self):
        self.ldir = player.posY
        self.rdir = player.posY

    def MoveHand(self):
        if self.ldir > self.l_hand.posY +10: self.l_hand.posY += 10
        elif  self.ldir < self.l_hand.posY : self.l_hand.posY -= 10

        if self.rdir > self.r_hand.posY + 10 : self.r_hand.posY += 10
        elif  self.rdir < self.r_hand.posY : self.r_hand.posY -= 10

    def CreateGhost(self):
        s = [Ghost() for i in range(20)]
        self.s_list += s
        del s

    def Breath(self):
        e = [EBall(self.posX,self.posY,(self.skillDelay//2) + 180*i) for i in range(2)]
        self.e_list += e
        del e

    def update(self):
        if Map.number != 1: return

        for s in self.s_list:
            s.update()
            if s.ready >400 or s.col:
                self.s_list.remove(s)

        for e in self.e_list:
            e.update()
            if e.timer > 100: self.e_list.remove(e)

        if len(skul.s_list): shield.update()

        if self.hp <= 0: return

        self.MoveHand()
        self.skillDelay += 1
        self.frame = (self.frame+ 0.1) % 4
        if self.skillDelay % 5 == 0:
            self.Breath()
        if self.skillDelay % 300 == 0:
            self.UpdateHand()
        if self.skillDelay % 500 == 0:
            self.CreateGhost()




    def Draw(self):
        if Map.number != 1: return

        self.Show(player.cameraX,player.cameraY)

        if self.hp > 0:
            self.r_hand.image.clip_composite_draw(0,0,self.r_hand.w,self.r_hand.h,0,'h',self.r_hand.posX-player.cameraX,self.r_hand.posY-player.cameraY,\
                                                  self.r_hand.w,self.r_hand.h)
            self.l_hand.Show(player.cameraX,player.cameraY)

        for s in self.s_list:
            s.Show(player.cameraX,player.cameraY)

        for e in self.e_list:
            e.Show(player.cameraX, player.cameraY)

        if len(skul.s_list): shield.Show(player.cameraX,player.cameraY)

class Ghost(Sprite):
    image = None
    def __init__(self):
        if Ghost.image == None:
            Ghost.image = pico2d.load_image('./res/Ghost.png')
        self.w = 50
        self.h = 50
        self.i_w = 25
        self.i_h = 25
        self.posX = random.randint(50,1150)
        self.posY = random.randint(100,650)
        self.damage = 1
        self.ready = 0
        self.rad = 0
        self.dir = 0
        self.speed = 8
        self.action = 0
        self.col = False

    def update(self):
        self.ready += 1
        self.frame = (self.frame+0.1) % 4
        if self.ready >= 150:
            self.setRad()
        self.Attack()
        self.hit()

    def hit(self):
        if self.ready <= 150: return

        if abs(self.posX - player.posX) < player.w/2:
            if abs(self.posY - player.posY) < player.h/2:
                if player.inv == 0:
                    if not skul.ignore:
                        player.hp -= self.damage
                self.col = True

    def setRad(self):
            if self.posX > player.posX: #우측
                self.dir = -1
                self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi  # + 180
            elif self.posX <= player.posX: #좌측
                self.dir = 1
                self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi

    def Attack(self):
        if self.ready > 150:
            self.posX += self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += self.speed * math.sin(self.rad / 360 * 2 * math.pi)

class EBall(Sprite):
    image = None

    def __init__(self,x,y,r):
        if EBall.image == None:
            EBall.image = pico2d.load_image('./res/DarkBall.png')

        self.posX = random.randint(-30+x,x+30)
        self.posY = random.randint(-130+y,y-100)
        self.toX = random.randint(-5,5)
        self.damage = 7
        self.i_w =45
        self.i_h =45
        self.w = 50
        self.h = 50
        self.action = 0
        self.rad = r
        self.timer = 0

    def move(self):
        self.posX += 15 * math.cos(self.rad * math.pi /180)
        self.posY += 15 * math.sin(self.rad * math.pi /180)

        # self.posX += self.toX
        # self.posY -= 5

        self.timer += 1
        if self.timer > 500 or self.posY < -10: del self

    def hit(self):
        if abs(self.posX - player.posX) < player.w/2:
            if abs(self.posY - player.posY) < player.h/2:
                if player.inv == 0:
                    player.hp -= self.damage
                    player.inv = 2

    def update(self):
        self.move()
        self.hit()

class Shield(Sprite):
    image = None

    def __init__(self):
        if Shield.image == None:
            Shield.image = pico2d.load_image('./res/Shield.png')
            self.posX = 600
            self.posY = 600
            self.i_w= 29
            self.i_h=17
            self.w = 200
            self.h = 100
            self.action = 0

    def SavePlayer(self):
            skul.ignore = False

            if abs(self.posX - player.posX) < self.w/2:
                if abs(self.posY - player.posY) < self.h/2:
                    skul.ignore = True


    def update(self):
        self.frame = (self.frame+0.05) % 2
        self.SavePlayer()


skul = Boss()
shield = Shield()

def InitBoss():

    if Map.number != 1: return

    skul.__init__()
    skul.l_hand.imageLoad('./res/belial_hand.png')
    skul.r_hand.imageLoad('./res/belial_hand.png')
    skul.l_hand.i_w = 111
    skul.r_hand.i_w = 111
    skul.l_hand.i_h = 102
    skul.r_hand.i_h = 102
    skul.l_hand.w =  200
    skul.l_hand.h = 200
    skul.r_hand.w =  200
    skul.r_hand.h = 200
    skul.l_hand.posX = skul.posX - 400
    skul.r_hand.posX = skul.posX + 400
    skul.l_hand.action = 0






