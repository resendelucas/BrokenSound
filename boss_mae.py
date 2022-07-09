from pygame.draw import rect as drawrect

from PPlay.sprite import Sprite
from PPlay.window import Window


class BossClasseMae:
    janela = Window(1365, 768)
    healthbar_sprite = Sprite("Assets/boss_healthbar.png")
    healthbar_sprite.x = janela.width/2 - healthbar_sprite.width / 2
    healthbar_sprite.y = 75

    def __init__(self, max_health, starting_health):
        self.max_health = max_health
        self.health_atual = starting_health
        self.old_health = self.health_atual
        self.health_ratio = self.health_atual / self.max_health
        self.old_health_ratio = self.health_atual / self.max_health
        self.is_started = False
        self.is_imune = False

    def draw_healthbar(self):
        self.mostrar_dano_levado()
        drawrect(self.janela.screen, (255, 0, 0), (self.healthbar_sprite.x + 5, self.healthbar_sprite.y + 6,
                                                   (self.healthbar_sprite.width - 5) * self.health_ratio, 124))
        self.healthbar_sprite.draw()

    def levar_dano(self, qtd_dano):
        self.old_health = self.health_atual
        self.old_health_ratio = self.old_health / self.max_health
        self.health_atual -= qtd_dano
        if self.health_atual < 0:
            self.health_atual = 0
        self.health_ratio = self.health_atual / self.max_health

    def mostrar_dano_levado(self):
        drawrect(self.janela.screen, (255, 255, 255), (self.healthbar_sprite.x + 5, self.healthbar_sprite.y + 6,
                                                       (self.healthbar_sprite.width - 5) * self.old_health_ratio, 124))
        self.old_health -= self.max_health * 0.05 * self.janela.delta_time()
        if self.old_health < 0:
            self.old_health = 0
        self.old_health_ratio = self.old_health / self.max_health
