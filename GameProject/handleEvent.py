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
        if e.type == SDL_KEYDOWN:  # 키다운
            if e.key == SDLK_ESCAPE:
                if not Hero.player.DashCnt:
                    game_framework.push_state(pause_state)
            elif e.key == SDLK_f:
                Hero.player.Flash()
            elif e.key == SDLK_r:  # 장전
                if weapon.gun.ammo != weapon.gun.maxAmmo and not weapon.gun.R:
                    weapon.gun.R = True
            elif e.key == SDLK_g:
                object.Interact()
            elif e.key == SDLK_s:
                if not Hero.player.PushSpace: Hero.player.pushS = True
            elif e.key == SDLK_t:
                if time.time() - Hero.player.slowMotionCD > 10:
                    Hero.player.PushT = True
            elif e.key == SDLK_y:
                Hero.player.hp = 100
        elif e.type == SDL_KEYUP:  # 키업
            if e.key == SDLK_s:
                Hero.player.pushS = False
        elif e.type == SDL_MOUSEMOTION:  # 마우스 움직임
            cursor.aim.UpdateCursor(e.x, e.y)
            weapon.gun.DefDir(e.x)
            weapon.gun.radian(e.x, e.y)
        elif e.type == SDL_MOUSEBUTTONDOWN:  # 마우스 클릭
            if e.button == SDL_BUTTON_LEFT:
                Hero.player.clickButton = True
            if e.button == SDL_BUTTON_RIGHT:
                Hero.player.DashGet(e.x, e.y)
        elif e.type == SDL_MOUSEBUTTONUP:
            if e.button == SDL_BUTTON_LEFT:
                Hero.player.clickButton = False
        Hero.player.handle_event(e)
