from random import randint

from PPlay.sprite import Sprite
from gaiola import Gaiola


class MiniGameTeclas:
    player = None
    caminho = 'Assets/boss_piano/gaiola/tecla_'
    gravity = 50
    teclas = []
    cronometro_cair_value = 2

    @classmethod
    def reset_class(cls):
        cls.player = None
        cls.caminho = 'Assets/boss_piano/gaiola/tecla_'
        cls.gravity = 50
        cls.teclas = []
        cls.cronometro_cair_value = 2

    def __init__(self, gaiola: Gaiola):
        self.gaiola = gaiola
        self.player = self.gaiola.player
        self.janela = self.gaiola.janela
        self.teclas_restantes = []
        self.cronometro_cair = 0
        self.is_second_row_on = False
        self.is_draw_elements_on = False
        self.teclas.append(Sprite(f'{self.caminho}left.png'))
        for i in range(3):
            self.teclas.append(Sprite(f'{self.caminho}middle.png'))
        self.teclas.append(Sprite(f'{self.caminho}right.png'))
        for i, tecla in enumerate(self.teclas):
            tecla.y = 100
            tecla.vely = 0
            tecla.is_falling = False
            self.teclas_restantes.append(tecla)

    def respawn(self):
        for i, tecla in enumerate(self.teclas):
            tecla.y = 100
            tecla.vely = 0
            tecla.is_falling = False

            self.teclas_restantes.append(tecla)
            self.cronometro_cair = 0

    def draw_elements(self):
        for tecla in self.teclas:
            tecla.draw()
        self.gaiola.draw()

    def apply_gravity(self, tecla):
        if tecla.is_falling:
            tecla.vely -= self.gravity * self.janela.delta_time()
            tecla.y -= tecla.vely * self.janela.delta_time()

    def sortear_teclas_caindo(self):
        if self.is_second_row_on:
            for tecla in self.teclas:
                tecla.is_falling = True
            return
        while len(self.teclas_restantes) != 2:
            i = randint(0, len(self.teclas_restantes) - 1)

            self.teclas_restantes[i].is_falling = True
            self.teclas_restantes[i].vely = 0
            self.teclas_restantes.pop(i)

    def colisao_player_teclas(self):
        for tecla in self.teclas:
            if tecla.collided(self.player.hitbox) and not self.player.is_imune:
                self.player.levar_dano(1)

    def update_teclas(self):
        self.cronometro_cair += self.janela.delta_time()
        teclas_finished = 0
        teclas_almost_finished = 0
        if self.cronometro_cair >= self.cronometro_cair_value and len(self.teclas) == 5:
            self.sortear_teclas_caindo()

        for i, tecla in enumerate(self.teclas):
            if tecla.is_falling:
                self.apply_gravity(tecla)
                if tecla.y >= self.janela.height - tecla.height * 2.3:
                    teclas_almost_finished += 1
                if tecla.y >= 676:
                    teclas_finished += 1
                    self.cronometro_cair = -2
            if teclas_almost_finished == 3:
                for tecla in self.teclas:
                    tecla.is_falling = True
            elif teclas_finished == 5:
                for tecla in self.teclas:
                    tecla.y = 100
                    tecla.vely = 0
                    tecla.is_falling = False
                    self.teclas_restantes.clear()
                    for i, tecla in enumerate(self.teclas):
                        tecla.y = 100
                        tecla.vely = 0
                        tecla.is_falling = False
                        self.teclas_restantes.append(tecla)
                    self.sortear_teclas_caindo()
                    break

    def posicionar_teclas_x(self):
        for i, tecla in enumerate(self.teclas):
            tecla.x = self.gaiola.x + 5 + (tecla.width + 24) * i

    def update(self):
        self.gaiola.update()
        self.update_teclas()
        if self.gaiola.y < 676 - self.gaiola.height:
            self.posicionar_teclas_x()
