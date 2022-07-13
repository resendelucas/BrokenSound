from pygame.draw import rect as drawrect

from PPlay.sprite import Sprite
from PPlay.window import Window


class PlayerHealthBar:
    janela = Window(1365, 768)
    # healthbar_sprite = Sprite("Assets/player_healthbar.png")
    # healthbar_sprite.x = janela.width/2 - healthbar_sprite.width / 2
    # healthbar_sprite.y = janela.height - healthbar_sprite.height - 30
    healthbar_sprite = Sprite("Assets/hud/healthbar.png")
    manabar_sprite = Sprite("Assets/hud/healthbar.png", 5)
    healthbar_sprite.x = 158
    healthbar_sprite.y = 50
    manabar_sprite.x = healthbar_sprite.x
    manabar_sprite.y = healthbar_sprite.y + healthbar_sprite.height * 1.5
    max_mana = 100
    mana_atual = 100
    mana_ratio = mana_atual / max_mana
    old_mana_ratio = mana_ratio

    def __init__(self, max_health, starting_health, janela):
        self.max_health = max_health
        self.health_atual = starting_health
        self.old_health = self.health_atual
        self.janela = janela
        self.health_ratio = self.health_atual / self.max_health
        self.old_health_ratio = self.health_atual / self.max_health

    def draw(self):
        self.mostrar_dano_levado()
        self.mostrar_mana_perdida()
        drawrect(self.janela.screen, (255, 0, 0), (self.healthbar_sprite.x, self.healthbar_sprite.y,
                                                   self.healthbar_sprite.width * self.health_ratio,
                                                   self.healthbar_sprite.height))
        self.healthbar_sprite.draw()
        self.mana_atual += 3 * self.janela.delta_time()
        if self.mana_atual >= self.max_mana:
            self.mana_atual = self.max_mana
        self.draw_mana()
        self.manabar_sprite.draw()

    def levar_dano(self, qtd_dano):
        self.old_health = self.health_atual
        self.old_health_ratio = self.old_health / self.max_health
        self.health_atual -= qtd_dano
        if self.health_atual < 0:
            self.health_atual = 0
        self.health_ratio = self.health_atual / self.max_health

    def mostrar_dano_levado(self):
        drawrect(self.janela.screen, (255, 255, 255), (self.healthbar_sprite.x, self.healthbar_sprite.y,
                                                       self.healthbar_sprite.width * self.old_health_ratio,
                                                       self.healthbar_sprite.height))
        self.old_health -= self.max_health * 0.2 * self.janela.delta_time() / 3
        if self.old_health < 0:
            self.old_health = 0
        self.old_health_ratio = self.old_health / self.max_health

    def draw_mana(self):
        self.mana_ratio = self.mana_atual / self.max_mana
        # print(self.mana_ratio)
        drawrect(self.janela.screen, (15, 15, 255), (self.manabar_sprite.x, self.manabar_sprite.y,
                                                     self.manabar_sprite.width * self.mana_ratio,
                                                     self.manabar_sprite.height))

    def perder_mana(self, qtd_mana):
        self.old_mana_ratio = self.mana_ratio
        self.mana_atual -= qtd_mana
        self.mana_ratio = self.mana_atual / self.max_mana
        # print(self.mana_ratio)
        if self.mana_ratio < 0:
            self.mana_ratio = 0

    def mostrar_mana_perdida(self):
        drawrect(self.janela.screen, (255, 255, 255), (self.manabar_sprite.x, self.manabar_sprite.y,
                                                       self.manabar_sprite.width * self.old_mana_ratio,
                                                       self.manabar_sprite.height))
        self.old_mana_ratio -= self.max_mana * 1 * self.janela.delta_time() / 1.5
