from PPlayTeste.gameimage import *

class Mapa():
    def __init__(self, janela):
        self.janela = janela
        self.get_elements()
        self.background = None
        self.floor = None

    def get_elements(self):
        self.background = GameImage("Assets/imagens/sky.png")
        self.floor = GameImage("Assets/imagens/floor.png")
        self.floor.set_position(0,608)

    def draw_elements(self):
        self.background.draw()
        self.floor.draw()
