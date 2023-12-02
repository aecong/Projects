from pico2d import *

import game_framework


class Backgroundsound:
    def __init__(self):
        self.bgm = load_music('resource/background_sound.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        pass
    def update(self):
        pass

class Titlesound:
    def __init__(self):
        self.bgm = load_music('resource/bgm_lobby.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        pass
    def update(self):
        pass
