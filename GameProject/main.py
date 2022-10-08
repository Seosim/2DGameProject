import HandleEvent
from HandleEvent import *
from Background import *
from Hero import *
from map import  *
from cursor import *
from mapObject import *
from weapon import *
from monster import *

width = 1200
height = 700

open_canvas(width,height)

background.imageLoad('./res/background.png')
player.imageLoad('./res/idle.png')
darkgrass.imageLoad('./res/dark_grass50.png')
darkdirt.imageLoad('./res/dark_dirt.png')
aim.imageLoad('./res/cursor.png')
obj_1.imageLoad('./res/largeobject.png')
gun.imageLoad('./res/pistolR.png')
hoodman.imageLoad('./res/hoodman.png')

while HandleEvent.running:
    hide_cursor()
    clear_canvas()

    background.image.draw(width/2,height/2,width,height)
    LoadMap(stage)
    LoadObj(obj_loc)
    hoodman.Update()
    LoadMonster()


    playerUpdate()
    player.ColtoMonster(m_list)

    gun.Update()
    aim.Show()

    update_canvas()
    Handle_events()
    delay(0.01)

close_canvas()


