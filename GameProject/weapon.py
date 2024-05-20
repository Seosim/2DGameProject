import time

import pico2d

import game_framework
from sprite import Sprite
from Hero import player
import math
from mapData import Map, width, height
from cursor import aim
from particle import Particle


class Weapon(Sprite):
    def __init__(self):
        self.damage = 17
        self.speed = 35
        self.attack_speed = 0.5  # 공격속도
        self.attack_delay = 0  # 공격딜레이
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
        self.image = pico2d.load_image('./res/pistol.png')

        self.sound = pico2d.load_wav('./sound/pistol.wav')
        self.reloadSound = pico2d.load_wav('./sound/reload_p.wav')

    def radian(self, x, y):
        if self.action == 1:
            self.rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi
        else:
            self.rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi + 180

    def Show(self):
        if self.action == 1:
            self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX - player.cameraX, self.posY - player.cameraY,
                                   self.w, self.h)
        else:
            self.image.clip_composite_draw(self.i_w * int(self.frame), self.i_h * self.action, self.i_w, self.i_h,
                                           self.rad / 360 * 2 * math.pi,
                                           'h', self.posX - player.cameraX, self.posY - player.cameraY, self.w, self.h)

    def Shot(self):
        if (time.time() - self.attack_delay) < self.attack_speed: return

        if self.reloadDelay == 0:
            if self.ammo == 0:
                return

            player.shooting = time.time()
            gun.radian(aim.posX, aim.posY)
            b = Bullet()
            # b.imageLoad('./res/Bullet.png')
            if self.dir < 0: b.dir = -1
            bullet_list.append(b)
            self.sound.play()
            self.ammo -= 1
            self.attack_delay = time.time()
            player.vibration = self.damage

    def Reload(self):
        if self.R:
            if self.reloadDelay == 0:
                self.reloadSound.play()
                self.reloadDelay = time.time()
        else:
            return

        if self.reloadTime <= time.time() - self.reloadDelay:
            self.ammo = self.maxAmmo
            self.reloadDelay = 0
            self.R = False

    def DefDir(self, x):
        if player.screenX < x:
            self.action = 1
        else:
            self.action = 0

    def Update(self):
        self.Reload()
        self.dir = (-1 + (self.action * 2))
        self.posX = player.posX + self.dir * 15
        self.posY = player.posY - 15
        if player.clickButton: self.Shot()

    def CoolTimeSet(self, t):
        self.attack_delay += t
        if self.reloadDelay: self.reloadDelay += t


bullet_list = []


class Bullet(Sprite):
    image = pico2d.load_image('./res/Bullet.png')

    def __init__(self):
        self.speed = gun.speed
        self.rad = gun.rad
        self.posX = gun.posX
        self.posY = gun.posY
        self.spawnX = self.posX
        self.w = 15
        self.h = 5
        self.damage = gun.damage
        self.dir = 1

    def Show(self):
        self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX - player.cameraX, self.posY - player.cameraY,
                               self.w, self.h)

    def move(self):
        SPEED = game_framework.getSpeed(self.speed)

        if self.dir == 1:
            self.posX += SPEED * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY += SPEED * math.sin(self.rad / 360 * 2 * math.pi)
        else:
            self.posX -= SPEED * math.cos(self.rad / 360 * 2 * math.pi)
            self.posY -= SPEED * math.sin(self.rad / 360 * 2 * math.pi)

    def MakeParticle(self):
        p = Particle(self.posX, self.posY, "HitEffect", self.dir)
        p.addList()


def ShowBullet():
    for bullet in bullet_list:
        bullet.Show()


def UpdateBullet():
    for bullet in bullet_list:
        bullet.Show()
        bullet.move()

        if abs(bullet.posX - bullet.spawnX) > gun.distance or bullet.posY > 3000 or \
                bullet.posX > len(Map.stageData[Map.number][0]) * 100 or bullet.ColtoMap(0, 0):
            bullet_list.remove(bullet)
            del bullet
            continue

        # if bullet.ColtoBoss() and Map.number == 1:
        #     bullet_list.remove(bullet)
        #     continue


gun = Weapon()


def weaponInit():
    gun.__init__()
