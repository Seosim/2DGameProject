import time

from pico2d import *
import Hero
import cursor
import weapon
import game_framework
import pause_state
import object

def Handle_events():
    events = get_events()
    for e in events:
        # if e.type == SDL_QUIT:  #종료버튼
        #     game_framework.quit()
        if e.type == SDL_KEYDOWN: #키다운
            if e.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)
            if e.key == SDLK_d:
                Hero.player.PushR = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_a:
                Hero.player.PushL = True
                Hero.player.imageLoad('./res/running.png')
            elif e.key == SDLK_SPACE and  Hero.player.stand:
                Hero.player.PushSpace = True
            elif e.key == SDLK_f:
                Hero.player.Flash()
            elif e.key == SDLK_r: #장전
                if weapon.gun.ammo != weapon.gun.maxAmmo and not weapon.gun.R:
                    weapon.gun.R = True
            elif e.key == SDLK_g:
                object.Interact()
            elif e.key == SDLK_s:
                if not Hero.player.PushSpace: Hero.player.pushS = True
            elif e.key == SDLK_t:
                if time.time() - Hero.player.slowMotionCD >10:
                    Hero.player.PushT = True
        elif e.type == SDL_KEYUP:   # 키업
            if e.key == SDLK_d:
                Hero.player.PushR = False
            elif e.key == SDLK_a:
                Hero.player.PushL = False
            elif e.key == SDLK_s:
                Hero.player.pushS = False
        elif e.type == SDL_MOUSEMOTION: #마우스 움직임
            cursor.aim.UpdateCursor(e.x,e.y)
            weapon.gun.DefDir(e.x)
            weapon.gun.radian(e.x,e.y)
        elif e.type == SDL_MOUSEBUTTONDOWN: #마우스 클릭
            if e.button == SDL_BUTTON_LEFT:
                weapon.gun.clickButton = True
            if e.button == SDL_BUTTON_RIGHT:
                if Hero.player.DashCD == 0: Hero.player.DashGet(e.x,e.y)
        elif e.type == SDL_MOUSEBUTTONUP:
            if e.button == SDL_BUTTON_LEFT:
                weapon.gun.clickButton = False


    if Hero.player.PushR == False and Hero.player.PushL == False:
        Hero.player.imageLoad('./res/idle.png')
