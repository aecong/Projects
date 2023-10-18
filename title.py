from pico2d import *

import game_world

click = False


class Title:
    def __init__(self):
        self.image = load_image('resource/title.png')

    def draw(self):
        self.image.draw(400, 300, 900, 700)

    def update(self):
        if click:
            game_world.remove_object(self)


class Name:
    def __init__(self):
        self.image = load_image('resource/name.png')
        self.size_x = 506
        self.size_y = 111
        self.is_mouse_over = False  # 마우스가 객체 위에 있는지 여부

    def draw(self):
        self.image.draw(500, 150, self.size_x, self.size_y)

    def update(self):
        if not self.is_mouse_over:
            self.size_x = self.size_x * 0.95
            self.size_y = self.size_y * 0.95
            if self.size_x <= 253:
                self.size_x = 506
                self.size_y = 111

    def handle_events(self, e):
        global click
        if e[0] == 'INPUT' and e[1].type == SDL_MOUSEMOTION:
            x, y = e[1].x, e[1].y
            # 마우스 좌표와 객체 좌표를 비교하여 마우스가 객체 위에 있는지 확인
            if 500 - self.size_x / 2 < x < 500 + self.size_x / 2 and 150 - self.size_y / 2 < y < 150 + self.size_y / 2:
                self.is_mouse_over = True
                print('mouseover')
            else:
                self.is_mouse_over = False
        elif e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].key == SDLK_LEFT:
            if self.is_mouse_over:
                game_world.remove_object(self)
                click = True


class TitleCookie:
    def __init__(self):
        self.image = load_image('resource/title_cookie.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 148, 0, 148, 164, 170, 270, 148 * 2.2, 164 * 2.2)

    def update(self):
        self.frame = (self.frame + 1) % 4
        if click:
            game_world.remove_object(self)


class TitleLaser:
    def __init__(self):
        self.image = load_image('resource/title_laser.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 851, 0, 851, 101, 540, 290, 851 * 0.75, 101)

    def update(self):
        self.frame = (self.frame + 1) % 3
        if click:
            game_world.remove_object(self)
