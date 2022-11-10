from HandleEvent import *
from Background import *
from Hero import *
from map import *
from cursor import *
from mapObject import *
from weapon import *
from monster import *
from UI import *
from object import *
from boss import *

import title_state

width = 1200
height = 700

tile = []

def enter():
    global tile
    tile = [Tile((x*100) + 50,(y*100) + 50,100,100,val) for x,y,val in Mapgenerator() if val]

    playerInit()
    aim.imageLoad('./res/cursor.png')
    obj_1.imageLoad('./res/largeobject.png')
    weaponInit()
    monsterInit()
    ObjectInit()
    LoadUI()

def drawWorld():
    hide_cursor()
    background.image.draw(width / 2, height / 2, width, height)

    for t in tile:
        t.draw()

    skul.Draw()
    #LoadMap()
    LoadObj(Map.objData[Map.number])
    ShowArrow()
    ShowBullet()
    ShowObject()
    ShowMonster()
    player.Show()
    gun.Show()
    aim.Show()


def draw():
    clear_canvas()
    drawWorld()
    showUI()
    update_canvas()

def update():
    UpdateObject()
    UpdateMonster()
    UpdateArrow()
    UpdateBullet()
    player.ColtoMonster(m_list)
    playerUpdate()
    gun.Update()
    skul.update()
    if Hero.player.hp <= 0:
        Map.number = 0
        game_framework.change_state(title_state) #게임종료

def handle_events():
    Handle_events()

def pause(): player.KeyReset()

def resume():
    global tile

    tile.clear()
    tile = [Tile((x*100) + 50,(y*100) + 50,100,100,val) for x,y,val in Mapgenerator() if val]

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


