from pico2d import *

import game_world

class Title:
    global click
    def __init__(self):
        self.image = load_image('resource/title.png')

    def draw(self):
        self.image.draw(400, 300, 900, 700)

    def update(self):
        pass


class Name:
    def __init__(self):
        self.image = load_image('resource/name.png')
        self.size_x = 506
        self.size_y = 111
        self.is_mouse_over = False  # 마우스가 위에 있는지 여부


    def draw(self):
        self.image.draw(500, 150, self.size_x, self.size_y)

    def update(self):
        if not self.is_mouse_over:
            self.size_x = self.size_x * 0.95
            self.size_y = self.size_y * 0.95
            if self.size_x <= 253:
                self.size_x = 506
                self.size_y = 111



class TitleCookie:
    def __init__(self):
        self.image = load_image('resource/title_cookie.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 148, 0, 148, 164, 170, 270, 148 * 2.2, 164 * 2.2)

    def update(self):
        self.frame = (self.frame + 1) % 4


class TitleLaser:
    def __init__(self):
        self.image = load_image('resource/title_laser.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 851, 0, 851, 101, 540, 290, 851 * 0.75, 101)

    def update(self):
        self.frame = (self.frame + 1) % 3