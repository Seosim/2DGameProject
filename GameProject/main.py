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

def enter():
    player.imageLoad('./res/idle.png')
    background.imageLoad('./res/background.png')
    darkgrass.imageLoad('./res/dark_grass50.png')
    darkdirt.imageLoad('./res/dark_dirt.png')
    aim.imageLoad('./res/cursor.png')
    obj_1.imageLoad('./res/largeobject.png')
    gun.imageLoad('./res/pistolR.png')
    MonsterImage()

def drawWorld():
    hide_cursor()
    background.image.draw(width / 2, height / 2, width, height)
    LoadMap(stage)
    LoadObj(obj_loc)
    ShowMonster()
    ShowArrow()
    ShowBullet()
    player.Show()
    gun.Show()
    aim.Show()

def draw():
    clear_canvas()
    drawWorld()
    update_canvas()

def update():
    UpdateMonster()
    UpdateArrow()
    UpdateBullet()
    player.ColtoMonster(m_list)
    playerUpdate()
    gun.Update()
    delay(0.01)

def handle_events():
    Handle_events()

def exit():
    global player,background,darkdirt,darkgrass,aim,obj_1,gun,m_list,a_list,bullet_list
    del player
    del background
    del darkdirt
    del darkgrass
    del aim
    del obj_1
    del gun
    del m_list
    del a_list
    del bullet_list



# while HandleEvent.running:
#     show()
#     update()
#     Handle_events()
#     delay(0.01)
#
# close_canvas()


