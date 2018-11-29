from pico2d import *
import main_state
import game_framework
import title_state
import game_world
import player
from inventory import Inventory
from material import IvenMaterialStone, InvenMaterialWood

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

name = 'TutorialState'
inventory = None
material_stone = None
material_wood = None


def enter():
    global inventory, material_wood, material_stone
    inventory = Inventory(200, 300)
    material_stone = IvenMaterialStone(inventory.x, inventory.y)
    material_wood = InvenMaterialWood(inventory.x, inventory.y)
    game_world.add_object(inventory, 1)
    game_world.add_object(material_stone, 2)
    game_world.add_object(material_wood, 2)


def exit():
    game_world.remove_object(inventory)
    game_world.remove_object(material_stone)
    game_world.remove_object(material_wood)


def resume():
    pass


def update():
    main_state.mousecursor.update()
    inventory.update()
    material_wood.update()
    material_stone.update()


def pause():
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    inventory.draw()
    material_wood.draw()
    material_stone.draw()
    main_state.mousecursor.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()
            elif event.type == SDL_MOUSEMOTION:
                main_state.mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_i):
                game_framework.pop_state()
            else:
                main_state.player.handle_event(event)
