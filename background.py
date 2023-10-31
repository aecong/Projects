from pico2d import load_image


class Background:
    def __init__(self):
        self.x = 700
        self.image = load_image('resource/back1.png')

    def draw(self):
        self.image.draw(self.x, 300, 2125.5, 478.5)

    def update(self):
        self.x -= 1
