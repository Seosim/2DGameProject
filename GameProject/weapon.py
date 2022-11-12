import time

import pico2d

import game_framework
from sprite import Sprite
from Hero import player
import math
from monster import m_list
from boss import Belial
from MapData import Map , width,height
from cursor import aim

class Weapon(Sprite):

    def __init__(self):
        self.cameraX = player.posX - (1200 / 2)
        self.damage = 10
        self.speed = 35
        self.attack_speed = 0.5 #공격속도
        self.attack_delay = 0 #공격딜레이
        self.dir = 1
        self.rad = 0

        self.posX = player.posX
        self.posY = player.posY
        self.w = 50
        self.h = 50
        self.i_w = 48
        self.i_h = 48
        self.distance = 500
        self.ammo = 8
        self.maxAmmo = self.ammo
        self.reloadDelay = 0
        self.reloadTime = 1
        self.R = False

        self.sound = pico2d.load_wav('./sound/pistol.wav')


    def radian(self,x,y):
        if self.action == 1:
            self.rad = math.atan2((height-y)-self.posY+ player.cameraY,x-player.screenX)*180/math.pi
        else :
            self.rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi + 180

    def Show(self):
        self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX-player.cameraX, self.posY-player.cameraY, self.w, self.h)

    def Shot(self):
        if (time.time() - self.attack_delay) < self.attack_speed: return

        if self.reloadDelay == 0:
            if self.ammo == 0:
                return

            player.shooting = time.time()
            gun.radian(aim.posX,aim.posY)
            b = Bullet()
            #b.imageLoad('./res/Bullet.png')
            if self.dir < 0: b.dir = 0
            bullet_list.append(b)
            self.sound.play()
            self.ammo -= 1
            self.attack_delay = time.time()

    def Reload(self):
        if self.R:
            if self.reloadDelay == 0:
                self.reloadDelay = time.time()
        else: return

        if self.reloadTime <= time.time() - self.reloadDelay:
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
        #if self.attack_delay: self.attack_delay = (self.attack_delay + 1) % self.attack_speed
        if player.clickButton: self.Shot()

bullet_list = []

class Bullet(Sprite):
    image = pico2d.load_image('./res/Bullet.png')
    def __init__(self):
        self.speed = gun.speed
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
        SPEED = game_framework.getSpeed(self.speed)

        if self.dir == 1:
            self.posX += SPEED * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += SPEED * math.sin(self.rad / 360 * 2 * math.pi)
        else:
            self.posX -= SPEED * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY -= SPEED * math.sin(self.rad / 360 * 2 * math.pi)

    def ColtoMonster(self,mlist):
        for monster in mlist:
            if abs(self.posX - monster.posX) < (monster.w/2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - monster.posY) < (monster.h / 2) + (self.h / 2)-15:  # 세로줄 충돌
                    monster.hp -= self.damage
                    # print('monster hp :' , monster.hp)
                    return True
        return False

    def ColtoBoss(self):
        if abs(self.posX - Belial.posX)+150 < (Belial.w / 2) + (self.w / 2):  # 가로줄 충돌
            if Belial.action == 0:
                if self.posY == pico2d.clamp(130,self.posY,650):  # 세로줄 충돌
                    Belial.hp -= self.damage
                    return True
            elif Belial.action == 1:
                if self.posY == pico2d.clamp(130,self.posY,750):  # 세로줄 충돌
                    Belial.hp -= self.damage
                    return True

def ShowBullet():
    for bullet in bullet_list:
        bullet.Show()

def UpdateBullet():
    for bullet in bullet_list:
        bullet.Show()
        bullet.move()

        if abs(bullet.posX - bullet.spawnX) > gun.distance or bullet.posY > 3000 or \
                bullet.posX> len(Map.stageData[Map.number][0])*100 or bullet.collision(0,0) or\
                bullet.ColtoMonster(m_list) :
            bullet_list.remove(bullet)
            del bullet
            continue

        if bullet.ColtoBoss() and Map.number == 1:
            bullet_list.remove(bullet)
            continue

gun = Weapon()

def weaponInit():
    gun.__init__()
    gun.imageLoad('./res/pistolR.png')








