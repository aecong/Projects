from pico2d import *


class Clicksound:
    bgm = None
    def __init__(self):
        if not Clicksound.bgm:
            Clicksound.bgm = load_wav('resource/bgm_jump.wav')
            Clicksound.bgm.set_volume(32)

    def draw(self):
        pass

    def update(self):
        pass
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
