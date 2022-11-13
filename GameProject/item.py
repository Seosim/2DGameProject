from object import Object,o_list
from weapon import gun

WeaponList = {0 : (10,8,35,0.5,48,48,50,50,'./res/pistolR.png'),
              1 : (5,30,35,0.2,130,60,120,50,'./res/M4.png')} #데미지,장탄수,총알속도,연사력,이미지크기,실제크기,이미지이름

class Item_W(Object):
    def __init__(self, iw, ih, sizeX, sizeY, pX, pY, name):
        self.i_w = iw
        self.i_h = ih
        self.w = sizeX
        self.h = sizeY
        self.posX = pX
        self.posY = pY
        self.action = 0
        self.imageLoad(name)
        self.data = WeaponList[1]
        self.name = self.data

    def Interaction(self):
        gun.damage = self.data[0]
        gun.maxAmmo = self.data[1]
        gun.ammo = self.data[1]
        gun.speed = self.data[2]
        gun.attack_speed = self.data[3]
        gun.i_w = self.data[4]
        gun.i_h = self.data[5]
        gun.w = self.data[6]
        gun.h = self.data[7]
        gun.imageLoad(self.data[8])

    def addList(self):
        o_list.append(self)