from PPlay.gameimage import *
from chao import Chao
from plataforma import Plataforma
from player import Player
from PPlay.sound import Sound

class Fase1:

    def __init__(self, janela, boss):
        self.janela = janela
        self.background = GameImage("Assets/imagens/Skies/arvore-final.png")
        self.background.set_position(0,-620)
        self.floor = Chao("floor.png")
        self.floor.y = self.janela.height - self.floor.height
        self.boss_x_start = -450
        self.boss = boss
        self.plataformas = []
        self.Plataforma_classe = Plataforma
        self.over = False
        self.inicializar_plataformas()


    def draw_elements(self):
        if self.boss.is_finished:
            if self.background.x < 0:
                self.background.x += 50 * self.janela.delta_time()
            if self.background.y < 0:
                self.background.y += 50 * self.janela.delta_time()
            self.over = True
        self.background.draw()
        if not self.over:
            self.floor.draw()

    def try_landing_boss(self):
        if self.boss.hitbox.y + self.boss.hitbox.height > self.floor.y and self.boss.is_falling:
            self.boss.hitbox.y = self.floor.y - self.boss.hitbox.height
            self.boss.vely = 0
            self.boss.is_falling = False

            if self.boss.is_arriving:
                self.boss.is_arriving = False
                self.boss.is_imune = False
                self.boss.is_idle = True
                self.boss.sprite_atual = self.boss.sprites["idle_left"]
                self.boss.cronometro_animacao = 0
                self.boss.sprite_atual.set_total_duration(1.7)

    def inicializar_plataformas(self):
        for i in range(1, int(self.janela.width // (Plataforma.width1x4 * 1.5))):
            y_relativo_a_chao = Player.hitboxes["desmontado"].height
            y_relativo_a_chao *= 4 if i % 2 == 0 else 2
            Plataforma(i * Plataforma.width1x4 * 1.5 + abs(self.boss_x_start), self.floor.y - y_relativo_a_chao, "1x4")
        self.plataformas = Plataforma.lista

    def limpar_plataformas(self):
        self.plataformas.clear()
        Plataforma.lista.clear()
