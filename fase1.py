from PPlay.gameimage import *
from chao import Chao


class Fase1:
    def __init__(self, janela, boss):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/background-2.png")
        self.floor = Chao("floor.png", 608)
        self.boss_x_start = -700
        self.boss = boss

    def draw_elements(self):
        self.background.draw()
        self.floor.draw()
