from pico2d import *
import game_framework
import play_state
from button import Button
import cursor
from MapData import width,height

background = None
start_button = None
quit_button = None
title_name = load_image('./res/JongWick.png')

def enter():
    global background , start_button , quit_button,title_name
    background = load_image('./res/background.png')
    title_name = load_image('./res/JongWick.png')
    start_button = Button()
    start_button.setButton(width/2,height/2- 50,1)
    quit_button = Button()
    quit_button.setButton(width/2,height/2 - 250,0)
    cursor.aim.imageLoad('./res/cursor.png')
    play_state.playerInit()


def draw():
    clear_canvas()
    hide_cursor()
    background.draw(width / 2, height / 2, width, height)
    title_name.clip_draw(0,0,width - (width//5) , 200 ,width//2 ,height - (height//4))
    start_button.draw()
    quit_button.draw()
    cursor.aim.Show()
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if start_button.InClick(e.x,e.y):
                    game_framework.change_state(play_state)
                    break
                if quit_button.InClick(e.x,e.y):
                    game_framework.quit()
        elif e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)
        play_state.Hero.player.handle_event(e)

def update(): pass

def pause():pass

def resume():pass

def exit():
    global background , start_button , quit_button,title_name
    del background
    del start_button
    del quit_button
    del title_name

