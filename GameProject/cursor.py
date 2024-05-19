from sprite import Sprite
from mapData import width, height


class Cursor(Sprite):
    def __init__(self):
        self.i_w = 50
        self.i_h = 50
        self.w = 100
        self.h = 100
        self.posX = width / 2
        self.posY = height / 2

    def UpdateCursor(self, x, y):
        self.posX = x
        self.posY = y

    def Show(self):
        self.image.clip_draw(0, 0, self.w, self.h, self.posX, height - 1 - self.posY)


aim = Cursor()
