from sprite import Sprite
from Hero import player

class Object(Sprite):
    freeze = False
    def Gravity(self):
        if self.freeze : return

        if not self.collision(0,-5):
            self.posY -=5
        else : self.freeze = True

    def Interaction(self):
        if abs(player.posX - self.posX) < (player.w/2+self.w/2) \
            and abs(player.posY - self.posY) < (player.h/2+self.h/2):
            return True
        else : return False


