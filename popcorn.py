import math
import random

from pico2d import *

import game_framework
import game_world

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

class PowerCount:
    @staticmethod
    def enter(popcorn, e):
        pass

    @staticmethod
    def exit(popcorn, e):
        pass

    @staticmethod
    def do(popcorn):

        pass

    @staticmethod
    def draw(cookie):
        popcorn.image.draw(popcorn.x, 200, 100, 100)


class Shoot:
    @staticmethod
    def enter(popcorn, e):
        pass
    @staticmethod
    def exit(popcorn, e):
        pass
    @staticmethod
    def do(popcorn):
        pass

    @staticmethod
    def draw(popcorn):
        popcorn.image.draw(popcorn.x, 200, 100, 100)


class StateMachine:
    def __init__(self, popcorn):
        self.popcorn = popcorn
        self.cur_state = PowerCount
        self.transitions = {
            PowerCount: {f_down: Shoot}
            # Shoot: {time_out: Run},
        }

    def start(self):
        self.cur_state.enter(self.popcorn, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.popcorn)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                if check_event == f_down:
                    pass

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
    throwPower = 0
    def __init__(self):
        if Popcorn.image == None:
            self.image = load_image('resource/popcorn.png')
        self.x, self.y = random.randint(800, 1600), 200
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.power = 1
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        Popcorn.eat = 0
        if not Popcorn.popcorn_eat_sound:
            Popcorn.popcorn_eat_sound = load_wav('resource/bgm_popcorn.wav')
            Popcorn.popcorn_eat_sound.set_volume(32)

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        if Popcorn.eat == 1:
            self.font.draw(self.x, self.y + 60, f'{int(self.power):2d}', (255, 0, 255))

    def update(self):
        self.state_machine.update()
        # if Popcorn.eat == 1:
        #     self.power += POPCORN_SPEED_PPS * game_framework.frame_time
        #     if self.power > 10:
        #         self.power = 1
        # elif Popcorn.eat == 2:
        #     PIXEL_PER_METER = (10.0 / 0.3)
        #     POWER_SPEED_KMPH = Popcorn.throwPower * 5
        #     POWER_SPEED_MPM = POWER_SPEED_KMPH * 1000.0 / 60.0
        #     POWER_SPEED_MPS = POWER_SPEED_MPM / 60.0
        #     POWER_SPEED_PPS = POWER_SPEED_MPS * PIXEL_PER_METER
        #     self.x += POWER_SPEED_PPS * game_framework.frame_time
        #
        # elif Popcorn.eat == 0:
        #     self.x -= RUN_SPEED_PPS * game_framework.frame_time
        #
        # if self.x < -100:
        #     game_world.remove_object(self)
    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_events(self, events):
        for e in events:
            if f_down(e):
                Popcorn.throwPower = self.power
                Popcorn.eat = 2
    def handle_collision(self, group, other):
        if group == 'cookie:popcorn':
            if Popcorn.eat == 0:
            # game_world.remove_object(self)
                Popcorn.popcorn_eat_sound.play()
            # global popcorn
            # popcorn = Popcorn()
            # game_world.add_object(popcorn, 2)
            # game_world.add_collision_pair('cookie:popcorn', None, popcorn)
            Popcorn.eat = 1
            pass