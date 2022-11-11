from sprite import Sprite
from Hero import player
from MapData import width,height

size = 100

class object(Sprite):
    def __init__(self,iw,sizeX,sizeY):
        self.i_w = iw
        self.w = sizeX
        self.h = sizeY

    def Show(self,cam_x,posX,posY):
        if -150 < (x * size) + size / 2 - cam_x < width+100:#화면에 안보일땐 출력x
            obj_1.image.clip_draw(self.i_w, 0, self.w, self.h, posX - cam_x,posY + (self.h-size)/2-player.cameraY )
            #obj들은 모두 하나의 이미지를 쓰기 때문에 obj1의 이미지 출력으로만 출력

obj_list = []

obj_0 = None
obj_list.append(obj_0)

obj_1 = object(0,153,186) # 철창
obj_list.append(obj_1)

obj_2 = object(153,117,144) # 시든나무
obj_list.append(obj_2)

obj_3 = object(288,192,96) # 강아지 동상
obj_list.append(obj_3)

obj_4 = object(483,39,132) # 소형 전등
obj_list.append(obj_4)

obj_5 = object(534,222,126) # 부숴진 철장
obj_list.append(obj_5)

obj_6 = object(774,120,144) # 독수리 동상
obj_list.append(obj_6)

obj_7 = object(893,48,87) # 클로버 동상
obj_list.append(obj_7)

obj_8 = object(946,26,100) # 사슬 1번과 같이 사용
obj_list.append(obj_8)

obj_9 = object(971,102,177) # 큰 가로등
obj_list.append(obj_9)

obj_10 = object(1080,63,39) # 오크통
obj_list.append(obj_10)




def LoadObj(stage):
    global x,y
    # cameraX = Hero.player.posX - (1200 / 2)
    # #카메라가 맵밖을 촬영하지 않게 설정
    # if cameraX <= 0: cameraX = 0
    # elif size * len(stage[6]) - Hero.player.posX <= 600: cameraX = size * len(stage[6]) - 1200

    x = 0
    y = len(stage)-1

    for _y in stage:
        for _x in _y:
            if _x:
                obj_list[_x].Show(player.cameraX,(x * size) + size / 2,(y * size) + size / 2)
            x += 1
        y -= 1
        x = 0
    x = 0
    y = 6

