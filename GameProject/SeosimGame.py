import game_framework
import pico2d

pico2d.open_canvas(1400, 720)

import logo_state

game_framework.run(logo_state)
pico2d.close_canvas()
