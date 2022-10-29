from HandleEvent import *
from Background import *
from Hero import *
from map import  *
from cursor import *
from mapObject import *
from weapon import *
from monster import *
from UI import *

import title_state

width = 1200
height = 700


def enter():
    playerInit()
    background.imageLoad('./res/background.png')
    darkgrass.imageLoad('./res/dark_grass50.png')
    darkdirt.imageLoad('./res/dark_dirt.png')
    halfgrass.imageLoad('./res/half_grass.png')
    aim.imageLoad('./res/cursor.png')
    obj_1.imageLoad('./res/largeobject.png')
    weaponInit()
    monsterInit()
    MonsterImage()
    LoadUI()

def drawWorld():
    hide_cursor()
    background.image.draw(width / 2, height / 2, width, height)
    LoadMap()
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
    showUI()
    update_canvas()

def update():
    UpdateMonster()
    UpdateArrow()
    UpdateBullet()
    player.ColtoMonster(m_list)
    playerUpdate()
    gun.Update()
    if Hero.player.hp <= 0:
        game_framework.change_state(title_state) #게임종료
    delay(0.01)

def handle_events():
    Handle_events()

def pause(): player.KeyReset()

def resume(): pass

def exit(): pass
    # global player,background,darkdirt,darkgrass,aim,obj_1,gun,m_list,a_list,bullet_list
    # del player
    # del background
    # del darkdirt
    # del darkgrass
    # del aim
    # del obj_1
    # del gun
    # del m_list
    # del a_list
    # del bullet_list


