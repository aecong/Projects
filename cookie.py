from pico2d import *

import game_framework
import game_world


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

class Run:

    @staticmethod
    def enter(cookie, e):
        cookie.action = 3

    @staticmethod
    def exit(cookie, e):
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(int(cookie.frame) * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)


class Jump:
    @staticmethod
    def enter(cookie, e):
        global up
        if space_down(e):
            cookie.action = 2
            up = 1
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
            Run: {space_down: Jump, time_out: Slip},
            Jump: {time_out: Run},
            Slip:{time_out: Run}
        }

    def start(self):
        self.cur_state.enter(self.cookie, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.cookie)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
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

        self.itemCount = 0
        self.action = 3  # 0 : 눈빛 점프. 1 : 눈빛 달리기, 2 : 그냥 점프, 3 : 그냥 달리기
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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 60, self.x + 40, self.y + 60

    def handle_collision(self, group, other):
        if group == 'cookie:obstacle':
            self.hp -= 1
        elif group == 'cookie:item':
            self.itemCount += 1
            print(self.itemCount)
            return
