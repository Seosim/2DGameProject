import time
import math
import pico2d

from sprite import Sprite

ParticleList ={"Clone":(0,0,64,100,0.1),
               "HitEffect":(1,0,70,70,0.05)
               } # 프레임번호, 액션번호 , 가로크기,세로크기,지속시간

p_list = []

class Particle(Sprite):
    image = None

    def __init__(self,pX,pY,name,dir):
        if Particle.image == None:
            Particle.image = pico2d.load_image('./res/effect.png')

        self.data = ParticleList[name]
        self.posX = pX
        self.posY = pY
        self.dir = dir
        self.i_w = 16
        self.i_h = 25
        self.frame = self.data[0]
        self.action = self.data[1]
        self.w = self.data[2]
        self.h = self.data[3]
        self.t = self.data[4]
        self.timer = time.time()

    def addList(self):
        p_list.append(self)

def ShowParticle(x,y):
    for p in p_list:
        if p.dir == 1:
            p.Show(x,y)
        elif p.dir == -1:
            p.flipShow(x,y)

def UpdateParticle():
    for p in p_list:
        if time.time() - p.timer > p.t:
            p_list.remove(p)


