from sprite import Sprite
from Hero import player
import random
import math



class Monster(Sprite):

    def __init__(self):
        self.hp = 50
        self.maxhp = self.hp
        self.speed = 1.5
        self.maxSpeed = 3
        self.power = 3
        self.gravity = True
        self.posX = random.randint(10,90)*100
        self.posY = 1000
        self.jumpY = -1
        self.jump = True


    def Gravity(self):
        if not self.collision(0, -self.gravitySpeed) and not self.MonsterCol(0, -self.gravitySpeed):
            self.posY -= self.gravitySpeed
            if self.gravitySpeed < 10:
                self.gravitySpeed += 0.5
        else:
            self.jump = True

    def MonsterCol(self,x,y):
        cnt = 0
        for m in m_list:
            if abs(self.posX - m.posX + x) <= (self.w/2) + (m.w /2):
                if abs(self.posY - m.posY + y) <= (self.h/2) + (m.h /2):
                    cnt += 1
            if cnt > 1 : return True
        return False

    def Update(self):
        self.Gravity()
        self.Hunting()


class Melee(Monster):
    value = 1

    i_w = 16*4
    i_h = 25*4
    w = i_w
    h = i_h
    def Hunting(self):
        dir = 0
        distance = abs(self.posX - player.posX)
        if distance < 500 or self.maxhp != self.hp:
            if self.posX - player.posX > 5:
                self.action = 2
                dir = -1
            elif self.posX - player.posX <= -5:
                self.action = 3
                dir = 1

            if not self.collision(dir* self.speed,0):
                if not self.MonsterCol(dir* self.speed,0):
                    self.posX += dir* self.speed
            else : # 점프 조건
                self.Jump(11)
        else : self.action = 0
        if self.hp < self.maxhp/2 : self.speed = 3

    def Jump(self,s):
        if not self.jump:
            return

        if self.jumpY < 0:
            self.jumpY = self.posY

        if self.jumpY + 100  > self.posY and not self.collision(0,s) and self.jump and not self.MonsterCol(0,s):
            self.posY += s
        else:
            self.jump = False
            self.jumpY = -1




class Archer(Monster):
    i_w = 25 * 4
    i_h = 25 * 4
    w = i_w
    h = i_h
    shootDelay = 0
    value = 2
    rad = 0
    dir = 0
    def Hunting(self):
        if abs(self.posX - player.posX) < 500 or self.maxhp != self.hp :
            if self.posX - player.posX > 5 and 3.1>self.frame > 3.0:
                self.action = 2
                self.Shooting()
            elif self.posX - player.posX <= -5 and 3.1>self.frame > 3.0:
                self.action = 3
                self.Shooting()
            self.shootDelay = (self.shootDelay + 1) % 100
        else :
            self.action = 0
            self.shootDelay = 0

    def Shooting(self):
        if self.action == 2:
            self.dir = -1
            self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi + 180
        elif self.action ==3:
            self.dir = 1
            self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi
        arrow = Arrow(self.posX,self.posY,self.power,self.rad,self.dir)

        arrow.imageLoad('./res/bullet.png')
        a_list.append(arrow)

    def Show(self,x):
        self.image.clip_draw(self.i_w*int(self.frame),self.i_h*self.action,self.w,self.h,self.posX - x,self.posY)
        self.frame = (self.frame+0.1) % 4


class Arrow(Sprite):
    def __init__(self,px,py,dmg,rad,dir):
        self.speed = 7
        self.dir = dir
        self.rad = rad
        self.posX = px
        self.posY = py
        self.spawnX = self.posX
        self.w = 10
        self.h = 10
        self.power = dmg


    def Show(self):
        self.image.clip_draw(self.i_w*int(self.frame),self.i_h*self.action,self.w,self.h,self.posX - player.cameraX,self.posY)

    def move(self):
        if self.dir == 1:
            self.posX += self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += self.speed * math.sin(self.rad / 360 * 2 * math.pi)
        else:
            self.posX -= self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY -= self.speed * math.sin(self.rad / 360 * 2 * math.pi)


def MonsterImage():
    for monster in m_list:
        if monster.value == 1:
            monster.imageLoad('./res/hoodman.png')
        else :
            monster.imageLoad('./res/archer.png')

def LoadMonster():
    for monster in m_list:
        monster.Update()
        monster.Show(player.cameraX)
        if monster.hp <= 0: m_list.remove(monster)

def LoadArrow():
    for a in a_list:
        a.move()
        a.Show()

        if a.posY > 700 :
            a_list.remove(a)
            continue
        if a.collision(0,0) :
            a_list.remove(a)
            continue
        if abs(a.posX - player.posX) < player.w/2:
            if abs(a.posY - player.posY) < player.h/2:
                if player.inv == 0:
                    player.hp -= a.power
                    player.inv = 2
                    print('hit')
                a_list.remove(a)
                continue

m_list = []
a_list = []

hood = [Melee() for i in range(10)]
m_list+=hood

archer = [Archer() for i in range(5)]
m_list+=archer
