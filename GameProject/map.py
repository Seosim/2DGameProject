from sprite import Sprite
import Hero
from MapData import stage
from MapData import size


def LoadMap(stage):
    global x,y

    for _y in stage:
        for _x in _y:
            if _x == 1:
                if -100<(x * size)+size/2 - Hero.player.cameraX <1400:
                    darkgrass.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2)
            elif _x == 2:
                if -100<(x * size)+size/2 - Hero.player.cameraX <1400:
                    darkdirt.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2)
            x += 1
        y -= 1
        x = 0
    x = 0
    y = 6




# 가로타일 100개 세로타일 7개
x = 0
y = len(stage)-1

darkgrass = Sprite()
darkdirt = Sprite()