import game_framework
from pico2d import *
import main_state
import loading_state
name = 'title_state'
screen_image = None
play_button = None
title_name = None
frame = 4


def enter():
    global screen_image, play_button, title_name
    screen_image = load_image('resource\screen_title.png')
    play_button = load_image('resource\click_to_start.png')
    title_name = load_image('resource\Title_name.png')

def exit():
    global screen_image, play_button, title_name
    del(screen_image, play_button, title_name)

def update():
    global frame
    frame = (frame - 1 * 8 * game_framework.frame_Time)%4


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                game_framework.change_state(loading_state)

def draw():
    global frame
    clear_canvas()
    screen_image.draw(1024/2, 764/2)
    play_button.clip_draw(0, int(frame) * 82, 452, 82, 1024/2, 764/8)
    title_name.clip_draw(0, 0, 1000, 300, 1024/2, 764 - 300)
    update_canvas()
