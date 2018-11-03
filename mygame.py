import game_framework
import pico2d
import main

pico2d.open_canvas(game_framework.VIEW_WIDTH, game_framework.VIEW_HEIGHT)
game_framework.run(main)
pico2d.close_canvas()