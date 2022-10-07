from sprite import Sprite
from Hero import player
from MapData import *
import random
import math

m_list = []

class Monster(Sprite):
    hp = 50
    maxhp = hp
    speed = 1.5
    mod = 1
    gravity = True

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
    cameraX = player.posX - (1200 / 2)
    #카메라가 맵밖을 촬영하지 않게 설정
    if cameraX <= 0: cameraX = 0
    elif size * len(stage[6]) - player.posX <= 600: cameraX = size * len(stage[6]) - 1200


    for monster in m_list:
        monster.Show(cameraX)

hoodman = Monster()
hoodman.posX = 1500
hoodman.posY = 1000
hoodman.w = 16*4
hoodman.h = 25*4
hoodman.i_w = 16*4
hoodman.i_h = 25*4
hoodman.action = 0
m_list.append(hoodman)