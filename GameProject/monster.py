from sprite import Sprite
from Hero import player
from MapData import *
import random

m_list = []

class Monster(Sprite):
    hp = 50
    speed = 5
    gravity = True

    def Gravity(self):
        if self.gravity:
            if not self.collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5


def LoadMonster():
    cameraX = player.posX - (1200 / 2)
    #카메라가 맵밖을 촬영하지 않게 설정
    if cameraX <= 0: cameraX = 0
    elif size * len(stage[6]) - player.posX <= 600: cameraX = size * len(stage[6]) - 1200


    for monster in m_list:
        monster.Show(cameraX)

clone = Monster()
clone.posX = random.randint(10,len(stage[6])-10) * 100
clone.posY = 1000
clone.w = 16*4
clone.h = 25*4
m_list.append(clone)