from PPlay.gameimage import *
from chao import Chao
class Mapa:
    def __init__(self, janela):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/sky.png")
        self.floor = Chao("floor.png", 608)


    def draw_elements(self):
        self.background.draw()
        self.floor.draw()

