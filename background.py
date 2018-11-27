from pico2d import *


class FixedBackground:
    image = None
    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        if FixedBackground.image == None:
            FixedBackground.image = load_image('resource\Background.png')
        self.w = self.image.w
        self.h = self.image.h


    def set_center_object(self, player):
        self.center_object = player

    def update(self):
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width//2, self.w - self.canvas_width )
        self.window_bottom = clamp(0, int(self.center_object.y) - self.canvas_height//2, self.h - self.canvas_height)

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0)
