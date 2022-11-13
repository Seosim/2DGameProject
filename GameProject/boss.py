import pico2d
import game_framework
import gameover_state

from sprite import Sprite
from Hero import player
from weapon import bullet_list
from MapData import Map,width,height


import random
import math
import time

class Boss(Sprite):
    def __init__(self):
        self.image = pico2d.load_image('./res/belial.png')
        self.hp = 30
        self.i_w = 100
        self.i_h = 130
        self.posX = width/2
        self.posY = 500
        self.w = self.i_w*5
        self.h = self.i_h*5
        self.l_hand = Sprite()
        self.r_hand = Sprite()
        self.handTimer = 0
        self.ldir = 250
        self.rdir = 250
        self.skillDelay = 0
        self.action = 0
        self.s_list = []
        self.e_list = []
        self.beam = Beam()
        self.ignore = False
        self.dead = False

        self.debugSkill = 0

    def UpdateHand(self):
        self.ldir = player.posY
        self.rdir = player.posY
        self.l_hand.action = 1
        self.r_hand.action = 1
        self.handTimer = time.time()

    def MoveHand(self):

        SPEED = game_framework.getSpeed(10)

        if self.ldir > self.l_hand.posY +SPEED: self.l_hand.posY += SPEED
        elif  self.ldir < self.l_hand.posY : self.l_hand.posY -= SPEED

        if self.rdir > self.r_hand.posY + SPEED : self.r_hand.posY += SPEED
        elif  self.rdir < self.r_hand.posY : self.r_hand.posY -= SPEED
        else:
            if self.r_hand.action:
                self.beam.setBeam(self.l_hand.posY,self.r_hand.posX-self.l_hand.posX)
                return
        self.beam.timer = 0
        self.beam.on = False

    def CreateGhost(self):

        s = [Ghost() for i in range(20)]
        self.s_list += s
        del s

    def Breath(self):
        e = [EBall(self.posX,self.posY,(20*i)) for i in range(18)]
        self.e_list += e
        del e

    def Dead(self):
        if self.dead : return

        if self.action == 0:
            self.frame = 1
        elif self.action == 1 :
            self.frame = 0
        self.action = 2
        self.frame = 1
        self.dead = True
        self.e_list.clear()
        self.s_list.clear()
        self.beam.on = False
        game_framework.push_state(gameover_state)

    def ColtoBullet(self):
        for b in bullet_list:
            if abs(self.posX - b.posX) + 150 < (b.w / 2) + (self.w / 2):  # 가로줄 충돌
                if self.action == 0:
                    if self.posY == pico2d.clamp(130, self.posY, 650):  # 세로줄 충돌
                        self.hp -= b.damage
                        bullet_list.remove(b)
                        return True
                elif self.action == 1:
                    if b.posY == pico2d.clamp(130, b.posY, 750):  # 세로줄 충돌
                        self.hp -= b.damage
                        bullet_list.remove(b)
                        return True

    def handAnimation(self):
        if self.handTimer :
            self.l_hand.action = 1
            self.r_hand.action = 1
        else :
            self.l_hand.action = 0
            self.r_hand.action = 0

        if time.time() - self.handTimer > 5:
            self.handTimer =0

    def update(self):
        if Map.number != 1: return

        if self.skillDelay == 0: self.skillDelay = time.time()

        for s in self.s_list:
            s.update()
            if time.time() - s.ready > 6 or s.col:
                self.s_list.remove(s)

        for e in self.e_list:
            e.update()
            if time.time() - e.timer > 3/game_framework.MS: self.e_list.remove(e)

        self.beam.hit()

        if len(self.s_list): shield.update()

        self.handAnimation()

        if len(self.e_list): self.action = 1
        else : self.action = 0

        if self.hp <= 0:
            self.Dead()
            if self.posY > self.h/2 + 50: self.posY -= 1
            return

        self.UseSkill()
        self.FrameUpdate()
        self.ColtoBullet()

    def FrameUpdate(self):
        self.frame = (self.frame + 4 * 2 * game_framework.frame_time) % 4
        self.l_hand.frame = (self.l_hand.frame + 4 * 2 * game_framework.frame_time) % 4
        self.r_hand.frame = (self.r_hand.frame + 4 * 2 * game_framework.frame_time) % 4

    def UseSkill(self):
        if time.time() - self.skillDelay > 5/game_framework.MS:
            rSkill = random.randint(0, 2)

            rSkill = self.debugSkill
            self.debugSkill = (self.debugSkill +1) % 3

            if rSkill == 0:
                self.Breath()
            if rSkill == 1:
                self.UpdateHand()
            if rSkill == 2:
                self.CreateGhost()
            self.skillDelay = 0
        self.MoveHand()

    def Draw(self):
        if Map.number != 1: return

        if len(Belial.s_list): shield.Show(player.cameraX, player.cameraY)

        self.Show(player.cameraX,player.cameraY)

        if self.hp > 0:
            self.l_hand.Show(player.cameraX,player.cameraY)
            self.r_hand.flipShow(player.cameraX,player.cameraY)

        for s in self.s_list:
            s.Show(player.cameraX,player.cameraY)

        for e in self.e_list:
            e.Show(player.cameraX, player.cameraY)

        if self.handTimer and self.beam.on:
            self.beam.Show(player.cameraX,player.cameraY)

    def CoolTimeSet(self,t):
        self.handTimer += t
        self.skillDelay += t
        for s in self.s_list:
            s.ready += t
        for e in self.e_list:
            e.timer += t


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
        self.damage = 2
        self.ready = time.time()
        self.rad = 0
        self.dir = 0
        self.speed = 20
        self.frame = random.randint(0,3)
        self.action = 0
        self.col = False

    def update(self):
        self.frame = (self.frame+ 4*2*game_framework.frame_time) % 4
        if self.ready >= 150:
            self.setRad()
        self.Attack()
        self.hit()

    def hit(self):
        if time.time() - self.ready <= 2: return

        if abs(self.posX - player.posX) < player.w/2:
            if abs(self.posY - player.posY) < player.h/2:
                if player.inv == 0:
                    if not Belial.ignore:
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
        if time.time() - self.ready > 2:

            SPEED =game_framework.getSpeed(self.speed)

            self.posX += SPEED * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += SPEED * math.sin(self.rad / 360 * 2 * math.pi)

class EBall(Sprite):
    image = None

    def __init__(self,x,y,r,Size = 50):
        if EBall.image == None:
            EBall.image = pico2d.load_image('./res/DarkBall.png')

        self.posX = x + 50* math.cos(r* math.pi /180)
        self.posY = y + 50* math.sin(r* math.pi /180) - 125
        self.toX = random.randint(-5,5)
        self.damage = 25
        self.i_w =45
        self.i_h =45
        self.w = Size
        self.h = Size
        self.action = 0
        self.rad = r
        self.timer = time.time()

    def move(self):
        if time.time() - self.timer < 1: return

        SPEED = game_framework.getSpeed(20)

        self.posX += SPEED * math.cos(self.rad * math.pi /180)
        self.posY += SPEED * math.sin(self.rad * math.pi /180)


    def hit(self):
        if time.time() - self.timer < 1/game_framework.MS:return

        if abs(self.posX - player.posX) < player.w/2:
            if abs(self.posY - player.posY) < player.h/2:
                if player.inv == 0:
                    player.hp -= self.damage
                    player.inv = time.time()

    def update(self):
        self.move()
        self.hit()

class Shield(Sprite):
    image = None

    def __init__(self):
        if Shield.image == None:
            Shield.image = pico2d.load_image('./res/Shield.png')
            self.posX = width/2
            self.posY = 215
            self.i_w= 29
            self.i_h=17
            self.w = 200
            self.h = 100
            self.action = 0

    def SavePlayer(self):
            Belial.ignore = False

            if abs(self.posX - player.posX) < self.w/2:
                if abs(self.posY - player.posY) < self.h/2:
                    Belial.ignore = True


    def update(self):
        self.frame = (self.frame+0.05) % 2
        self.SavePlayer()

class Beam(Sprite):
    image = None
    def __init__(self):
        if Beam.image == None:
            Beam.image = pico2d.load_image('./res/EnergyBeam.png')
        self.i_w = 175
        self.i_h = 43
        self.w = 800
        self.h = 150
        self.posX = width/2
        self.posY = -100
        self.on = False
        self.frame = 0
        self.action = 0
        self.timer = 0

    def setBeam(self,y,w):
        self.w = w
        self.posY = y
        self.action = (self.action + 4 * 2 * game_framework.frame_time) % 4
        if self.timer == 0 :self.timer = time.time()
        if time.time() - self.timer > 0.7:
            self.on = True

    def hit(self):
        if self.on :
            if abs(self.posX - player.posX) < (self.w+player.w)/2:
                if abs(self.posY - player.posY) < (self.h+player.h)/2:
                    player.hit(15,1)





Belial = Boss()
shield = Shield()

def InitBoss():

    if Map.number != 1: return

    Belial.__init__()
    Belial.l_hand.imageLoad('./res/belial_hand.png')
    Belial.r_hand.imageLoad('./res/belial_hand.png')
    Belial.l_hand.i_w = 58
    Belial.r_hand.i_w = 58
    Belial.l_hand.i_h = 67
    Belial.r_hand.i_h = 67
    Belial.l_hand.w =  200
    Belial.l_hand.h = 200
    Belial.r_hand.w =  200
    Belial.r_hand.h = 200
    Belial.l_hand.posX = Belial.posX - 550
    Belial.r_hand.posX = Belial.posX + 550
    Belial.l_hand.action = 0
    Belial.r_hand.action = 0






