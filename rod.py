
from pico2d import *

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

MOVE_X_SPEED_KMPH = 40.0
MOVE_Y_SPEED_KMPH = 90.0
MOVE_X_SPEED_MPM = MOVE_X_SPEED_KMPH * 1000.0 / 60.0
MOVE_Y_SPEED_MPM = MOVE_Y_SPEED_KMPH * 1000.0 / 60.0
MOVE_X_SPEED_MPS = MOVE_X_SPEED_MPM / 60.0
MOVE_Y_SPEED_MPS = MOVE_Y_SPEED_MPM / 60.0
MOVE_X_SPEED_PPS = MOVE_X_SPEED_MPS * PIXEL_PER_METER
MOVE_Y_SPEED_PPS = MOVE_Y_SPEED_MPS * PIXEL_PER_METER

MOVE_X1_SPEED_KMPH = 50.0
MOVE_Y1_SPEED_KMPH = 120.0
MOVE_X1_SPEED_MPM = MOVE_X1_SPEED_KMPH * 1000.0 / 60.0
MOVE_Y1_SPEED_MPM = MOVE_Y1_SPEED_KMPH * 1000.0 / 60.0
MOVE_X1_SPEED_MPS = MOVE_X1_SPEED_MPM / 60.0
MOVE_Y1_SPEED_MPS = MOVE_Y1_SPEED_MPM / 60.0
MOVE_X1_SPEED_PPS = MOVE_X1_SPEED_MPS * PIXEL_PER_METER
MOVE_Y1_SPEED_PPS = MOVE_Y1_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Rod:
    image = None
    frame = 0
    size = 0
    Mode = None
    X, Y = 100, 200
    def __init__(self):
        if Rod.image == None:
            self.image = load_image('resource/rod.png')
        self.x, self.y = 290, 200
        self.angle = 0
        Rod.Mode = 0

    def draw(self):
        if Rod.Mode == 1:
            self.image.clip_draw(int(Rod.frame) * 851, 0, 851, 101, self.x, self.y, 340, 40)
        elif Rod.Mode == 2:
            self.image.clip_composite_draw(int(Rod.size) * 851, 0, 851, 101, -self.angle / 2, '', self.x, self.y,340, 40)
        elif Rod.Mode == 3:
            self.image.clip_composite_draw(int(Rod.size) * 851, 0, 851, 101, -self.angle / 2, '', self.x, self.y,340, 40)


    def update(self):
        if Rod.Mode == 0:
            Rod.X, Rod.Y = 100, 200
        if Rod.Mode == 1:
            Rod.frame = (Rod.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        elif Rod.Mode == 2:
            if self.angle == 0:
                Rod.X = self.x - 170
            self.angle += 0.1
            if int(Rod.size) == 0 or int(Rod.size) == 2:
                self.x = 200 + Rod.size * math.cos(self.angle)
                self.y = 300 + Rod.size * math.sin(self.angle)
                Rod.X += MOVE_X1_SPEED_PPS * game_framework.frame_time
                Rod.Y += MOVE_Y1_SPEED_PPS * game_framework.frame_time
            elif int(Rod.size) == 1 or int(Rod.size) == 3:
                self.x = 200 + Rod.size * math.cos(self.angle)
                self.y = 200 + Rod.size * math.sin(self.angle)
                Rod.X += MOVE_X_SPEED_PPS * game_framework.frame_time
                Rod.Y += MOVE_Y_SPEED_PPS * game_framework.frame_time
            if self.angle > 3.5:
                Rod.Mode = 3

        elif Rod.Mode == 3:
            self.angle += 0.1
            if int(Rod.size) == 0 or int(Rod.size) == 2:
                self.x = 200 + Rod.size * math.cos(self.angle)
                self.y = 300 + Rod.size * math.sin(self.angle)
                Rod.X += MOVE_X1_SPEED_PPS * game_framework.frame_time
                Rod.Y -= MOVE_Y1_SPEED_PPS * game_framework.frame_time
            elif int(Rod.size) == 1 or int(Rod.size) == 3:
                self.x = 200 + Rod.size * math.cos(self.angle)
                self.y = 200 + Rod.size * math.sin(self.angle)
                Rod.X += MOVE_X_SPEED_PPS * game_framework.frame_time
                Rod.Y -= MOVE_Y_SPEED_PPS * game_framework.frame_time
            if self.angle > 7.0:
                self.x, self.y = 290, 200
                self.angle = 0
                Rod.Mode = 0
