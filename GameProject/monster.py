from sprite import Sprite

class Monster(Sprite):
    hp = 50
    speed = 5
    gravity = True

    def Gravity(self):
        if self.gravity:
            if not self.collision(0, -self.gravitySpeed):
                self.posY -= self.gravitySpeed
                if self.gravitySpeed < 10:
                    self.gravitySpeed += 0.5


