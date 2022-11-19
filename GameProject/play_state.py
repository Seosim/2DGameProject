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
from portal import Portal
from particle import *

import title_state

tile = []
bgm = None
portal = None

def enter():
    global tile,bgm,portal
    tile = [Tile((x*100) + 50,(y*100) + 50,100,100,val) for x,y,val in Mapgenerator() if val]
    portal = Portal(24, 33, 100, 170, 9700, 200, './res/Portal.png')
    #playerInit()
    aim.imageLoad('./res/cursor.png')
    obj_1.imageLoad('./res/largeobject.png')
    weaponInit()
    monsterInit()
    ObjectInit()
    for i in range(2):
        portal.addList()
    LoadUI()

    bgm = load_music('./sound/bgm.mp3')
    bgm.repeat_play()


def drawWorld():
    hide_cursor()
    background.image.draw(width / 2, height / 2, width, height)

    for t in tile:
        t.draw()
    #LoadMap()
    LoadObj(Map.objData[Map.number])
    Belial.Draw()
    ShowArrow()
    ShowBullet()
    ShowObject()
    ShowMonster()
    ShowParticle(player.cameraX,player.cameraY)
    player.draw()
    gun.Show()

    aim.Show()


def draw():
    clear_canvas()
    drawWorld()
    showUI()
    update_canvas()

def update():
    player.update()
    UpdateBullet()
    UpdateParticle()
    if Map.number != 2:
        UpdateObject()
        UpdateMonster()
        UpdateArrow()
        player.ColtoMonster(m_list)
    gun.Update()
    Belial.update()

def handle_events():
    Handle_events()


def pause():
    global bgm
    player.KeyReset()
    bgm.pause()

def resume():
    global tile,bgm

    bgm.resume()
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


