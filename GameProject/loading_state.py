import game_framework
import pico2d

image = None
timer = 0
width = 1200
height = 700

def enter():
    global image, timer
    image = pico2d.load_image('./res/logo_Sleep.png')
    timer = 0

def update():
    global timer
    timer += 1
    if timer > 2000: game_framework.pop_state()

def draw():
    pico2d.clear_canvas()
    image.draw(width / 2, height / 2, width, height)
    pico2d.update_canvas()

def pause():pass

def resume():pass

def exit(): pass

def handle_events():pass
