import pico2d

from sprite import Sprite
from Hero import player
import math
from monster import m_list
from boss import skul
from MapData import Map

width = 1200
height = 700

class Weapon(Sprite):

    def __init__(self):
        self.cameraX = player.posX - (1200 / 2)
        self.damage = 10
        self.attack_speed = 30
        self.dir = 1
        self.rad = 0

        self.posX = player.posX
        self.posY = player.posY
        self.w = 50
        self.h = 50
        self.i_w = 48
        self.i_h = 48
        self.delay = 0
        self.clickButton = False
        self.distance = 500
        self.ammo = 8
        self.maxAmmo = self.ammo
        self.reloadDelay = 0
        self.reloadTime = 50
        self.R = False


    def radian(self,x,y):
        if self.action == 1:
            self.rad = math.atan2((height-y)-self.posY+ player.cameraY,x-player.screenX)*180/math.pi
        else :
            self.rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi + 180

    def Show(self):
        self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX-player.cameraX, self.posY-player.cameraY, self.w, self.h)

    def Shot(self):
        if self.delay == 0 and self.reloadDelay == 0:
            if self.ammo == 0:
                return
            b = Bullet()
            #b.imageLoad('./res/Bullet.png')
            if self.dir < 0: b.dir = 0
            bullet_list.append(b)
            self.delay = 1
            self.ammo -= 1

    def Reload(self):
        if self.R :
            self.reloadDelay += 1
        else: return

        if self.reloadTime == self.reloadDelay:
            self.ammo = self.maxAmmo
            self.reloadDelay = 0
            self.R = False

    def DefDir(self,x):
        if player.screenX < x:
            self.imageLoad('./res/pistolR.png')
            self.action = 1
        else :
            self.imageLoad('./res/pistolL.png')
            self.action = 0


    def Update(self):
        self.Reload()
        self.dir = (-1 + (self.action * 2))
        self.cameraX = player.posX - (1200 / 2)
        self.posX = player.posX + self.dir*15
        self.posY = player.posY - 15
        if self.delay: self.delay = (self.delay +1) % self.attack_speed
        if self.clickButton: self.Shot()

bullet_list = []

class Bullet(Sprite):
    image = pico2d.load_image('./res/Bullet.png')
    def __init__(self):
        self.speed = 30
        self.rad = gun.rad
        self.dir = 1
        self.posX = gun.posX
        self.posY = gun.posY
        self.spawnX = self.posX
        self.w = 15
        self.h = 5
        self.damage = gun.damage


    def Show(self):
        self.image.rotate_draw(self.rad / 360*2*math.pi,self.posX-player.cameraX,self.posY-player.cameraY,self.w,self.h)

    def move(self):
        if self.dir == 1:
            self.posX += self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += self.speed * math.sin(self.rad / 360 * 2 * math.pi)
        else:
            self.posX -= self.speed * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY -= self.speed * math.sin(self.rad / 360 * 2 * math.pi)

    def ColtoMonster(self,mlist):
        for monster in mlist:
            if abs(self.posX - monster.posX) < (monster.w/2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - monster.posY) < (monster.h / 2) + (self.h / 2)-15:  # 세로줄 충돌
                    monster.hp -= self.damage
                    # print('monster hp :' , monster.hp)
                    return True
        return False

    def ColtoGhost(self):
        for s in skul.s_list:
            if abs(s.posX - self.posX) < (s.w / 2) \
                and abs(s.posY - self.posY) < (s.h/2) :
                s.col = True
                return True

def ShowBullet():
    for bullet in bullet_list:
        bullet.Show()

def UpdateBullet():
    for bullet in bullet_list:
        bullet.Show()
        bullet.move()
        bullet.ColtoGhost()

        if abs(bullet.posX - bullet.spawnX) > gun.distance:
            bullet_list.remove(bullet)
            continue
        if bullet.posY > 3000:
            bullet_list.remove(bullet)
            continue
        if bullet.posX> len(Map.stageData[Map.number][0])*100:
            bullet_list.remove(bullet)
            continue
        if bullet.collision(0,0):
            bullet_list.remove(bullet)
            continue
        if bullet.ColtoMonster(m_list):
            bullet_list.remove(bullet)
            continue
        if bullet.ColtoGhost():
            bullet_list.remove(bullet)
            continue

gun = Weapon()

def weaponInit():
    gun.__init__()
    gun.imageLoad('./res/pistolR.png')








