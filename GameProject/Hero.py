import pico2d
from pico2d import *
import game_framework
import time
import math
import gameover_state

from sprite import Sprite
from mapData import width,height,Map,size
from particle import Particle

RD, LD, RU, LU, LMD,RMD,LMU,RMU,SPACE,DEAD= range(10)
event_name = ['RD', 'LD', 'RU', 'LU', 'LMD','RMD','LMU','RMU','SPACE','DEAD']

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): RD,
    (SDL_KEYDOWN, SDLK_a): LD,
    (SDL_KEYUP, SDLK_d): RU,
    (SDL_KEYUP, SDLK_a): LU,
    (SDL_KEYDOWN,SDLK_SPACE) : SPACE,
    (SDL_MOUSEBUTTONDOWN,SDL_BUTTON_RIGHT) : RMD
}

class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.imageLoad('./res/idle.png')
        self.dir = 0
        if self.dir == 1: self.action = 1
        elif self.dir == -1: self.action = 0
        self.SetCamera(Map.stageData[Map.number])

    @staticmethod
    def exit(self,event):
        print('EXIT IDLE')
        if event == SPACE:
           if self.stand :self.PushSpace = True

    @staticmethod
    def do(self): pass



    @staticmethod
    def draw(self):
        self.Show()


class RUN:
    @staticmethod
    def enter(self, event):
        print('ENTER RUN')
        self.imageLoad('./res/running.png')
        if event == RD:
            self.dir = 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

        if self.dir == 1: self.action = 1
        elif self.dir == -1: self.action = 0

    def exit(self,event):
        print('EXIT RUN')
        self.face_dir = self.dir
        if event == SPACE:
           if self.stand: self.PushSpace = True

    @staticmethod
    def do(self):
        self.move()



    @staticmethod
    def draw(self):
        if self.dir == -1:
            self.Show()
        elif self.dir == 1:
            self.Show()

class SLEEP:
    @staticmethod
    def enter(self, event):
        print('ENTER SLEEP')
        self.imageLoad('./res/dead.png')
        self.action = 0
        self.frame = 0


    def exit(self,event):
        print('EXIT SLEEP')


    @staticmethod
    def do(self):pass


    @staticmethod
    def draw(self):
        self.Show()

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN,  SPACE:IDLE , DEAD:SLEEP},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE:RUN,DEAD:SLEEP},
    SLEEP: {RU: SLEEP,  LU: SLEEP,  RD: SLEEP,  LD: SLEEP,  SPACE:SLEEP , DEAD:SLEEP}
}

class Player(Sprite):

    def __init__(self):

        self.speed = 12
        self.jumpMax = 180
        self.jumpPower = 40
        self.hp = 100
        self.live = True
        self.god = False

        self.face_dir = 0
        self.dir = 0

        self.jumpY = -1
        self.gravitySpeed = 10

        self.PushR = False
        self.PushL = False

        self.PushSpace = False
        self.stand = True
        self.clickButton = False

        self.posX = 300
        self.posY = 200
        self.i_w = 16 * 4
        self.i_h = 25 * 4
        self.w = self.i_w
        self.h = self.i_h
        self.inv = 0 # 무적
        self.hitframe = 0
        self.screenX = self.posX
        self.cameraX = width/2
        self.cameraY = 0
        self.shooting = 0
        self.vibration = 8

        #하향점프 관련 변수
        self.pushS = False
        self.fall = 0

        #슬로우모션 관련 변수
        self.slowMotionDelay = 0
        self.slowMotionCD = 0
        self.PushT = False

        #대쉬 관련 변수
        self.DashCnt = 0
        self.DashDirX = 0
        self.DashDirY = 0
        self.DashCD = 0

        #사운드 변수
        self.hitSound = pico2d.load_wav('./sound/Hit_Player.wav')
        self.hitSound.set_volume(50)
        self.jumpSound = pico2d.load_wav('./sound/Jumping.wav')
        self.dashSound = pico2d.load_wav('./sound/dash.wav')
        self.runSound = pico2d.load_wav('./sound/step.wav')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        self.getScreenX()
        self.invincibility()
        self.jump()
        self.down()
        self.SlowMotion()
        self.Dash(self.DashDirX, self.DashDirY)
        self.OutOfMap()
        self.Dead()
        self.Gravity()
        if self.live:
            self.frame = (self.frame + 4 * 2 * game_framework.frame_time*game_framework.MS) % 4

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            try: #예외처리
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print("ERROR: " ,self.cur_state.__name__,'   ',event_name[event])
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


    def getScreenX(self):
        stage = Map.stageData[Map.number]

        if width / 2 > self.posX: self.screenX = self.posX
        elif self.posX >= size * len(stage[6]) - width/2:
            self.screenX = width - (len(stage[6])*size-self.posX)
        else : self.screenX =  width / 2

    def Show(self):
        self.image.clip_draw(self.i_w * (self.hitframe+int(self.frame)), self.i_h * self.action, self.i_w, self.i_h, self.screenX,self.posY-self.cameraY,\
                             self.w,self.h)

    def Dead(self):
        if self.live and self.hp <= 0:
            self.imageLoad('./res/dead.png')
            self.i_w = 76
            self.i_h = 53
            self.w = 76
            self.h = 53
            self.frame = 0
            self.god = True
            self.hitframe = 0
            self.PushSpace = False
            game_framework.push_state(gameover_state)
            self.live = False
            self.add_event(DEAD)


    def move(self):
        stage = Map.stageData[Map.number]

        SPEED = game_framework.getSpeed(self.speed)

        if self.dir == 1 and not self.collision(SPEED,0):
            self.posX += SPEED
            #self.action = 1
        elif self.dir == -1 and not self.collision(-1*SPEED,0):
            self.posX -= SPEED
            #self.action = 0

        self.SetCamera(stage)

    def SetCamera(self, stage):
        self.cameraX = self.posX - (width / 2)
        if self.cameraX <= 0:
            self.cameraX = 0
        elif size * len(stage[6]) - self.posX <= width / 2:
            self.cameraX = size * len(stage[6]) - width
        if self.shooting:  # 카메라 진동효과
            self.cameraX += self.vibration//2
            if time.time() - self.shooting > 0.05: self.shooting = 0

        self.cameraY = max(0, self.posY - height + 250)
        self.getScreenX()

    def down(self):

        if self.pushS and self.PushSpace:
            self.PushSpace = False
            if not self.collision(0,-20):
                self.posY -= 20

        # if self.fall > 0: self.fall = (self.fall +1) % 25

    def jump(self):
        if self.pushS: return

        SPEED = game_framework.getSpeed(self.jumpPower)
        J_SPEED = game_framework.getSpeed(5)

        if self.PushSpace:
            if self.jumpY == -1:
                self.jumpY = self.posY

            if self.posY < self.jumpY + self.jumpMax and not self.collision(0, SPEED):
                self.posY += SPEED
                self.speed = 16
                if self.jumpPower > 20: self.jumpPower -= J_SPEED
            else:
                self.PushSpace = False
                self.jumpY = -1
                self.speed = 12
                self.jumpPower = 40

    def Flash(self):
        # for i in range(5):
        #     if self.dir == 1 and not self.collision(35, 0):
        #         self.posX += 35
        #         self.action = 1
        #     elif self.dir ==-1 and not self.collision(-35, 0):
        #         self.posX -= 35
        #         self.action = 0
        # self.OutOfMap()
        return

    def DashGet(self,x,y):
        if self.DashCD == 0:
            self.god = True
            self.DashCD = time.time()
            self.DashCnt = 25/game_framework.MS
            self.DashDirX = x
            self.DashDirY = y
            self.PushSpace = False
            self.jumpPower = 40
            self.jumpY = -1
            self.speed = 12
            self.gravitySpeed = 10
            self.dashSound.play()

    def Dash(self,x,y):
        if not self.live : return

        if time.time() - self.DashCD > 5:
            self.DashCD = 0

        if self.DashCnt:
            SPEEDX = game_framework.getSpeed(self.speed * 7 )
            SPEEDY = game_framework.getSpeed(self.speed * 7 )
            rad = math.atan2((height - y) - self.posY + player.cameraY, x - player.screenX) * 180 / math.pi
            if not self.collision(SPEEDX * math.cos(rad * math.pi / 180),0):
                self.posX += SPEEDX * math.cos(rad / 360 * 2 * math.pi)
            if not self.collision(0, SPEEDY * math.sin(rad * math.pi / 180)):
                self.posY += SPEEDY * math.sin(rad / 360 * 2 * math.pi)

            if self.DashCnt % 5 == 0:
                print ('r')
                p = Particle(self.posX,self.posY,"Clone",self.dir)
                p.addList()

            self.DashCnt -= 1
        else:
            self.DashDirX = 0
            self.DashDirY = 0
            self.god = False
        self.SetCamera(Map.stageData[Map.number])


    def SlowMotion(self):
        if not self.PushT:return

        if self.slowMotionDelay == 0:
            self.slowMotionCD = 0
            game_framework.PIXEL_PER_METER /= 5
            game_framework.MS /= 5
            self.slowMotionDelay = time.time()

        if player.slowMotionDelay != 0 and time.time() - player.slowMotionDelay > 5:
            player.slowMotionDelay = 0
            game_framework.PIXEL_PER_METER *= 5
            game_framework.MS *= 5
            player.slowMotionCD = time.time()
            self.PushT = False

    def Gravity(self):
        if self.DashCnt : return
        if not self.PushSpace:

            SPEED = game_framework.getSpeed(self.gravitySpeed)
            G_SPEED = game_framework.getSpeed(5)

            if not self.collision(0, -SPEED):
                self.posY -= SPEED
                if self.gravitySpeed < 75:
                    self.gravitySpeed += G_SPEED
            else: self.PushSpace = False

    def collision(self,valX, valY):

        stage = Map.stageData[Map.number]

        sx = self.posX//size
        sy = self.posY//size
        if sx > len(Map.stageData[Map.number][0]) : return False

        for __y in range(-1,2):
            _y = len(stage)-1 - max(0,int(sy+__y))
            if _y != pico2d.clamp(0,_y,len(stage)-1): continue
            for _x in range(-2,2,1):
                x = int(sx + _x)
                if x != pico2d.clamp(0, x, len(stage[0]) - 1): continue
                if stage[_y][x] and stage[_y][x] != 3:
                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5:  # 가로줄 충돌
                        if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                                self.posY - (y * size + (size / 2)) + valY) < size / 2 + self.h / 2 - 5:  # 세로줄 충돌
                            if abs((self.posY - self.h / 2) - (y * size + size)) <= 5:  # 땅에 착지
                                self.gravitySpeed = 1
                            self.stand = True
                            return True
                elif stage[_y][x] == 3:

                    if self.PushSpace:continue
                    if self.DashCnt:continue

                    y = len(stage) - 1 - _y
                    if abs(self.posX - (x * size + (size / 2)) + valX) < size / 2 + (self.w / 2) - 5 :# 가로줄 충돌
                         # if self.posY + (size / 2) + valY > (y * size + (size / 2)) and abs(
                         #         self.posY - (y * size + (size/2)) + valY) < 30/2 + self.h / 2 -5:  # 세로줄 충돌
                         if abs(self.posY + valY - (self.h / 2) - (y * size + (size / 2))) < 8:
                             if abs((y * size + (size / 2)) - (self.posY - (self.h / 2))) < 8:  # 포지션 조정처리(끼임방지)
                                 self.posY = (y * size + (size / 2)) + 9 + (self.h / 2)

                             if abs((self.posY - self.h / 2) - (y * size + 50 + 15)) <= 15:  # 땅에 착지
                                 self.gravitySpeed = 1
                             self.stand = True
                             return True
        self.stand = False
        return False

    def hit(self,damage,t = 0):
        if self.god : return

        if self.inv == 0:
            self.hitSound.play()
            self.hp -= damage
            self.inv = time.time() - t
            self.shooting = time.time()
            self.vibration = 8

    def ColtoMonster(self,mlist):
        for monster in mlist:
            if abs(self.posX - monster.posX)+35 < (monster.w/2) + (self.w / 2):  # 가로줄 충돌
                if abs(self.posY - monster.posY) < (monster.h / 2) + (self.h / 2)-15:  # 세로줄 충돌
                    self.hit(monster.power)
                    return

    def invincibility(self):
        if self.inv == 0 : return

        if time.time() - self.inv < 2 :
            if self.hitframe == 0 : self.hitframe = 5
            else : self.hitframe = 0
        else :
            self.hitframe = 0
            self.inv = 0

    def CoolTimeSet(self , t):
        self.DashCD += t
        self.slowMotionCD += t
        self.inv += t

    def KeyReset(self):
        self.PushL = False
        self.PushR = False
        self.clickButton = False

player = Player()


def playerInit():
    player.__init__()
    player.imageLoad('./res/idle.png')



