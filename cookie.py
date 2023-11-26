from pico2d import *

import game_framework
import game_world
from hp import Hp
from rod import Rod

def space_down(e):  # 점프
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def i_down(e):  # 아이템 사용 키
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i

def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f


def time_out(e):
    return e[0] == 'TIME_OUT'


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
JUMP_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
JUMP_SPEED_MPM = JUMP_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
JUMP_SPEED_MPS = JUMP_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class ItemRun:

    @staticmethod
    def enter(cookie, e):
        if i_down(e):
            cookie.action = 1
        cookie.item_time = get_time()

    @staticmethod
    def exit(cookie, e):
        cookie.action = 3
        Cookie.speed = 0

    @staticmethod
    def do(cookie):
        if get_time() - cookie.item_time > 2.0:
            cookie.state_machine.handle_event(('TIME_OUT', 0))
        cookie.frame = (cookie.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(int(cookie.frame) * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)


class Run:

    @staticmethod
    def enter(cookie, e):
        cookie.action = 3

    @staticmethod
    def exit(cookie, e):
        cookie.action = 1

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(int(cookie.frame) * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)

class ItemJump:
    @staticmethod
    def enter(cookie, e):
        if space_down(e):
            cookie.action = 0
        cookie.jump_time = get_time()

    @staticmethod
    def exit(cookie, e):
        cookie.action = 1
        Cookie.speed = 0

    @staticmethod
    def do(cookie):
        cookie.frame = 2
        if get_time() - cookie.jump_time > 0.65:
            cookie.y -= JUMP_SPEED_PPS * game_framework.frame_time
            if cookie.y <= 200:
                cookie.state_machine.handle_event(('TIME_OUT', 0))
        else:
            cookie.y += JUMP_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(int(cookie.frame) * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)

class Jump:
    @staticmethod
    def enter(cookie, e):
        if space_down(e):
            cookie.action = 2
        cookie.jump_time = get_time()

    @staticmethod
    def exit(cookie, e):
        cookie.action = 3
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = 2
        if get_time() - cookie.jump_time > 0.65:
            cookie.y -= JUMP_SPEED_PPS * game_framework.frame_time
            if cookie.y <= 200:
                cookie.state_machine.handle_event(('TIME_OUT', 0))
        else:
            cookie.y += JUMP_SPEED_PPS * game_framework.frame_time



    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(int(cookie.frame) * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)

class StateMachine:
    def __init__(self, cookie):
        self.cookie = cookie
        self.cur_state = Run
        self.transitions = {
            Run: {space_down: Jump, i_down: ItemRun},
            Jump: {time_out: Run},
            ItemRun: {time_out: Run, space_down: ItemJump},
            ItemJump: {time_out: ItemRun}
        }

    def start(self):
        self.cur_state.enter(self.cookie, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.cookie)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                if self.cur_state == Run and check_event == i_down and \
                        (self.cookie.action == 0 or self.cookie.action == 1 or self.cookie.itemCount < 10):
                    continue
                if check_event == space_down:
                    Cookie.jump_sound.play()
                if check_event == i_down:
                    if Cookie.itemCount >= 10:
                        Cookie.itemCount -= 10
                        Cookie.transform_sound.play()

                self.cur_state.exit(self.cookie, e)
                self.cur_state = next_state
                self.cur_state.enter(self.cookie, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.cookie)


POPCORN_SPEED_KMPH = 0.1
POPCORN_SPEED_MPM = POPCORN_SPEED_KMPH * 1000.0 / 60.0
POPCORN_SPEED_MPS = POPCORN_SPEED_MPM / 60.0
POPCORN_SPEED_PPS = POPCORN_SPEED_MPS * PIXEL_PER_METER
class Cookie:
    itemCount = 0
    jump_sound = None
    transform_sound = None
    hp_sound = None
    start = False
    time = 0.0
    image = None
    def __init__(self):
        if Cookie.image == None:
            self.image = load_image('resource/cookie_sheet.png')
        self.x, self.y = 100, 200
        self.frame = 0
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        self.action = 3  # 0 : 눈빛 점프. 1 : 눈빛 달리기, 2 : 그냥 점프, 3 : 그냥 달리기
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        if not Cookie.jump_sound:
            Cookie.jump_sound = load_wav('resource/bgm_jump.wav')
            Cookie.jump_sound.set_volume(32)
        if not Cookie.transform_sound:
            Cookie.transform_sound = load_wav('resource/bgm_transform.wav')
            Cookie.transform_sound.set_volume(32)
        if not Cookie.hp_sound:
            Cookie.hp_sound = load_wav('resource/bgm_hpdecrease.wav')
            Cookie.hp_sound.set_volume(16)

    def update(self):
        self.state_machine.update()
        if self.start:
            # current_time = get_time()
            # Cookie.time += current_time - Cookie.time
            Cookie.time += POPCORN_SPEED_PPS * game_framework.frame_time
        if Rod.Mode == 2 or Rod.Mode == 3:
            self.x, self.y = Rod.X, Rod.Y
        if Rod.Mode == 0:
            self.x, self.y = 100, 200
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        if self.time < 90:
            self.font.draw(self.x, self.y + 100, f'{self.itemCount:2d}', (255, 255, 0))
            self.font.draw(600, 450, f'{Cookie.time:1f}', (255, 0, 0))
        else:
            self.font = load_font('resource/CookieRun Regular.TTF', 100)
            self.font.draw(340, 200, f'{self.itemCount:2d}', (255, 255, 0))

    def get_bb(self):
        return self.x - 40, self.y - 60, self.x + 40, self.y + 60

    def handle_collision(self, group, other):
        if group == 'cookie:obstacle':
            if self.start:
                if self.action == 2 or self.action == 3:
                    Hp.hpCnt -= 5
                    Hp.x -= 2.5
                    Cookie.hp_sound.play()

                elif self.action == 0 or self.action == 1:
                    Cookie.transform_sound.play()


        elif group == 'cookie:item':
            if self.action == 2 or self.action == 3:
                Cookie.itemCount += 1
                return
            elif self.action == 0 or self.action == 1:
                Cookie.itemCount += 2
                return

        elif group == 'cookie:floor':
            if self.action == 2 or self.action == 3:
                Hp.hpCnt -= 5
                Hp.x -= 2.5
                Cookie.hp_sound.play()
                self.y -= 5

            elif self.action == 0 or self.action == 1:
                Cookie.transform_sound.play()

        elif group == 'cookie:nothole':
            self.y = 200
