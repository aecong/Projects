
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
    def enter(boy, e):
        pass

    @staticmethod
    def exit(cookie, e):
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + 1) % 8
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(cookie.frame * 100, cookie.action * 100, 100, 100, cookie.x, cookie.y)


class Jump:

    @staticmethod
    def enter(cookie, e):
        if space_down(e):
            pass

    @staticmethod
    def exit(cookie, e):
        if space_down(e):
            pass
        pass

    @staticmethod
    def do(cookie):
        cookie.frame = (cookie.frame + 1) % 8
        pass

    @staticmethod
    def draw(cookie):
        cookie.image.clip_draw(cookie.frame * 100, cookie.action * 100, 100, 100, cookie.x, cookie.y)


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
        self.x, self.y = 100, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.image = load_image('resource/animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

