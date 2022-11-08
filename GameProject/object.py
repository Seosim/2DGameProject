from sprite import Sprite
from Hero import player
from monster import *
from MapData import *
from boss import *
import loading_state
import game_framework


class Object(Sprite):
    freeze = False

    def __init__(self,iw,ih,sizeX,sizeY,pX,pY):
        self.i_w = iw
        self.i_h = ih
        self.w = sizeX
        self.h = sizeY
        self.posX = pX
        self.posY = pY
        self.action = 0


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
        m_list.clear()
        Map.NextMap()
        player.posX = 300
        self.posX = 9700
        game_framework.push_state(loading_state)
        InitBoss()





o_list = []

def ObjectInit():
    global o_list
    o_list.clear()

    portal = Portal(24,33,100,170,300,200)
    portal.imageLoad('./res/Portal.png')
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
            return


