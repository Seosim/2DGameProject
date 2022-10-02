from pico2d import *
import Hero

running = True


def Handle_events():
    global running

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_d:
                Hero.player.PushR = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_a:
                Hero.player.PushL = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_SPACE and  Hero.player.stand:
                Hero.player.PushSpace = True
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_d:
                Hero.player.PushR = False
            elif e.key == SDLK_a:
                Hero.player.PushL = False
            #elif e.key == SDLK_SPACE:
             #   Hero.player.PushSpace = False
    if Hero.player.PushR == False and Hero.player.PushL == False:
        Hero.player.imageLoad('./res/idle.png')
