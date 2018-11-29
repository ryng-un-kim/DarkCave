import game_framework
from pico2d import *
import main_state
import game_world


name = 'loading_state'
screen_image = None
player_move = None
frame = 4
loading_time = 0.0
day_count = 0

def enter():
    global screen_image, player_move
    screen_image = load_image('resource\loading_screen.png')
    player_move = load_image('resource\player_move.png')

def exit():
    global screen_image, player_move
    del(screen_image, player_move)

def update():
    global frame, loading_time
    frame = (frame - 1 * 2 * game_framework.frame_Time)%4
    delay(0.01)
    loading_time += 0.01
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    global frame
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    screen_image.draw(1024/2, 764/2)
    player_move.clip_draw(int(frame)*64, 0, 64, 64, 1024/2, 764/2)
    update_canvas()


def handle_events():
    global loading_time, day_count
    if loading_time > 1.0:
        loading_time = 0
        day_count += 1
        game_framework.change_state(main_state)
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            
