from pico2d import *
import main_state
import game_framework
import title_state
import game_world
import player
from levelup import LevelUp
from weapon import Weapon
from Exp_bar import HealthUP, DamageUP

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

name = 'LevelUpState'
levelup = None
health_up = None
damage_up = None
weapon = None


def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def enter():
    global weapon, levelup, health_up, damage_up
    levelup = LevelUp(200, 300)
    health_up = HealthUP(levelup.x - 32, levelup.y)
    damage_up = DamageUP(levelup.x + 32, levelup.y)
    weapon = Weapon()
    game_world.add_object(levelup, 1)
    game_world.add_object(health_up, 2)
    game_world.add_object(damage_up, 2)


def exit():
    game_world.remove_object(levelup)
    game_world.remove_object(health_up)
    game_world.remove_object(damage_up)


def resume():
    pass


def update():
    main_state.mousecursor.update()
    levelup.update()
    health_up.update()
    damage_up.update()

    if collision(health_up, main_state.mousecursor):
        health_up.frame = 64
    else:
        health_up.frame = 0

    if collision(damage_up, main_state.mousecursor):
        damage_up.frame = 64
    else:
        damage_up.frame = 0
def pause():
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    levelup.draw()
    health_up.draw()
    damage_up.draw()
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
                if collision(health_up, main_state.mousecursor):
                    main_state.max_hp += 1
                    game_framework.pop_state()
                if collision(damage_up, main_state.mousecursor):
                    main_state.player_damage += 1
                    game_framework.pop_state()
            else:
                main_state.player.handle_event(event)
