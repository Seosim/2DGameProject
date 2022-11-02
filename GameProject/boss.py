import pico2d
from sprite import Sprite
import random
from Hero import player

class Boss(Sprite):
    def __init__(self):
        self.image = pico2d.load_image('./res/Skull.png')
        self.hp = 1000
        self.i_w = 510
        self.i_h = 0
        self.posX = 600
        self.posY = 400
        self.w = 510
        self.h = 558
        self.l_hand = Sprite()
        self.r_hand = Sprite()
        self.ldir = 250
        self.rdir = 250
        self.skillDelay = 0

    def UpdateHand(self):
        self.ldir = random.randint(100,500)
        self.rdir = random.randint(100,500)

    def MoveHand(self):
        if self.ldir > self.l_hand.posY : self.l_hand.posY += 1
        elif  self.ldir < self.l_hand.posY : self.l_hand.posY -= 1

        if self.rdir > self.r_hand.posY : self.r_hand.posY += 1
        elif  self.rdir < self.r_hand.posY : self.r_hand.posY -= 1

    def update(self):
        self.MoveHand()
        self.skillDelay += 1
        self.frame = (self.frame+ 0.05) % 2
        if self.skillDelay % 300 == 0:
            self.UpdateHand()


    def Draw(self):
        self.Show(player.cameraX)
        self.r_hand.Show(player.cameraX)
        self.l_hand.Show(player.cameraX)

skul = Boss()

def InitBoss():
    skul.l_hand.imageLoad('./res/Lhand.png')
    skul.r_hand.imageLoad('./res/Lhand.png')
    skul.l_hand.i_w = 111
    skul.r_hand.i_w = 111
    skul.l_hand.i_h = 0
    skul.r_hand.i_h = 0
    skul.l_hand.w =  111
    skul.l_hand.h = 102
    skul.r_hand.w =  111
    skul.r_hand.h = 102
    skul.l_hand.posX = skul.posX - 300
    skul.r_hand.posX = skul.posX + 300





