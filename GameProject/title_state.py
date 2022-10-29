from pico2d import *
import game_framework
import play_state

background = None
width = 1200
height = 700

def enter():
    global background
    background = load_image('./res/background.png')
def draw():
    clear_canvas()
    background.draw(width / 2, height / 2, width, height)
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                game_framework.change_state(play_state)

def update(): pass

def exit(): pass

