
from pico2d import *
import game_world


def space_down(e):  # 점프
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def i_down(e):  # 아이템 사용 키
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i


def time_out(e):
    return e[0] == 'TIME_OUT'


class Run:

    @staticmethod
    def enter(cookie, e):
        pass

    @staticmethod
    def exit(cookie, e):
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + 1) % 4
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(cookie.frame * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)


class Jump:

    @staticmethod
    def enter(cookie, e):
        if space_down(e):
            cookie.action = 2

    @staticmethod
    def exit(cookie, e):
        cookie.y = 120
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + 1) % 4
        if cookie.y <= 200:
            cookie.y += 5
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(cookie.frame * 160, cookie.action * 165, 160, 165, cookie.x, cookie.y)


class StateMachine:
    def __init__(self, cookie):
        self.cookie = cookie
        self.cur_state = Run
        self.transitions = {
            Run: {space_down: Jump},
            Jump: {time_out: Run}
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
        self.x, self.y = 100, 120
        self.frame = 0
        self.action = 3  # 0 - 눈빛 점프 1 - 눈빛 달리기 2 - 그냥 점프 3 - 그냥 달리기
        self.image = load_image('resource/cookie_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

