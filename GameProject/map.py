from sprite import Sprite
import Hero
from MapData import stage
from MapData import size


def LoadMap(stage):
    global x,y
    cameraX = Hero.player.posX - (1200 / 2)
    #카메라가 맵밖을 촬영하지 않게 설정
    if cameraX <= 0: cameraX = 0
    elif size * len(stage[6]) - Hero.player.posX <= 600: cameraX = size * len(stage[6]) - 1200

    for _y in stage:
        for _x in _y:
            if _x == 1:
                if -100<(x * size)+size/2 - cameraX <1400:
                    darkgrass.image.clip_draw(0, 0, size, size, (x * size)+size/2 - cameraX, (y * size)+size/2)
            elif _x == 2:
                if -100<(x * size)+size/2 - cameraX <1400:
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
            if _x:
               if abs(Hero.player.posX - (x*size+(size/2)) + valX) < size/2 + Hero.player.w/2 - 5:
                   if Hero.player.posY+(size/2)+valY > (y*size+(size/2)) and abs(Hero.player.posY - (y*size+(size/2)) + valY) < size/2 + Hero.player.h/2 - 5 :
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


# 가로타일 100개 세로타일 7개
x = 0
y = len(stage)-1

darkgrass = Sprite()
darkdirt = Sprite()