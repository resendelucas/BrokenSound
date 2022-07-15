from PPlay.gameimage import *
from chao import Chao
from obeliscos import Obelisco
from plataforma import Plataforma
from player import Player
from skeletons import Skeleton


class Fase2:
    def __init__(self, janela, boss):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/igreja-fundo.png")
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
        Obelisco.draw_obeliscos()
        self.floor.draw()

    def inicializar_plataformas(self):
        self.boss.plataformas_obeliscos = []
        for i in range(1, int(self.janela.width // (Plataforma.width1x4 * 1.5))):
            y_relativo_a_chao = Player.hitboxes["desmontado"].height
            y_relativo_a_chao *= 4 if i % 2 == 0 else 2
            plataforma = Plataforma(i * Plataforma.width1x4 * 1.5 + abs(self.boss_x_start),
                                    self.floor.y - y_relativo_a_chao, "1x4")
            if i in (2, 4):
                self.boss.plataformas_obeliscos.append(plataforma)
        self.plataformas = Plataforma.lista

    def try_landing_boss(self):
        if not self.boss.is_dying and not self.boss.is_finished:
            compensacao = 0 if self.boss.sprite_atual is self.boss.sprites['summoner_playing'] else 0
            if self.boss.hitbox.y + self.boss.sprite_atual.height <= self.floor.y:
                self.boss.hitbox.y = self.floor.y - self.boss.sprite_atual.height - compensacao
                self.boss.vely = 0
                self.boss.is_falling = False
                self.boss.is_underground = False

        Skeleton.try_landing_esqueletos(self.floor, self.plataformas)

    def limpar_plataformas(self):
        self.plataformas.clear()
        Plataforma.lista.clear()
