import game_framework
from pico2d import *
from button import Button
import play_state
import cursor

start_button = None
quit_button = None

def enter():
    global start_button , quit_button
    start_button = Button()
    start_button.setButton(600,450,1)
    quit_button = Button()
    quit_button.setButton(600,300,0)

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

def update():delay(0.01)

def draw():
    clear_canvas()
    play_state.drawWorld()
    start_button.draw()
    quit_button.draw()
    cursor.aim.Show()
    update_canvas()

def exit(): pass



