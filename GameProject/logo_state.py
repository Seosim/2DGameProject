import game_framework
import title_state
from pico2d import *

width = 1200
height = 700
logoImage = None
timer = 0

def enter():
    global logoImage , timer
    logoImage = load_image('./res/logo_Sleep.png')
    timer = 0

def exit():
    global logoImage,timer
    del logoImage,timer

def update():
    global timer
    delay(0.01)
    timer += 1
    if timer > 500:
        timer = 0
        game_framework.change_state(title_state)

def draw():
    clear_canvas()
    logoImage.draw(width / 2, height / 2, width, height)
    update_canvas()

def handle_events():
    global logoImage,timer
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                logoImage = load_image('./res/logo_wakeUp.png')
                timer = 400

