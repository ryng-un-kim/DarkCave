from pico2d import *
import main_state
import game_framework
import game_world


VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

name = 'PauseState'

support_screen = None

def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def enter():
    global support_screen
    support_screen = load_image('resource\support_screen.png')


def exit():
    global support_screen
    del support_screen


def resume():
    pass


def update():
    main_state.mousecursor.update()



def pause():
    pass


def draw():
    global support_screen
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    support_screen.draw(VIEW_WIDTH/2, VIEW_HEIGHT/2)
    main_state.mousecursor.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_MOUSEMOTION:
                main_state.mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
            elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                if main_state.collision(main_state.support_button, main_state.mousecursor):
                    game_framework.pop_state()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()
            else:
                main_state.player.handle_event(event)
