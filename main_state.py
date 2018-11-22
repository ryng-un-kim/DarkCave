from pico2d import*
import game_world
import game_framework
import random
import title_state
import start_state
import inventory_state
from mousecursor import MouseCursor
from player import Player, PlayerHealth
from map import Map
from item import Item
from enemy_skeleton import Skeleton
from background import FixedBackground as Background
from fear_bar import PlayerFear as Fear
from water_bar import PlayerWater as Water
from food_bar import PlayerFood as Food
from temperature_bar import PlayerTemperature as Temperature
from material import MaterialStone, MaterialWood
def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def handle_events():
    global see_right, skeletons, items, click
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            del (skeletons)
            del (items)
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            inventory.open()
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
mousecursor = None
items = None
skeletons = None
start_timer = 0
end_timer = 0
elapsed_timer = 0
player_health = None
background = None
map = None
player_fear = None
player_water = None
player_food = None
player_temperature = None
draging = False
material_stones = None
material_woods = None

def enter():
    global material_woods, material_stones, inventory, player_fear, player_water, \
        player_food, player_temperature, player, background, \
        wall, mousecursor, items, skeletons, start_timer, player_health, map
    player = Player((VIEW_WIDTH / 2), (VIEW_HEIGHT / 2))
    player_health = PlayerHealth(player.renew_hp)
    player_fear = Fear(player_health.x, player_health.y)
    player_temperature = Temperature(player_health.x, player_health.y)
    player_food = Food(player_health.x, player_health.y)
    player_water = Water(player_health.x, player_health.y)
    mousecursor = MouseCursor(100, 100)
    material_stones = [MaterialStone() for i in range(10)]
    material_woods = [MaterialWood() for i in range(10)]
    skeletons = [Skeleton() for i in range(10)]
    items = [Item() for i in range(10)]
    background = Background()
    map = Map()
    game_world.add_objects(material_woods, 1)
    game_world.add_objects(material_stones, 1)
    game_world.add_object(mousecursor, 4)
    game_world.add_objects(items, 1)
    game_world.add_object(player, 1)
    game_world.add_objects(skeletons, 1)
    game_world.add_object(player_health, 3)
    game_world.add_object(player_fear, 3)
    game_world.add_object(player_water, 3)
    game_world.add_object(player_food, 3)
    game_world.add_object(player_temperature, 3)
    game_world.add_object(background, 0)
    game_world.add_object(map, 2)

    player_fear.set_background(background)
    player.set_background(background)
    background.set_center_object(player)
    player_fear.set_position(player)

    for material_stone in material_stones:
        material_stone.set_background(background)
    for material_wood in material_woods:
        material_wood.set_background(background)
    for skeleton in skeletons:
        skeleton.set_background(background)
    for item in items:
        item.set_background(background)

def exit():
    game_world.clear()


def update():
    global start_timer, end_timer, elapsed_timer, player_health, draging

    if player.renew_hp <= 0:
        player.renew_hp = 0.2 * 100
        game_framework.change_state(title_state)

    for game_object in game_world.all_objects():
        game_object.update()

    for item in items:
        if collision(player, item):
            if player_health.renew_hp < 20:
                items.remove(item)
                game_world.remove_object(item)
                player_health.renew_hp += 1
                print('Hit!')
        elif collision(mousecursor, item):
            if click:
                item.drag(mousecursor)

    for skeleton in skeletons:
        for weapon in player.weapons:
            if collision(skeleton, weapon):
                skeleton.hp -= weapon.damage
                game_world.remove_object(weapon)
                player.weapons.remove(weapon)
                skeleton.die()
                if skeleton.hp == 0:
                    game_world.remove_object(skeleton)
                    skeletons.remove(skeleton)

    for skeleton in skeletons:
        if collision(player, skeleton):
            elapsed_timer = end_timer - start_timer
            # print(start_timer, end_timer, elapsed_timer)
            game_world.remove_object(player_health)
            player_health = PlayerHealth(player.renew_hp)
            game_world.add_object(player_health, 2)
            end_timer = get_time()
        elif collision(player_fear, skeleton):
            player_fear.skeleton_collision()

        for material_stone in material_stones:
            if collision(player, material_stone):
                game_world.remove_object(material_stone)
                material_stones.remove(material_stone)
                # player.material_stone_count(material_stone)
                player_health.set_count()

        for material_wood in material_woods:
            if collision(player, material_wood):
                game_world.remove_object(material_wood)
                material_woods.remove(material_wood)
                # player.material_stone_count(material_stone)
                player_health.set_count()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def pause():
    pass
def resume():
    pass


def main():
    enter()
    while running:
        handle_events()
        update()
        draw()
    exit()


if __name__ == '__main__':
    main()
