import HandleEvent
from HandleEvent import *
from Background import *
from Hero import *
from map import  *

width = 1200
height = 700

open_canvas(width,height)

background.imageLoad('./res/background.png')
player.imageLoad('./res/idle.png')
darkgrass.imageLoad('./res/dark_grass50.png')
darkdirt.imageLoad('./res/dark_dirt.png')

while HandleEvent.running:
    clear_canvas()
    background.Show()
    LoadMap(stage)
    playerUpdate()
    update_canvas()
    Handle_events()
    delay(0.01)

close_canvas()


