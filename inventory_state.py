from pico2d import *
import game_framework
import game_world
import main_state

inventory_image = None
def enter():
    global inventory_image
    inventory_image = load_image('resource\inventory.png')

def exit():
    global inventory_image
    del inventory_image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
            if event.x > player.x:
                main_state.see_right = True
            elif event.x < player.x:
                main_state.see_right = False
        else:

            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_i):
                game_framework.pop_state()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()


def update():
    pass

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    inventory_image.draw(600, 200)
    update_canvas()



def exit():
    pass



