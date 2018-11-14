import game_framework
from pico2d import *
import main_state


name = 'title_state'
screen_image = None
play_button = None
frame = 4

def enter():
    global screen_image, play_button
    screen_image = load_image('resource\screen_title.png')
    play_button = load_image('resource\play_button_action.png')

def exit():
    global screen_image, play_button
    del(screen_image, play_button)

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
                game_framework.change_state(main_state)
def draw():
    global frame
    clear_canvas()
    screen_image.draw(1024/2, 764/2)
    play_button.clip_draw(0, int(frame) * 82, 226, 82, 1024/2, 764/8)

    update_canvas()
