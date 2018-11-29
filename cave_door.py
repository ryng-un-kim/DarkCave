from pico2d import *
import main_state

class CaveDoor:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.ope_sound = load_wav('resource\door_open.wav')
        self.ope_sound.set_volume(100)
        if CaveDoor.image == None:
            CaveDoor.image = load_image('resource\cave_door.png')

    def set_background(self, bg):
        self.bg = bg

    def open_sound(self, cave_door):
        self.ope_sound.play()

    def get_hitbox(self):
        return self.x - 20- self.bg.window_left, \
               self.y- 20- self.bg.window_bottom, \
               self.x + 20- self.bg.window_left, \
               self.y + 20- self.bg.window_bottom

    def update(self):
        pass

    def draw(self):
        if len(main_state.skeletons) == 0:
            self.image.clip_draw(0, 0, 70, 70, self.x - self.bg.window_left, self.y - self.bg.window_bottom)
        else:
            self.image.clip_draw(64, 0, 70, 70, self.x - self.bg.window_left, self.y - self.bg.window_bottom)

        draw_rectangle(*self.get_hitbox())

