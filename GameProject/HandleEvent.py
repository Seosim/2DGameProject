from pico2d import *
import Hero
import cursor
import weapon

running = True


def Handle_events():
    global running

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:  #종료버튼
            running = False
        elif e.type == SDL_KEYDOWN: #키다운
            if e.key == SDLK_d:
                Hero.player.PushR = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_a:
                Hero.player.PushL = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_SPACE and  Hero.player.stand:
                Hero.player.PushSpace = True
        elif e.type == SDL_KEYUP:   # 키업
            if e.key == SDLK_d:
                Hero.player.PushR = False
            elif e.key == SDLK_a:
                Hero.player.PushL = False
            #elif e.key == SDLK_SPACE:
             #   Hero.player.PushSpace = False  #점프중 떼면 바로착지
        elif e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)
            weapon.gun.DefDir(e.x)
            weapon.gun.radian(e.x,e.y)
        elif e.type == SDL_MOUSEBUTTONDOWN: #마우스 클릭
            weapon.gun.clickButton = True
        elif e.type == SDL_MOUSEBUTTONUP:
            weapon.gun.clickButton = False

    if Hero.player.PushR == False and Hero.player.PushL == False:
        Hero.player.imageLoad('./res/idle.png')
