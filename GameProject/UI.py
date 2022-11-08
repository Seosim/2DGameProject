from pico2d import *
from Hero import player
from weapon import gun
from boss import skul
from MapData import Map

UI_hp = None
hpBar = None
UI_ammo = None

UI_BossHP = None


def LoadUI():
    global UI_hp,hpBar,UI_ammo,UI_BossHP
    UI_hp = load_image('./res/HP_UI.png')
    hpBar = load_image('./res/hp.png')
    UI_ammo = load_image('./res/ui_bullet.png')
    UI_BossHP = load_image('./res/Bar.png')


def showUI():
    for i in range(player.hp):
        hpBar.clip_draw(0,0,1,20,40+i,700-28)
    UI_hp.clip_draw(0,0,144,28,72,700-28)

    for i in range(gun.ammo):
        UI_ammo.clip_draw(0,0,5,15,10+(i*7),700-56)

    if Map.number == 1:
        for i in range(skul.hp//3):
            hpBar.clip_draw(0,0,1,20,100+i,50,1,50)
        UI_BossHP.clip_draw(0,0,144,28,600,50,1050,50)

