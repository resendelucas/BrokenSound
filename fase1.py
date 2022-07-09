from PPlay.gameimage import *
from chao import Chao


class Fase1:
    def __init__(self, janela, boss):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/background-2.png")
        self.floor = Chao("floor.png")
        self.floor.y = self.janela.height - self.floor.height
        self.boss_x_start = -700
        self.boss = boss
        ''' plataformas é uma lista de tuplas contendo x, y e tipo da plataforma.'''
        self.inicializar_plataformas()

    def draw_elements(self):
        self.background.draw()
        self.floor.draw()

    def inicializar_plataformas(self):
        from plataforma import Plataforma
        from player import Player
        for i in range(1, int(self.janela.width // (Plataforma.width1x4 * 1.5))):
            y_relativo_a_chao = Player.hitboxes["desmontado"].height
            y_relativo_a_chao *= 4 if i % 2 == 0 else 2
            Plataforma(i * Plataforma.width1x4 * 1.5 + abs(self.boss_x_start), self.floor.y - y_relativo_a_chao, "1x4")
