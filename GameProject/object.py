from sprite import Sprite
from Hero import player
from weapon import gun
from MapData import *
from boss import *
import loading_state
import game_framework


class Object(Sprite):
    freeze = False

    def __init__(self,iw,ih,sizeX,sizeY,pX,pY,name):
        self.i_w = iw
        self.i_h = ih
        self.w = sizeX
        self.h = sizeY
        self.posX = pX
        self.posY = pY
        self.action = 0
        self.imageLoad(name)



    def Gravity(self):
        if self.freeze : return

        if not self.collision(0,-5):
            self.posY -=5
        else : self.freeze = True

    def InPlayer(self):
        if abs(player.posX - self.posX) < (player.w/2+self.w/2) \
            and abs(player.posY - self.posY) < (player.h/2+self.h/2):
            return True
        else : return False

class Portal(Object):
    def Interaction(self):
        Map.NextMap()
        player.posX = 300
        self.posX = 9700
        game_framework.push_state(loading_state)
        InitBoss()


WeaponList = {'./res/pistolR' : (10,8,35,0.5,48,48,50,50)} #데미지,장탄수,총알속도,연사력,이미지크기,실제크기

class Item_W(Object):
    def __init__(self, iw, ih, sizeX, sizeY, pX, pY, name):
        self.i_w = iw
        self.i_h = ih
        self.w = sizeX
        self.h = sizeY
        self.posX = pX
        self.posY = pY
        self.action = 0
        self.imageLoad(name)
        self.data = WeaponList['./res/pistolR']

    def Interaction(self):
        gun.damage = self.data[0]
        gun.maxAmmo = self.data[1]
        gun.ammo = self.data[1]
        gun.speed = self.data[2]
        gun.attack_speed = self.data[3]
        gun.i_w = self.data[4]
        gun.i_h = self.data[5]
        gun.w = self.data[6]
        gun.h = self.data[7]



o_list = []

def ObjectInit():
    global o_list
    o_list.clear()

    portal = Portal(24,33,100,170,300,200,'./res/Portal.png')
    o_list.append(portal)

def ShowObject():
    for o in o_list:
        o.Show(player.cameraX,player.cameraY)

def UpdateObject():
    for o in o_list:
        o.Gravity()

        if o.posY < - 100:
            o_list.remove(o)
            del o

def Interact():
    for o in o_list:
        if o.InPlayer():
            o.Interaction()
            o_list.remove(o)
            return


