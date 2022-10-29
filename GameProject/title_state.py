from pico2d import *
import game_framework
import play_state
from button import Button

background = None
start_button = None
quit_button = None

width = 1200
height = 700

def enter():
    global background , start_button , quit_button
    background = load_image('./res/background.png')
    start_button = Button()
    start_button.setButton(600,250,1)
    quit_button = Button()
    quit_button.setButton(600,100,0)


def draw():
    clear_canvas()
    show_cursor()
    background.draw(width / 2, height / 2, width, height)
    start_button.draw()
    quit_button.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if start_button.InClick(e.x,699-e.y):
                    game_framework.change_state(play_state)
                    break
                if quit_button.InClick(e.x,699-e.y):
                    game_framework.quit()

def update(): pass

def pause():pass

def resume():pass

def exit():
    global background , start_button , quit_button
    del background
    del start_button
    del quit_button
