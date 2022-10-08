from sprite import Sprite
from Hero import player
from MapData import *
import random
import math

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


    def Gravity(self):
        if self.gravity:
            if not self.collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5

    def Hunting(self):
        dir = 0
        distance = abs(self.posX - player.posX)
        if distance < 500 and self.mod == 1 or self.maxhp != self.hp:
            if self.posX - player.posX > 0:
                self.action = 2
                dir = -1
            elif self.posX - player.posX < 0:
                self.action = 3
                dir = 1
            if not self.collision(dir* self.speed,0):
                self.posX += dir* self.speed
        else : self.action = 0

    def Update(self):
        self.Gravity()
        self.Hunting()




def LoadMonster():
    for monster in m_list:
        monster.Show(player.cameraX)
        if monster.hp <= 0: m_list.remove(monster)


hoodman = Monster()
hoodman.posX = 1500
hoodman.posY = 1000
hoodman.action = 0
m_list.append(hoodman)