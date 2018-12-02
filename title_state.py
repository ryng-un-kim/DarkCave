import game_framework
from pico2d import *
import main_state
import loading_state

name = 'title_state'
screen_image = None
play_button = None
title_name = None
title_music = None
frame = 4

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768


def enter():

    global screen_image, play_button, title_name,title_music
    screen_image = load_image('resource\screen_title.png')
    play_button = load_image('resource\click_to_start.png')
    title_name = load_image('resource\Title_name.png')
    title_music = load_music('resource\Title_music.mp3')
    loading_state.day_count = 0
    main_state.stone = 0
    main_state.wood = 0
    main_state.renew_hp, main_state.food_gauge, \
    main_state.max_hp, main_state.water_gauge, \
    main_state.fear_gauge, main_state.temp_gauge, main_state.exp_gauge = 20, 20, 20, 20, 20, 20, 0
    main_state.player_damage = 0.01 * 100
    main_state.player_max_exp = 10
    title_music.set_volume(100)
    title_music.repeat_play()



def exit():
    global screen_image, play_button, title_name,title_music
    title_music.stop()
    del(screen_image, play_button, title_name,title_music)



def update():
    global frame
    frame = (frame - 1 * 8 * game_framework.frame_Time) %4






def draw():
    global frame
    clear_canvas()
    screen_image.draw(1024/2, 764/2)
    play_button.clip_draw(0, int(frame) * 82, 452, 82, 1024/2, 764/8)
    title_name.clip_draw(0, 0, 1000, 300, 1024/2, 764 - 300)
    update_canvas()

def handle_events():
    global mousecursor
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                game_framework.change_state(loading_state)
