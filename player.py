import game_framework
from pico2d import*
import game_world
import random
import main_state
import pause_state
import support_state
import start_state
from effect import Effect
from weapon import Weapon
import enemy_skeleton
import mousecursor


PIXEL_PER_METER = (10.0/0.3)  # 10 pixel 30cm

RUN_SPEED_KMPH = 20.0  # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000/60)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# Player Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, \
DOWN_UP, LMOUSE_DOWN, LMOUSE_UP, RMOUSE_DOWN, RMOUSE_UP, IdleState = range(13)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None, SDL_BUTTON_LEFT): LMOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None, SDL_BUTTON_LEFT): LMOUSE_UP,
    (SDL_KEYDOWN, SDLK_s, None): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_w, None): UP_DOWN,
    (SDL_KEYDOWN, SDLK_a, None): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_d, None): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_s, None): DOWN_UP,
    (SDL_KEYUP, SDLK_w, None): UP_UP,
    (SDL_KEYUP, SDLK_a, None): LEFT_UP,
    (SDL_KEYUP, SDLK_d, None): RIGHT_UP
}
weapon = None


class IdleState:
    @staticmethod
    def enter(player, event):
        if event == LEFT_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHT_DOWN:
            player.x_velocity += RUN_SPEED_PPS
        elif event == UP_DOWN:
            player.y_velocity += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            player.y_velocity -= RUN_SPEED_PPS

    @staticmethod
    def exit(player, event):
        if event == LMOUSE_DOWN:
            main_state.click = True
            player.throw_weapon()
        elif event == LMOUSE_UP:
            main_state.click = False

    @staticmethod
    def do(player):
        if main_state.mousecursor.x > player.x - player.bg.window_left:
            main_state.see_right = True
        elif main_state.mousecursor.x < player.x - player.bg.window_left:
            main_state.see_right = False
        player.x = clamp(0 + 48, player.x, player.bg.w - 48)
        player.y = clamp(0 + 200, player.y, player.bg.h - 48)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        for skeleton in main_state.skeletons:
            if main_state.collision(player, skeleton):
                if main_state.elapsed_timer > 1:
                    player.damage_collision(skeleton.damage)
                player.font.draw(cx - 20, cy + 25 + random.randint(400, 550) * game_framework.frame_Time, 'Fear', (255, 0, 0))
        if main_state.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 128, 64, 64, cx, cy)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 196, 64, 64, cx, cy)


class MoveState:
    @staticmethod
    def enter(player, event):
        if event == LEFT_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHT_DOWN:
            player.x_velocity += RUN_SPEED_PPS
        elif event == UP_DOWN:
            player.y_velocity += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == UP_UP:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            player.y_velocity += RUN_SPEED_PPS
        player.start_timer = get_time()

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x = clamp(0 + 48, player.x, player.bg.w - 48)
        player.y = clamp(0 + 200, player.y, player.bg.h - 48)
        if main_state.mousecursor.x > player.x - player.bg.window_left:
            main_state.see_right = True
        elif main_state.mousecursor.x < player.x - player.bg.window_left:
            main_state.see_right = False
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4
        player.x += player.x_velocity * game_framework.frame_Time
        player.y += player.y_velocity * game_framework.frame_Time
        if player.x_velocity == 0 and player.y_velocity == 0:
            player.end_timer = get_time()
            player.elapsed_timer = player.end_timer - player.start_timer
            if player.elapsed_timer > 0.3:
                player.add_event(IdleState)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        for skeleton in main_state.skeletons:
            if main_state.collision(player, skeleton):
                if main_state.elapsed_timer > 1:
                    player.damage_collision(skeleton.damage)
                player.font.draw(cx - 20, cy + 25 + random.randint(400, 550) * game_framework.frame_Time, 'Fear', (255, 0, 0))
        if main_state.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 0, 64, 64, cx, cy)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 64, 64, 64, cx, cy)


class AttackState:
    @staticmethod
    def enter(player, event):

        if event == LMOUSE_DOWN:
            main_state.click = True
            if player.attack_elapsed_timer > 0.2:
                player.effect_act()
                player.throw_weapon()
                player.attack_start_timer = get_time()
            if main_state.collision(main_state.pause_button, main_state.mousecursor):
                game_framework.push_state(pause_state)
            elif main_state.collision(main_state.support_button, main_state.mousecursor):
                game_framework.push_state(support_state)
        elif event == LMOUSE_UP:
            main_state.click = False

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x = clamp(0 + 48, player.x, player.bg.w - 48)
        player.y = clamp(0 + 200, player.y, player.bg.h - 48)
        if main_state.mousecursor.x > player.x - player.bg.window_left:
            main_state.see_right = True
        elif main_state.mousecursor.x < player.x - player.bg.window_left:
            main_state.see_right = False
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4
        player.x += player.x_velocity * game_framework.frame_Time
        player.y += player.y_velocity * game_framework.frame_Time
        player.attack_end_timer = get_time()
        player.attack_elapsed_timer = player.attack_end_timer - player.attack_start_timer

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        for skeleton in main_state.skeletons:
            if main_state.collision(player, skeleton):
                if main_state.elapsed_timer > 1:
                    player.damage_collision(skeleton.damage)
                player.font.draw(cx - 20, cy + 25 + random.randint(400, 550) * game_framework.frame_Time, 'Fear', (255, 0, 0))

        if main_state.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 0, 64, 64, cx, cy)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 64, 64, 64, cx, cy)


next_state_table = {
    IdleState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: IdleState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: IdleState,
                LEFT_UP: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: IdleState, DOWN_UP: IdleState,
                IdleState: IdleState},
    MoveState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: MoveState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: MoveState, LEFT_UP: MoveState,
                IdleState: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: MoveState, DOWN_UP: MoveState,
                },
    AttackState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: AttackState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: MoveState, LEFT_UP: MoveState,
                  IdleState: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: MoveState, DOWN_UP: MoveState,

    }

}


class Player:
    unit = None
    weapons = []

    def __init__(self, x, y, x_velocity=0, y_velocity= 0, renew_hp=0.2*100):
        self.x = x
        self.y = y
        self.cx = x
        self.cy = y
        self.x_acceleration = 10
        self.y_acceleration = 0
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.size = 64
        self.hitbox_size = 30
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 18)
        self.event_que = []
        self.cur_state = IdleState
        self.start_timer = 0
        self.end_timer = 0
        self.elapsed_timer = 0
        self.attack_start_timer = 0
        self.attack_end_timer = 0
        self.attack_elapsed_timer = 0
        self.hp = main_state.renew_hp
        self.stone_count = 0
        self.renew_hp = renew_hp
        self.hit_sound = load_wav('resource\skele_hit.wav')
        self.hit_sound.set_volume(30)
        self.eat_sound = load_wav('resource\eat_food.wav')
        self.eat_sound.set_volume(32)
        self.get_item = load_wav('resource\pickup.wav')
        self.get_item.set_volume(32)
        self.cur_state.enter(self, None)
        if Player.unit == None:
            Player.unit = load_image('resource\player_animation.png')

    def pickup_sound(self, material_stone):
        self.get_item.play()

    def eat(self):
        self.eat_sound.play()

    def skeleton_hit_sound(self, weapon):
        self.hit_sound.play()

    def effect_act(self):
        effect = Effect(self.cx, self.cy, self.x_velocity, self.y_velocity)
        game_world.add_object(effect, 1)

    def material_stone_count(self, material_stone):
        self.stone_count += 1

    def get_hitbox(self):
        return (self.x - self.bg.window_left - self.hitbox_size / 2), (self.y - self.bg.window_bottom - self.hitbox_size / 2), \
               (self.x - self.bg.window_left + self.hitbox_size / 2), (self.y - self.bg.window_bottom+ self.hitbox_size / 2)

    def throw_weapon(self):
        self.weapons = [Weapon(self.x, self.y, self.x_velocity, self.y_velocity) for i in range(1)]
        game_world.add_objects(self.weapons, 1)
        for self.weapon in self.weapons:
            self.weapon.set_background(self.bg)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def damage_collision(self, skeleton_damage):
        main_state.renew_hp -= skeleton_damage
        main_state.start_timer = get_time()

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w // 2
        self.y = self.bg.h // 2

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cx = self.x - self.bg.window_left
        self.cy = self.y - self.bg.window_bottom
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_hitbox())

    def handle_event(self, event):
        if (event.type, event.key, event.button) in key_event_table:
            key_event = key_event_table[(event.type, event.key, event.button)]
            self.add_event(key_event)


class PlayerHealth():
    image = None

    def __init__(self, material_counter= 0):
        self.x=110
        self.y=764/14
        self.material_counter = material_counter
        if PlayerHealth.image == None:
            PlayerHealth.image = load_image('resource\health.png')
        self.health = main_state.renew_hp * 128/ main_state.max_hp
        self.small_jua_font = load_font('ENCR10B.TTF', 14)
        self.jua_font = load_font('ENCR11B.TTF', 20)

    def damage_food(self):
        main_state.renew_hp -= 1
        main_state.start_timer = get_time()

    def damage_water(self):
        main_state.renew_hp -= 1
        main_state.start_timer = get_time()

    def damage_temp(self):
        main_state.renew_hp -= 1
        main_state.start_timer = get_time()

    def damage_fear(self):
        main_state.renew_hp -= 1
        main_state.start_timer = get_time()

    def set_count(self):
        self.material_counter += 1

    def update(self):
        self.health = main_state.renew_hp * 128 / main_state.max_hp

    def draw(self):
        self.image.clip_draw(0,0,int(self.health),16,self.x-(128-int(self.health))/2 ,self.y)
        self.jua_font.draw(80, 764 / 10, 'Health                  Fear             Temperature             Food                  Water                     Exp', (255, 255, 255))
        self.small_jua_font.draw(92, 764 / 20,'%2.0f/%2.0f' % (main_state.renew_hp,main_state.max_hp), (255, 255, 255))

