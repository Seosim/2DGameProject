from sprite import Sprite
import Hero
from MapData import Map
from MapData import size

def LoadMap():
    stage = Map.stageData[Map.number]

    x = 0
    y = len(stage) - 1

    for _y in stage:
        for _x in _y:
            if _x == 1:
                if -100<(x * size)+size/2 - Hero.player.cameraX <1400:
                    darkgrass.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2- Hero.player.cameraY)
            elif _x == 2:
                if -100<(x * size)+size/2 - Hero.player.cameraX <1400:
                    darkdirt.image.clip_draw(0, 0, size, size, (x * size)+size/2 - Hero.player.cameraX, (y * size)+size/2- Hero.player.cameraY)
            elif _x == 3:
                if -100<(x * size)+size/2 - Hero.player.cameraX <1400:
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
