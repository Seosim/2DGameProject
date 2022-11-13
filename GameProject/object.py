import time

from sprite import Sprite
from Hero import player
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
        self.timer = 0



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

o_list = []

def ObjectInit():
    global o_list
    o_list.clear()

def ShowObject():
    for o in o_list:
        o.Show(player.cameraX,player.cameraY)

def UpdateObject():
    for o in o_list:
        o.Gravity()

        if o.posY < - 100:
            o_list.remove(o)
            del o
        if o.timer and time.time()-o.timer > 10: o_list.remove(o)

def Interact():
    for o in o_list:
        if o.InPlayer():
            o.Interaction()
            o_list.remove(o)
            return


