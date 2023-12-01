from pico2d import *

import game_framework
import game_world
from hp import Hp
def space_down(e):  # 점프
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def i_down(e):  # 아이템 사용 키
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i


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

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Slip:
    @staticmethod
    def enter(cookie, e):
        cookie.image = load_image('resource/slip.png')
        cookie.slip_time = get_time()


    @staticmethod
    def exit(cookie, e):
        cookie.image = load_image('resource/cookie_sheet.png')

    @staticmethod
    def do(cookie):
        if get_time() - cookie.slip_time > 0.25:
            cookie.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(cookie):
        cookie.image.draw(cookie.x,cookie.y, 160, 165)


class ItemRun:

    @staticmethod
    def enter(cookie, e):
        if i_down(e):
            cookie.action = 1
        cookie.item_time = get_time()

    @staticmethod
    def exit(cookie, e):
        cookie.action = 3

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
            Slip:{time_out: Run},
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
                    self.cookie.itemCount -= 10
                    continue
                self.cur_state.exit(self.cookie, e)
                self.cur_state = next_state
                self.cur_state.enter(self.cookie, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.cookie)



class Cookie:
    def __init__(self):
        self.image = load_image('resource/cookie_sheet.png')
        self.x, self.y = 100, 200
        self.frame = 0
        self.hp = 100
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        self.itemCount = 0
        self.action = 3  # 0 : 눈빛 점프. 1 : 눈빛 달리기, 2 : 그냥 점프, 3 : 그냥 달리기 4 : 넘어지기
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()
        if isinstance(self.state_machine.cur_state, Slip):
            self.state_machine.cur_state.do(self)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y + 100, f'{self.itemCount:2d}', (255, 255, 0))

    def get_bb(self):
        return self.x - 40, self.y - 60, self.x + 40, self.y + 60

    def handle_collision(self, group, other):
        if group == 'cookie:obstacle':
            Hp.hpCnt -= 5
            return
        elif group == 'cookie:item':
            self.itemCount += 1
            return
