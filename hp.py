from pico2d import load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Hp:
    hpCnt = 850
    x = 0
    def __init__(self):
        self.image = load_image('resource/title_laser.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(int(self.frame) * 850, 0, 850, 101, 400, 500, Hp.hpCnt, 101)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 3