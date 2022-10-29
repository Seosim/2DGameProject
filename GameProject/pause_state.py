import game_framework
from pico2d import *
from button import Button
import play_state
import cursor

def enter(): pass

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
        elif e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)




def update():delay(0.01)

def draw():
    clear_canvas()
    play_state.drawWorld()
    cursor.aim.Show()
    update_canvas()

def exit(): pass



