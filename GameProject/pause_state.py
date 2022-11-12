import time

import game_framework
from pico2d import *
from button import Button
import play_state
import cursor
from MapData import width,height
from Hero import player
from boss import Belial

start_button = None
quit_button = None
timer = 0

def enter():
    global start_button , quit_button,timer
    start_button = Button()
    start_button.setButton(width/2,height/2 + 100,1)
    quit_button = Button()
    quit_button.setButton(width/2,height/2 - 100,0)
    timer = time.time()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
        if e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if start_button.InClick(e.x,e.y):
                    game_framework.pop_state()
                if quit_button.InClick(e.x,e.y):
                    game_framework.quit()

def update(): pass

def draw():
    clear_canvas()
    play_state.drawWorld()
    start_button.draw()
    quit_button.draw()
    cursor.aim.Show()
    update_canvas()

def exit():
    global timer , start_button,quit_button
    quit_time = time.time() - timer
    player.CoolTimeSet(quit_time)
    Belial.CoolTimeSet(quit_time)





