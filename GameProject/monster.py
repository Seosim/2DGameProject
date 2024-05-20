import pico2d
import game_framework
import time
import json

from sprite import Sprite
from Hero import player
import random
import math
from mapData import Map
from weapon import bullet_list
from item import *


class Monster(Sprite):

    def __init__(self, x, y):
        self.hp = 50
        self.maxhp = self.hp
        self.speed = 6
        self.maxSpeed = 3
        self.power = 15
        self.gravity = True
        self.posX = x
        self.posY = y
        self.jumpY = -1
        self.jump = False
        self.falling = True

    def Gravity(self):
        SPEED = game_framework.getSpeed(self.gravitySpeed)
        G_SPEED = game_framework.getSpeed(5)

        if not self.ColtoMap(0, -SPEED) and not self.MonsterCol(0, -SPEED) and self.falling:
            self.posY -= SPEED
            self.falling = True
            if self.gravitySpeed < 75:
                self.gravitySpeed += G_SPEED
        else:
            self.jump = True
            self.falling = True
            self.jumpY = -1

    def MonsterCol(self, x, y):
        cnt = 0
        for m in m_list:
            if m.value != 1: continue
            if abs(self.posX - m.posX + x) <= (self.w / 2) + (m.w / 2):
                if abs(self.posY - m.posY + y) <= (self.h / 2) + (m.h / 2):
                    cnt += 1
            if cnt > 1: return True
        return False

    def ColtoBullet(self):
        for b in bullet_list:
            if abs(self.posX - b.posX) < (b.w / 2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - b.posY) < (b.h / 2) + (self.h / 2) - 15:  # 세로줄 충돌
                    self.hp -= b.damage
                    b.MakeParticle()
                    bullet_list.remove(b)
                    return True
        return False

    def DropItem(self):
        Rnum = random.randint(1, 100)
        item = None
        if Rnum == 100:
            item = Item_W(self.posX, self.posY, 2)
            item.addList()
        elif 96 <= Rnum <= 99:
            item = Item_W(self.posX, self.posY, 1)
            item.addList()
        elif 90 <= Rnum <= 95:
            item = Item_W(self.posX, self.posY, 3)
            item.addList()
        elif Rnum < 7:
            item = Item_HP(self.posX, self.posY)
            item.addList()

    def Update(self):
        self.Gravity()
        self.Hunting()
        self.OutOfMap()
        self.ColtoBullet()

        if self.hp <= 0:
            self.DropItem()
            m_list.remove(self)

class Melee(Monster):
    value = 1

    i_w = 16 * 4
    i_h = 25 * 4
    w = i_w
    h = i_h

    image = pico2d.load_image('./res/Hoodman.png')

    def Hunting(self):
        SPEED = game_framework.getSpeed(self.speed)
        self.frame = (self.frame + 4 * 2 * game_framework.frame_time * game_framework.MS) % 4

        dir = 0
        distanceX = abs(self.posX - player.posX)
        distanceY = abs(self.posY - player.posY)
        if (math.sqrt(distanceX ** 2 + distanceY ** 2) < 500 and distanceY < 250) or self.maxhp != self.hp:
            if self.posX - player.posX > 5:
                self.action = 2
                dir = -1
            elif self.posX - player.posX <= -5:
                self.action = 3
                dir = 1

            if not self.ColtoMap(dir * SPEED, 0):
                if not self.MonsterCol(dir * SPEED, 0):
                    self.posX += dir * SPEED
            else:  # 점프 조건
                self.Jump(33)
        else:
            self.action = 0
        if self.hp < self.maxhp / 2: self.speed = 9

    def Jump(self, s):
        if not self.jump:
            return

        SPEED = game_framework.getSpeed(s)

        if self.jumpY < 0:
            self.jumpY = self.posY

        if self.ColtoMap(0, -100) and self.jumpY + 100 > self.posY and not self.ColtoMap(0, SPEED) and not self.MonsterCol(0, SPEED):
            self.posY += SPEED
        else:
            self.jump = False
            self.falling = True
            self.jumpY = -1


class Archer(Monster):
    value = 2

    i_w = 25 * 4
    i_h = 25 * 4
    w = 85
    h = 100
    rad = 0
    dir = 0
    shoot = False
    image = pico2d.load_image('./res/Archer.png')

    def Hunting(self):
        self.frame = (self.frame + 4 * 1 * game_framework.frame_time * game_framework.MS) % 4

        if abs(self.posX - player.posX) < 650 and abs(self.posY - player.posY) < 650 or self.maxhp != self.hp:
            if self.posX - player.posX > 5 and 4.0 > self.frame > 3.0 and not self.shoot:
                self.action = 2
                self.Shooting()
                self.shoot = True
            elif self.posX - player.posX <= -5 and 4.0 > self.frame > 3.0 and not self.shoot:
                self.action = 3
                self.Shooting()
                self.shoot = True

            if self.frame < 3 and self.shoot: self.shoot = False
        else:
            self.action = 0

    def Shooting(self):
        if self.action == 2:
            self.dir = -1
            self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi  # + 180
        elif self.action == 3:
            self.dir = 1
            self.rad = math.atan2(player.posY - self.posY, player.posX - self.posX) * 180 / math.pi
        arrow = Arrow(self.posX, self.posY, self.power, self.rad, self.dir)

        a_list.append(arrow)

    def Show(self, x, y):
        self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.i_w, self.i_h, self.posX - x,
                             self.posY - y, self.w, self.h)


class Arrow(Sprite):
    image = pico2d.load_image('./res/arrow.png')

    def __init__(self, px, py, dmg, rad, dir):
        self.speed = 20
        self.dir = dir
        self.rad = rad
        self.posX = px
        self.posY = py
        self.spawnX = self.posX
        self.w = 15 * 3
        self.h = 5 * 3
        self.power = dmg

    def Show(self):
        self.image.rotate_draw(self.rad / 360 * 2 * math.pi, self.posX - player.cameraX, self.posY - player.cameraY,
                               self.w, self.h)

    def move(self):
        SPEED = game_framework.getSpeed(self.speed)

        self.posX += SPEED * math.cos(self.rad / 360 * 2 * math.pi)
        self.posY += SPEED * math.sin(self.rad / 360 * 2 * math.pi)


def UpdateMonster():
    for monster in m_list:
        monster.Update()




def ShowMonster():
    for monster in m_list:
        monster.Show(player.cameraX, player.cameraY)


def ShowArrow():
    for a in a_list:
        a.Show()


def UpdateArrow():
    for a in a_list:
        a.move()

        if a.posY > 3000:
            a_list.remove(a)
            continue
        if a.posX > len(Map.stageData[Map.number][0]) * 100:
            a_list.remove(a)
            continue
        if a.ColtoMap(0, 0):
            a_list.remove(a)
            continue
        if abs(a.posX - player.posX) < player.w / 2:
            if abs(a.posY - player.posY) + 25 < player.h / 2:
                player.hit(a.power)
                a_list.remove(a)
                continue


m_list = []
a_list = []


def monsterInit():
    global m_list, a_list
    m_list.clear()
    a_list.clear()

    with open('monsterPos.json', 'r') as f:
        monsterData = json.load(f)
        for data in monsterData:
            if data['stage'] == Map.number:
                if data['type'] == 'melee':
                    m = Melee(data['x'], data['y'])
                elif data['type'] == 'archer':
                    m = Archer(data['x'], data['y'])
                m_list.append(m)
