from object import Object,o_list
import loading_state
from mapData import *
from boss import *

class Portal(Object):
    def Interaction(self):
        Map.NextMap()
        player.posX = 300
        #self.posX = 9700
        game_framework.push_state(loading_state)
        if Map.number == 2:
            InitBoss()

    def addList(self):
        o_list.append(self)

