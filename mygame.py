import game_framework
import pico2d
import main

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

pico2d.open_canvas(VIEW_WIDTH, VIEW_HEIGHT)
game_framework.run(main)
pico2d.close_canvas()