from sprite import Sprite
from Hero import player
import map

width = 1200
height = 700

class Weapon(Sprite):
    cameraX = player.posX - (1200 / 2)
    damage = 10
    attack_speed = 50
    dis = 15
    def __init__(self):
        self.posX = player.posX
        self.posY = player.posY
        self.w = 50
        self.h = 50
        self.i_w = 48
        self.i_h = 48


    def Show(self):
        if  width/2 > self.posX: # 맵 가장 왼쪽으로 가게된다면 플레이어가 맵에서 좌로 움직임
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h,self.posX+self.dis,self.posY)
        elif self.posX >= map.size * len(map.stage[6]) - width/2: # 맵 가장 오른쪽으로 가게된다면 플레이어가 맵에서 우로 움직임
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h,width - (len(map.stage[6])*map.size-self.posX)+self.dis ,self.posY)
        else :
            self.image.clip_draw(self.i_w * int(self.frame), self.i_h * self.action, self.w, self.h, width / 2+ self.dis, self.posY)



    def Update(self):
        self.dis = 15 * (-1 + (self.action * 2))
        self.cameraX = player.posX - (1200 / 2)
        self.posX = player.posX
        self.posY = player.posY - 15
        self.action = player.action
        self.Show()



pistol = Weapon()






