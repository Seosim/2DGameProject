from pico2d import *
from Hero import player
from weapon import gun
from boss import skul
from MapData import Map,width,height

UI_hp = None
hpBar = None
UI_ammo = None
UI_BossHP = None
DashGage = None




def LoadUI():
    global UI_hp,hpBar,UI_ammo,UI_BossHP,DashGage
    UI_hp = load_image('./res/HP_UI.png')
    hpBar = load_image('./res/hp.png')
    UI_ammo = load_image('./res/ui_bullet.png')
    UI_BossHP = load_image('./res/Bar.png')
    DashGage = load_image('./res/DashGage.png')


def showUI():
    #플레이어 체력 UI
    hpBar.draw(90 -(100 - player.hp)//2 ,height-28,player.hp,28)
    UI_hp.clip_draw(0,0,144,28,72,height-28)

    #Dash가능여부 UI
    if player.DashCD == 0:
        DashGage.clip_draw(0,0,20,20,150,height-28)

    for i in range(gun.ammo): #총알갯수 UI
        UI_ammo.clip_draw(0,0,5,15,10+(i*7),height-56)

    if Map.number == 1: #보스 체력 UI
        hpBar.draw(width/2 -(1000 - skul.hp//3)//2,50,skul.hp//3,50)
        UI_BossHP.clip_draw(0,0,144,28,width/2,50,1050,50)

