from sprite import Sprite
import Hero

size = 100


def LoadMap(stage):
    global x,y
    cameraX = Hero.player.posX - (1200 / 2)
    cameraY = Hero.player.posY - 160
    for _y in stage:
        for _x in _y:
            if _x == 1:
                darkgrass.image.clip_draw(0, 0, size, size, (x * size)+size/2 - cameraX, (y * size)+size/2)
            elif _x == 2:
                darkdirt.image.clip_draw(0, 0, size, size, (x * size)+size/2 - cameraX, (y * size)+size/2)
            x += 1
        y -= 1
        x = 0
    x = 0
    y = 6

def collision(valX,valY):
    global x,y
    for _y in stage:
        for _x in _y:
            if _x == 1:
               if abs(Hero.player.posX - (x*size+(size/2)) + valX) < size/2 + Hero.player.w/2 - 5:
                   if abs(Hero.player.posY - (y*size+(size/2)) + valY) < size/2 + Hero.player.h/2 - 5 :
                       if abs((Hero.player.posY - Hero.player.h/2) -((y+1)*size)) <= 5:
                           Hero.player.gravitySpeed = 1
                       x = 0
                       y = 6
                       Hero.player.stand = True
                       return True
            x += 1
        y -= 1
        x = 0
    x = 0
    y = 6
    Hero.player.stand = False
    return False


# 가로타일 12개 세로타일 7개
stage = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,1,1,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,1,2],
         [0,0,0,0,0,0,0,0,0,0,1,2,2],
         [1,1,1,1,1,1,1,1,1,1,2,2,2,0,0,1,1,1,1]]

x = 0
y = len(stage)

darkgrass = Sprite()
darkdirt = Sprite()