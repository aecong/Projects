from pico2d import *

import game_framework
from popcorn import Popcorn
from rod import Rod

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

ROD_SPEED_KMPH = 20.0
ROD_SPEED_MPM = ROD_SPEED_KMPH * 1000.0 / 60.0
ROD_SPEED_MPS = ROD_SPEED_MPM / 60.0
ROD_SPEED_PPS = ROD_SPEED_MPS * PIXEL_PER_METER

class Badbackground:
    image = None
    def __init__(self):
        if Badbackground.image == None:
            self.image = load_image('resource/badending_back.png')
        self.bgm = load_music('resource/bgm_badending.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        self.x, self.y = 200, 300
        self.angle = 0
    def draw(self):
        self.image.draw(400, 300, 800, 600)
        self.font.draw(self.x, self.y, f'저런... 통과하지 못하셨네요...', (15, 14, 24))
        self.font.draw(self.x, self.y - 50, f'다시 도전하려면 r키를 누르세요!', (15, 14, 24))

    def update(self):
        self.angle += 0.1
        if self.angle >= 6.0:
            self.angle = 0
        self.x = 200 + 5 * math.cos(self.angle)
        self.y = 300 + 5 * math.sin(self.angle)

class Happybackground:
    image = None
    def __init__(self):
        if Happybackground.image == None:
            self.image = load_image('resource/happyending_back.png')
        self.bgm = load_music('resource/bgm_happyending.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        self.font = load_font('resource/CookieRun Regular.TTF', 32)
        self.x = 150
        global size
        global zoomin
        zoomin = True
        size = 32
    def draw(self):
        global size
        self.image.draw(400, 300, 800, 600)
        self.font = load_font('resource/CookieRun Regular.TTF', size)
        self.font.draw(self.x, 50, f'다시 시작하려면 r키를 누르세요!', (255, 255, 0))

    def update(self):
        global size
        global zoomin
        if zoomin == True:
            size += 1
            if size >= 45:
                zoomin = False
        else:
            size -= 1
            if size < 32:
                zoomin = True

        pass


class Polejumpbackground:
    image = None
    def __init__(self):
        self.x = 0
        if Polejumpbackground.image == None:
            self.image = load_image('resource/back3.png')
            self.font = load_font('resource/CookieRun Regular.TTF', 32)

    def draw(self):
        self.image.draw(self.x, 300, 1120, 600)
        self.image.draw(self.x+1120, 300, 1120, 600)
        self.image.draw(self.x+2240, 300, 1120, 600)
        self.font.draw(0,580,f'v키를 눌러 장대를 꺼내세요!',(255, 0, 0))
    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= -1120:
            self.x = 0
class Shotputbackground:
    image = None
    def __init__(self):
        self.x = 0
        if Shotputbackground.image == None:
            self.image = load_image('resource/back2.png')
            self.font = load_font('resource/CookieRun Regular.TTF', 32)

    def draw(self):
        self.image.draw(self.x, 300, 2096, 640)
        self.image.draw(self.x+2096, 300, 2096, 640)
        self.font.draw(0,580,f'f키를 눌러 팝콘(투포환)을 던지세요!',(255, 0, 0))

    def update(self):
        if Popcorn.eat == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x <= -2096:
            self.x = 0
class Background:
    image = None
    def __init__(self):
        self.x = 0
        if Background.image == None:
            self.image = load_image('resource/back1.png')
            self.font = load_font('resource/CookieRun Regular.TTF', 32)

    def draw(self):
        self.image.draw(self.x, 300, 2834, 638)
        self.image.draw(self.x+2834, 300, 2834, 638)
        self.font.draw(0,580,f'스페이스 바를 눌러 점프하세요!',(255, 0, 0))

    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.x <= -2834:
            self.x = 0
