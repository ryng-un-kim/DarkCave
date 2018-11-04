from pico2d import *
import settings
import game_framework
import player
import main


class Weapon:
    unit = None

    def __init__(self, x=100, y=100, velx=5, vely=5):
        self.x = x
        self.y = y
        self.fx = x     # 초기값
        self.fy = y     # 초기값
        self.SIZE = 32
        self.frame = 0
        self.first_timer = get_time()
        self.timer = 0
        self.etime = 0
        self.accx = 0     # 가속도
        self.accy = 0.98  # 중력가속도
        self.Fric = 1   # 저항
        self.dir = 1    # 방향
        self.ThrowVelY = 0
        self.velx, self.vely = velx, vely
        if main.mouse.x - self.x > 0:
            self.switch = 1
        else:
            self.switch = 0     # 마우스 좌우 발사
            self.dir = -1
        self.ThrowVelX = player.THROW_SPEED_MPM + (self.dir * velx) # 돌 던지는 속도
        if Weapon.unit == None:
            Weapon.unit = load_image('weapon.png')

    def setForce(self, force, mass):
        self.force = force
        self.mass = mass
        self.accx = self.force/self.mass
        self.Fric = 1*mass
        self.u = force - self.Fric
        if self.u < 0:
            self.ThrowVelX = 0
            self.u = 0
        self.ThrowVelX += self.accx     # 던지기 직전 가속도
        print(self.accx)

    def update(self):
        self.accx = 0        # 던진 후 가속도
        if self.switch == 1:
            self.x += self.ThrowVelX * game_framework.frame_Time
        elif self.switch == 0:
            self.x -= self.ThrowVelX * game_framework.frame_Time
        self.ThrowVelX -= self.Fric
        if self.ThrowVelX > 0:
            self.ThrowVelX += self.u
        elif self.ThrowVelX < 0:
            self.ThrowVelX = 0
        if self.fy - self.y < 12:
            self.y -= self.ThrowVelY * game_framework.frame_Time
            self.ThrowVelY += self.accy
        else:
            self.ThrowVelX *= -1


        if self.y < 0 + 64 + 4:
            self.ThrowVelY *= -0.5
            self.velx = 0
        self.timer = get_time()
        self.etime = self.timer - self.first_timer
        print(self.accx)
        if self.x > game_framework.VIEW_WIDTH - 64 - 4:
            self.ThrowVelX *= -1
            self.velx *= -0.5
        if self.etime > 1:
            settings.remove_object(self)




    def draw(self):
        self.unit.clip_draw(self.frame * self.SIZE, 0, 32, 32, self.x, self.y)




