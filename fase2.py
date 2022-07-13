from PPlay.gameimage import *
from chao import Chao
from plataforma import Plataforma
from player import Player


class Fase2:
    def __init__(self, janela, boss):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/background-1.png")
        self.floor = Chao("floor.png")
        self.floor.y = self.janela.height - self.floor.height
        self.boss_x_start = -700
        self.boss = boss
        self.plataformas = []
        self.Plataforma_classe = Plataforma
        self.inicializar_plataformas()

    def draw_elements(self):
        self.background.draw()
        if self.boss.is_arriving:
            self.boss.sprite_atual.draw()
        self.floor.draw()

    def inicializar_plataformas(self):
        for i in range(1, int(self.janela.width // (Plataforma.width1x4 * 1.5))):
            y_relativo_a_chao = Player.hitboxes["desmontado"].height
            y_relativo_a_chao *= 4 if i % 2 == 0 else 2
            Plataforma(i * Plataforma.width1x4 * 1.5 + abs(self.boss_x_start), self.floor.y - y_relativo_a_chao, "1x4")
        self.plataformas = Plataforma.lista
        
    def try_landing_boss(self):
        if self.boss.hitbox.y + self.boss.sprite_atual.height <= self.floor.y:
            self.boss.hitbox.y = self.floor.y - self.boss.sprite_atual.height
            print(self.boss.hitbox.y)
            self.boss.vely = 0
            self.boss.is_falling = False
            self.boss.is_underground = False