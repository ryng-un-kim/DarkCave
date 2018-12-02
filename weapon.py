from pico2d import *
import game_world
import game_framework
import player
import main_state
import random
VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

PIXEL_PER_METER = (10.0/0.3)  # 10 pixel 30cm
THROW_SPEED_KMPH = 120.0  # km/hour
THROW_SPEED_MPM = (THROW_SPEED_KMPH * 1000/60)
THROW_SPEED_MPM = (THROW_SPEED_MPM / 60)
THROW_SPEED_MPM = (THROW_SPEED_MPM * PIXEL_PER_METER)


class Weapon:
    unit = None

    def __init__(self, x=100, y=100, x_velocity=5, y_velocity=5):
        self.x = x
        self.y = y
        self.u = 0
        self.x_init = x     # 초기값
        self.y_init = y     # 초기값
        self.size = 32
        self.frame = 0
        self.start_timer = get_time()
        self.end_timer = 0
        self.elapsed_time = 0
        self.x_acceleration = 0     # 가속도
        self.y_acceleration = 9.8  # 중력가속도
        self.frictional_force = 1   # 마찰력
        self.dir = 1    # 방향
        if main_state.mousecursor.x - (self.x_init - main_state.background.window_left) > 0:
            self.dir = 1
        else:     # 마우스 좌우 발사
            self.dir = -1
        self.y_throwvelocity = 0
        self.x_velocity, self.y_velocity = x_velocity, y_velocity
        self.x_throwvelocity = THROW_SPEED_MPM + (self.dir * x_velocity)

        if Weapon.unit == None:
            Weapon.unit = load_image('resource\weapon.png')

    def set_background(self, bg):
        self.bg = bg

    def damage_up(self):
        self.damage += 1

    def set_force(self, force, mass):
        self.force = force
        self.mass = mass
        self.x_acceleration = self.force/self.mass
        self.frictional_force = 1*mass
        self.u = force - self.frictional_force
        if self.u < 0:
            self.x_throwvelocity = 0
            self.u = 0
        self.x_throwvelocity += self.x_acceleration     # 던지기 직전 가속도

    def update(self):
        self.x_acceleration = 0        # 던진 후 가속도

        if self.dir == 1:
            self.x += self.x_throwvelocity * game_framework.frame_Time
        elif self.dir == -1:
            self.x -= self.x_throwvelocity * game_framework.frame_Time
        self.x_throwvelocity -= self.frictional_force

        if self.x_throwvelocity > 0:
            self.x_throwvelocity += self.u
        elif self.x_throwvelocity < 0:
            self.x_throwvelocity = 0

        if self.y_init - self.y < 16:
            self.y -= self.y_throwvelocity * game_framework.frame_Time
            self.y_throwvelocity += self.y_acceleration
        else:
            self.x_throwvelocity *= -1

        if self.y < 0 + 64 + 4:
            self.y_throwvelocity *= -0.5
            self.x_velocity = 0
        self.end_timer = get_time()
        self.elapsed_time = self.end_timer - self.start_timer

        if self.elapsed_time > 1:
            game_world.remove_object(self)

    def get_hitbox(self):
        return self.x - self.bg.window_left- 5, self.y - self.bg.window_bottom- 5, \
               self.x - self.bg.window_left+ 10, self.y - self.bg.window_bottom+ 10

    def draw(self):
        self.unit.clip_draw(self.frame * self.size, 0, 32, 32, self.x - self.bg.window_left , self.y - self.bg.window_bottom)
        draw_rectangle(*self.get_hitbox())




