import random
import time

import pico2d

from object import Object,o_list
from weapon import gun
from Hero import player

WeaponList = {0 : (17,8,35,0.5,48,48,50,50,'./res/pistol.png',500,'./sound/pistol.wav','./sound/reload_p.wav',1),
              1 : (10,30,44,0.15,130,60,130,60,'./res/M4.png',750,'./sound/m4.wav','./sound/reload_m.wav',1.5),
              2 : (70,5,70,2,144,50,150,50,'./res/Sniper.png',1500,'./sound/Sniper.wav','./sound/reload_s.wav',2.5),
              3 : (13,35,35,0.2,130,60,120,50,'./res/AK47.png',600,'./sound/AK47.wav','./sound/reload_m.wav',1.5)}
#데미지,장탄수,총알속도,연사력,이미지크기,실제크기,이미지이름,사거리,장전소리,장전속도

class Item_HP(Object):
    image = None
    sound = None
    def __init__(self, pX, pY):
        if Item_HP.image == None:
            Item_HP.image = pico2d.load_image('./res/medikit.png')
        if  Item_HP.sound == None:
            Item_HP.sound = pico2d.load_wav('./sound/health.wav')
            Item_HP.sound.set_volume(30)
        self.i_w = 18
        self.i_h = 11
        self.action = 0
        self.frame = 0
        self.w = 36
        self.h = 22
        self.posX = pX
        self.posY = pY
        self.timer = time.time()


    def Interaction(self):
        self.sound.play()
        player.hp += 10
        if player.hp > 100 : player.hp = 100

    def addList(self):
        o_list.append(self)


class Item_W(Object):
    sound = None
    def __init__(self, pX, pY):
        if Item_W.sound == None:
            Item_W.sound = pico2d.load_wav('./sound/swap.wav')
        self.data = WeaponList[random.randint(1,3)]
        self.i_w = self.data[4]
        self.i_h = self.data[5]
        self.w = self.data[6]
        self.h = self.data[7]
        self.posX = pX
        self.posY = pY
        self.imageLoad(self.data[8])
        self.action = 0
        self.timer = time.time()

    def Interaction(self):
        self.sound.play()
        gun.damage = self.data[0]
        gun.maxAmmo = self.data[1]
        gun.ammo = self.data[1]
        gun.speed = self.data[2]
        gun.attack_speed = self.data[3]
        gun.i_w = self.data[4]
        gun.i_h = self.data[5]
        gun.w = self.data[6]
        gun.h = self.data[7]
        gun.imageLoad(self.data[8])
        gun.distance = self.data[9]
        gun.sound = pico2d.load_wav(self.data[10])
        gun.reloadSound = pico2d.load_wav(self.data[11])
        gun.reloadTime = self.data[12]
        gun.reloadSound.set_volume(33)

    def addList(self):
        o_list.append(self)