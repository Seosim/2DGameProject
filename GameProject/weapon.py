from sprite import Sprite
from Hero import player
import math

width = 1200
height = 700

class Weapon(Sprite):
    cameraX = player.posX - (1200 / 2)
    damage = 10
    attack_speed = 50
    dis = 15
    rad = 0

    def __init__(self):
        self.posX = player.posX
        self.posY = player.posY
        self.w = 50
        self.h = 50
        self.i_w = 48
        self.i_h = 48

    def radian(self,x,y):
        if self.action == 1:
            self.rad = math.atan2((height-y)-self.posY,x-player.screenX)*180/math.pi
        else :
            self.rad = math.atan2((height - y) - self.posY, x - player.screenX) * 180 / math.pi + 180

    def Show(self):
        self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX + self.dis, self.posY, self.w, self.h)

    def DefDir(self,x):
        if player.screenX < x:
            self.imageLoad('./res/pistolR.png')
            self.action = 1
        else :
            self.imageLoad('./res/pistolL.png')
            self.action = 0


    def Update(self):
        self.dis = 15 * (-1 + (self.action * 2))
        self.cameraX = player.posX - (1200 / 2)
        self.posX = player.screenX
        self.posY = player.posY - 15
        self.Show()

gun = Weapon()






