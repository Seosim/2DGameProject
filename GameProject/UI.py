from pico2d import *
from Hero import player

UI_hp = None
hpBar = None

def LoadUI():
    global UI_hp,hpBar
    UI_hp = load_image('./res/HP_UI.png')
    hpBar = load_image('./res/hp.png')


def showUI():
    for i in range(player.hp):
        hpBar.clip_draw(0,0,1,20,40+i,700-28)
    UI_hp.clip_draw(0,0,144,28,72,700-28)
