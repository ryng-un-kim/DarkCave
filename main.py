from pico2d import*
import game_world
import game_framework
import random
from mousecursor import MouseCursor
from player import Player
from map import Map
from item import Item
from enemy_skeleton import Skeleton


def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def handle_events():
    global see_right
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
            if event.x > player.x:
                see_right = True
            elif event.x < player.x:
                see_right = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


name = "MainState"

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

TILESIZE = 64

see_right = True
click = False
running = True
player = None
ground = None
mousecursor = None
items = None
skeletons = None
def enter():
    global player, ground, wall, mousecursor, items, skeletons
    player = Player((VIEW_WIDTH / 2), (VIEW_HEIGHT / 2))
    ground = Map()
    mousecursor = MouseCursor(100, 100)
    skeletons = [Skeleton()]
    items = [Item() for i in range(10)]
    game_world.add_object(ground, 0)
    game_world.add_object(mousecursor, 2)
    game_world.add_objects(items, 1)
    game_world.add_object(player, 1)
    game_world.add_objects(skeletons, 1)

def exit():
    game_world.clear()


def update():
    global skeleton
    for game_object in game_world.all_objects():
        game_object.update()

    for item in items:
        if collision(player, item):
            items.remove(item)
            game_world.remove_object(item)
            print('Hit!')


    # if collision(player, skeleton):
       #  print('HP -1 !')

    for weapon in player.weapons:
        for skeleton in skeletons:
            if collision(skeleton, weapon):
                skeleton.hp -= weapon.damage
                player.weapons.remove(weapon)
                game_world.remove_object(weapon)
                print(skeleton.hp)
                if skeleton.hp == 0:
                    skeleton.die()
                    game_world.remove_object(skeleton)
                    skeletons.remove(skeleton)







def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def main():
    enter()
    while running:
        handle_events()
        update()
        draw()
    exit()


if __name__ == '__main__':
    main()
