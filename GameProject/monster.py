from sprite import Sprite
from Hero import player
import random

m_list = []

class Monster(Sprite):

    def __init__(self):
        self.hp = 50
        self.maxhp = self.hp
        self.speed = 1.5
        self.power = 3
        self.mod = 1
        self.gravity = True
        self.i_w = 16*4
        self.i_h = 25*4
        self.w = self.i_w
        self.h = self.i_h
        self.posX = random.randint(10,90)*100
        self.posY = 1000
        self.jumpY = -1
        self.jump = True


    def Gravity(self):
        if self.gravity:
            if not self.collision(0, -self.gravitySpeed) and not self.MonsterCol(0,-self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5
            else : self.jump = True

    def Hunting(self):
        dir = 0
        distance = abs(self.posX - player.posX)
        if distance < 500 and self.mod == 1 or self.maxhp != self.hp:
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
                self.Jump()
        else : self.action = 0
        if self.hp < self.maxhp/2 : self.speed = 3

    def Jump(self):
        if not self.jump:
            return

        if self.jumpY < 0:
            self.jumpY = self.posY

        if self.jumpY + 100  > self.posY and not self.collision(0,11) and self.jump and not self.MonsterCol(0,11):
            self.posY += 11
        else:
            self.jump = False
            self.jumpY = -1

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


def MonsterImage():
    for monster in m_list:
        monster.imageLoad('./res/hoodman.png')

def LoadMonster():
    for monster in m_list:
        monster.Update()
        monster.Show(player.cameraX)
        if monster.hp <= 0: m_list.remove(monster)


hoodman = Monster()
hoodman.posX = 500
hoodman.posY = 700
hoodman.action = 0

hood = [Monster() for i in range(10)]

m_list.append(hoodman)
m_list+=hood
