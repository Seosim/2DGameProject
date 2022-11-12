import pico2d

from sprite import Sprite
import Hero
from MapData import width,height,Map,size

from Hero import player

def LoadMap():
    stage = Map.stageData[Map.number]

    x = 0
    y = len(stage) - 1

    for _y in stage:
        for _x in _y:
            if _x == 1:
                if -100<(x * size)+size/2 - Hero.player.cameraX <width+200:
                    darkgrass.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2- Hero.player.cameraY)
            elif _x == 2:
                if -100<(x * size)+size/2 - Hero.player.cameraX <width+200:
                    darkdirt.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2- Hero.player.cameraY)
            elif _x == 3:
                if -100<(x * size)+size/2 - Hero.player.cameraX <width+200:
                    halfgrass.image.clip_draw(0, 0, size, 30, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2 - Hero.player.cameraY)
            x += 1
        y -= 1
        x = 0
    # x = 0
    # y = 6

# 가로타일 100개 세로타일 7개


darkgrass = Sprite()
darkdirt = Sprite()
halfgrass = Sprite()

darkgrass.imageLoad('./res/dark_grass50.png')
darkdirt.imageLoad('./res/dark_dirt.png')
halfgrass.imageLoad('./res/half_grass.png')

def Mapgenerator():
    _x = -1
    #_y = -1
    _y = len(Map.stageData[Map.number])

    for y in Map.stageData[Map.number]:
        _y -= 1
        _x = -1
        for val in y:
            _x += 1
            yield _x,_y,val


class Tile(Sprite):
    image = None
    def __init__(self,x,y,w,h,v):
        if self.image == None:
            self.image = pico2d.load_image('./res/dark_grass50.png')

        if v == 2:
            self.image = pico2d.load_image('./res/dark_dirt.png')
        elif v == 3:
            self.image = pico2d.load_image('./res/half_grass.png')

        self.posX = x
        self.posY = y
        self.w = w
        self.h = h
        self.frame = 0
        self.action = 0
        self.i_w = w
        self.i_h= h

        if v ==3 :
            self.h = 30

    def update(self): pass

    def draw(self):
        if  abs(self.posX - player.posX) < width:
            self.image.clip_draw(0,0,self.w,self.h,self.posX-player.cameraX,self.posY-player.cameraY)

