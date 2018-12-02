from pico2d import*
import pickle
import game_world
import game_framework
import random
import title_state
import level_up_state
import loading_state
from mousecursor import MouseCursor
from player import Player, PlayerHealth
from map import Map
from item import Item, WaterItem
from enemy_skeleton import Skeleton
from background import FixedBackground as Background
from fear_bar import PlayerFear as Fear
from water_bar import PlayerWater as Water
from food_bar import PlayerFood as Food
from exp_bar import Exp
from temperature_bar import PlayerTemperature as Temperature
from material import MaterialStone, MaterialWood
from darkness import Darkness
from bonfire import Bonfire
from light import Light
from cave_door import CaveDoor
from ui import UI, MouseClickImage, PauseImage, SupportImage
from levelup import StoneDamage
import pause_state



def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def handle_events():
    global see_right, skeletons, items, click, bonfire_ready, background, bonfire, light, stone, wood
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mousecursor.position(x=event.x, y=VIEW_HEIGHT - 1 - event.y)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            del (skeletons)
            del (items)
            del light
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            if collision(ui, mousecursor):
                if stone >= 2 and wood >= 2:
                    game_world.remove_object(bonfire)
                    game_world.remove_object(light)
                    bonfire = Bonfire(player.x, player.y)
                    game_world.add_object(bonfire, 3)
                    bonfire.set_background(background)
                    light = Light(bonfire.x, bonfire.y)
                    game_world.add_object(light, 3)
                    light.set_background(background)
                    stone -= 2
                    wood -= 2
        else:
            player.handle_event(event)


name = "MainState"

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768
TILESIZE = 64

renew_hp, food_gauge, water_gauge, fear_gauge, temp_gauge, exp_gauge= 20, 20, 20, 20, 20, 0
see_right = True
click = False
right_click = False
running = True
player = None
mousecursor = None
items = None
water_items = None
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
player_exp = None
player_max_exp = 10
material_stones = None
material_woods = None
darkness = None
bonfire = None
light = None
cave_door = None
ui = None
build_bar = None
stone = 0
wood = 0
mouse_right_click_image = None
main_music = None
max_hp = 20
player_damage = 0.01*100
pause_button, support_button = None, None
stone_damage = None

def get_player():
    return player


def enter():
    global stone_damage, water_items, pause_button, support_button, max_hp, player_exp, main_music, mouse_right_click_image, build_bar, ui, \
        cave_door, light, bonfire, darkness, material_woods, material_stones,  player_fear, player_water, \
        player_food, player_temperature, player, background, \
        mousecursor, items, skeletons, start_timer, player_health, map, renew_hp, food_gauge, water_gauge, fear_gauge, temp_gauge

    player = Player((VIEW_WIDTH / 2), (VIEW_HEIGHT / 2))
    player_health = PlayerHealth(player.hp)
    player_fear = Fear(player_health.x, player_health.y)
    player_temperature = Temperature(player_health.x, player_health.y)
    player_food = Food(player_health.x, player_health.y)
    player_water = Water(player_health.x, player_health.y)
    player_exp = Exp(player_health.x, player_health.y)
    mousecursor = MouseCursor(100, 100)
    material_stones = [MaterialStone() for i in range(1, 2+1)]
    material_woods = [MaterialWood() for i in range(1, 2+1)]
    skeletons = [Skeleton(0, 0.1 * 100, 0.01 * 100) for i in range(1, 5+1)]
    if loading_state.day_count > 10:
        skeletons = [Skeleton(0, 0.1 * 100, 0.01 * 100) for i in range(1, 8 + 1)]
    with open('skeleton_data_list.pickle', 'rb') as f:
        skeleton_data_list = pickle.load(f)
    for i in range(1, 20+1):
        if loading_state.day_count == i:
            for skeleton in skeletons:
                skeleton.__dict__.update(skeleton_data_list[i])
        if loading_state.day_count > 20:
            for skeleton in skeletons:
                skeleton.__dict__.update(skeleton_data_list[20])
        elif loading_state.day_count > 30:
            for skeleton in skeletons:
                skeleton.__dict__.update(skeleton_data_list[21])

    items = [Item() for i in range(random.randint(1, 5))]
    water_items = [WaterItem() for i in range(random.randint(1, 3))]

    background = Background()
    map = Map()
    darkness = Darkness()
    cave_door = CaveDoor(background.w - 50, random.randint(210, background.h - 50))
    ui = UI()
    mouse_right_click_image = MouseClickImage(903, 46)
    pause_button = PauseImage(970, 710)
    support_button = SupportImage(970, 650)
    stone_damage = StoneDamage(55, 145)
    light = Light(-300, -300)

    game_world.add_object(stone_damage, 4)
    game_world.add_object(pause_button, 4)
    game_world.add_object(support_button, 4)
    game_world.add_object(cave_door, 1)
    game_world.add_object(mouse_right_click_image, 4)
    game_world.add_object(ui, 4)
    game_world.add_objects(material_woods, 1)
    game_world.add_objects(material_stones, 1)
    game_world.add_object(mousecursor, 4)
    game_world.add_objects(items, 1)
    game_world.add_objects(water_items, 1)
    game_world.add_object(player, 1)
    game_world.add_objects(skeletons, 1)
    game_world.add_object(player_health, 3)
    game_world.add_object(player_fear, 3)
    game_world.add_object(player_water, 3)
    game_world.add_object(player_food, 3)
    game_world.add_object(player_exp, 3)
    game_world.add_object(player_temperature, 3)
    game_world.add_object(background, 0)
    game_world.add_object(map, 2)
    game_world.add_object(darkness, 2)

    darkness.set_background(background)
    player_fear.set_background(background)
    player.set_background(background)
    background.set_center_object(player)
    player_fear.set_position(player)
    cave_door.set_background(background)
    light.set_background(background)

    for material_stone in material_stones:
        material_stone.set_background(background)
    for material_wood in material_woods:
        material_wood.set_background(background)
    for skeleton in skeletons:
        skeleton.set_background(background)
    for item in items:
        item.set_background(background)
    for water_item in water_items:
        water_item.set_background(background)

    main_music = load_music('resource\main_music.mp3')
    main_music.set_volume(100)
    main_music.repeat_play()


def exit():
    global main_music, light
    game_world.clear()
    main_music.stop()
    del main_music, light


def update():
    global player_damage, max_hp, exp_gauge, renew_hp, food_gauge, water_gauge, fear_gauge, temp_gauge, stone, wood, start_timer, end_timer, elapsed_timer, player_health, bonfire, light

    if renew_hp <= 0:
        renew_hp = player.hp
        game_framework.change_state(title_state)

    for game_object in game_world.all_objects():
        game_object.update()

    for item in items:
        if collision(player, item):
            if food_gauge < 20:
                items.remove(item)
                game_world.remove_object(item)
                player.eat()
                food_gauge += 2
                if renew_hp < max_hp:
                    player.eat()
                    renew_hp += 1

    for water_item in water_items:
        if collision(player, water_item):
            if water_gauge < 20:
                water_items.remove(water_item)
                game_world.remove_object(water_item)
                player.eat()
                water_gauge += 1

    for skeleton in skeletons:
        for weapon in player.weapons:
            if collision(skeleton, weapon):
                skeleton.hp -= player_damage
                game_world.remove_object(weapon)
                player.weapons.remove(weapon)
                skeleton.hit()
                player.skeleton_hit_sound(skeleton)
                if skeleton.hp <= 0:
                    game_world.remove_object(skeleton)
                    skeletons.remove(skeleton)
                    exp_gauge += 5

    for skeleton in skeletons:
        if collision(player, skeleton):
            skeleton.attack()
            elapsed_timer = end_timer - start_timer
            end_timer = get_time()
        elif collision(player_fear, skeleton):
            player_fear.skeleton_collision()

    for material_stone in material_stones:
        if collision(player, material_stone):
            player.pickup_sound(material_stone)
            game_world.remove_object(material_stone)
            material_stones.remove(material_stone)
            # player.material_stone_count(material_stone)
            ui.set_stone_counter()

    for material_wood in material_woods:
        if collision(player, material_wood):
            player.pickup_sound(material_wood)
            game_world.remove_object(material_wood)
            material_woods.remove(material_wood)
            # player.material_stone_count(material_stone)
            ui.set_wood_counter()

    if collision(player, light):
        player_fear.recovery()
        player_temperature.recovery()

    if len(skeletons) == 0:
        if collision(player, cave_door):
            cave_door.open_sound(cave_door)
            game_framework.change_state(loading_state)


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
