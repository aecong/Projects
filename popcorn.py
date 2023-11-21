import math
import random

from pico2d import *

import game_framework
import game_world

def time_out(e):
    return e[0] == 'TIME_OUT'
def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

POPCORN_SPEED_KMPH = 1.0
POPCORN_SPEED_MPM = POPCORN_SPEED_KMPH * 1000.0 / 60.0
POPCORN_SPEED_MPS = POPCORN_SPEED_MPM / 60.0
POPCORN_SPEED_PPS = POPCORN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Move:
    @staticmethod
    def enter(popcorn, e):
        pass

    @staticmethod
    def exit(popcorn, e):
        popcorn.throwPower = popcorn.power

    @staticmethod
    def do(popcorn):
        popcorn.power += POPCORN_SPEED_PPS * game_framework.frame_time
        if popcorn.power > 10:
            popcorn.power = 1
        if Popcorn.eat == 0:
            popcorn.x -= RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(popcorn):
        popcorn.image.draw(popcorn.x, 200, 100, 100)
        if Popcorn.eat == 1:
            popcorn.font.draw(popcorn.x, popcorn.y + 60, f'{int(popcorn.power):2d}', (255, 0, 255))



class Shoot:
    @staticmethod
    def enter(popcorn, e):
        pass
    @staticmethod
    def exit(popcorn, e):
        pass
    @staticmethod
    def do(popcorn):
        PIXEL_PER_METER = (10.0 / 0.3)
        POWER_SPEED_KMPH = popcorn.throwPower * 5
        POWER_SPEED_MPM = POWER_SPEED_KMPH * 1000.0 / 60.0
        POWER_SPEED_MPS = POWER_SPEED_MPM / 60.0
        POWER_SPEED_PPS = POWER_SPEED_MPS * PIXEL_PER_METER
        popcorn.x += POWER_SPEED_PPS * game_framework.frame_time
        if popcorn.x > 800:
            popcorn.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(popcorn):
        popcorn.image.draw(popcorn.x, 200, 100, 100)


class StateMachine:
    def __init__(self, popcorn):
        self.popcorn = popcorn
        self.cur_state = Move
        self.transitions = {
            Move: {f_down: Shoot},
            Shoot: {time_out: Move}
        }

    def start(self):
        self.cur_state.enter(self.popcorn, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.popcorn)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                if self.cur_state == Move and check_event == f_down:
                    Popcorn.eat = 0
                self.cur_state.exit(self.popcorn, e)
                self.cur_state = next_state
                self.cur_state.enter(self.popcorn, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.popcorn)

class Popcorn:
    image = None
    popcorn_eat_sound = None
    eat = 0
    def __init__(self):
        if Popcorn.image == None:
            self.image = load_image('resource/popcorn.png')
        self.x, self.y = random.randint(800, 1600), 200
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.power = 1
        self.throwPower = 1
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        Popcorn.eat = 0
        if not Popcorn.popcorn_eat_sound:
            Popcorn.popcorn_eat_sound = load_wav('resource/bgm_popcorn.wav')
            Popcorn.popcorn_eat_sound.set_volume(32)

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
        if self.x < -100 or self.x > 1600 - 100:
            self.x, self.y = random.randint(800, 1600), 200

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'cookie:popcorn':
            if Popcorn.eat == 0:
                Popcorn.popcorn_eat_sound.play()
                Popcorn.eat = 1
            pass