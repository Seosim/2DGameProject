import game_framework
import title_state
import play_state
import cursor

from pico2d import *
from button import Button
from MapData import width,height,Map

title_button = None
quit_button = None
gameover = None

def enter():
    global title_button , quit_button,gameover
    title_button = Button()
    title_button.setButton(width/2,height/2,2)
    quit_button = Button()
    quit_button.setButton(width/2,height/2 - 150,0)
    if play_state.Hero.player.hp <= 0:
        gameover = load_image('./res/GameOver.png')
    else :
        gameover = load_image('./res/GameClear.png')

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if title_button.InClick(e.x,e.y):
                    Map.number = 0
                    play_state.player.live = True
                    game_framework.change_state(title_state)
                    break
                if quit_button.InClick(e.x,e.y):
                    game_framework.quit()
        elif e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)

def draw():
    clear_canvas()
    play_state.drawWorld()
    gameover.clip_draw(0,0,width - (width//5) , 200 ,width//2 ,height - (height//4))
    title_button.draw()
    quit_button.draw()
    cursor.aim.Show()
    update_canvas()

def update():
    play_state.update()

def pause(): pass

def resume(): pass

def exit(): pass
    # global title_button , quit_button,gameover
    # del title_button
    # del quit_button
    # del gameover
