import time

import pico2d

from sprite import Sprite

ParticleList ={"Clone":(0,0,64,100,0.1)} # 프레임번호, 액션번호 , 가로크기,세로크기,지속시간

p_list = []

class Particle(Sprite):
    image = None

    def __init__(self,pX,pY,name):
        if Particle.image == None:
            Particle.image = pico2d.load_image('./res/Clone.png')

        self.data = ParticleList[name]
        self.posX = pX
        self.posY = pY
        self.i_w = 25
        self.i_h = 25
        self.w = self.data[2]
        self.h = self.data[3]
        self.t = self.data[4]
        self.timer = time.time()

    def addList(self):
        p_list.append(self)

def ShowParticle(x,y):
    for p in p_list:
        p.Show(x,y)


