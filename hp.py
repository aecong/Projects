from pico2d import load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Hp:
    def __init__(self):
        self.image = load_image('resource/hp_laser.png')
        self.frame = 0
        self.hpCnt = 850
    def draw(self):
        self.image.clip_draw(self.frame * 850, 0, 850, 101, 400, 500, self.hpCnt * 0.75, 101)

    def update(self):
        self.frame = (self.frame + 1) % 3

