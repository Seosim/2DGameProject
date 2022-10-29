from pico2d import *
import game_framework
import play_state

background = None
start_button = None
quit_button = None

width = 1200
height = 700

class Button():
    image = None
    def __init__(self):
        Button.image = load_image('./res/title_button.png')
        self.xSize = 270
        self.ySize = 102
        self.posX = 0
        self.posY = 0
        self.frame = 0

    def setButton(self,x,y,f):
        self.posX = x
        self.posY = y
        self.frame = f

    def draw(self):
        self.image.clip_draw(0,self.ySize*self.frame,self.xSize,self.ySize,self.posX,self.posY)

    def InClick(self,x,y):
        if self.posX - self.xSize/2 < x < self.posX+self.xSize/2:
            if self.posY - self.ySize/2 < y < self.posY+self.ySize/2:
                return True
        return False

def enter():
    global background , start_button , quit_button
    background = load_image('./res/background.png')
    start_button = Button()
    start_button.setButton(600,250,1)
    quit_button = Button()
    quit_button.setButton(600,100,0)


def draw():
    clear_canvas()
    background.draw(width / 2, height / 2, width, height)
    start_button.draw()
    quit_button.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if start_button.InClick(e.x,699-e.y):
                    game_framework.change_state(play_state)
                if quit_button.InClick(e.x,699-e.y):
                    game_framework.quit()

def update(): pass

def exit(): pass

