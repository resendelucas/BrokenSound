from PPlay.window import Window
from PPlay.sprite import Sprite
from pygame.draw import rect as drawrect
class PlayerHealthBar:
    janela = Window(1365, 768)
    healthbar_sprite = Sprite("Assets/player_healthbar.png")
    healthbar_sprite.x = janela.width/2 - healthbar_sprite.width / 2
    healthbar_sprite.y = janela.height - healthbar_sprite.height - 30

    def __init__(self, max_health, starting_health, janela):
        self.max_health = max_health
        self.health_atual = starting_health
        self.old_health = self.health_atual
        self.janela = janela
        self.health_ratio = self.health_atual / self.max_health
        self.old_health_ratio = self.health_atual / self.max_health

    def draw(self):
        self.mostrar_dano_levado()
        drawrect(self.janela.screen, (255, 0, 0), (self.healthbar_sprite.x, self.healthbar_sprite.y,
                                                       self.healthbar_sprite.width * self.health_ratio,
                                                       self.healthbar_sprite.height))
        self.healthbar_sprite.draw()

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
        self.old_health -= self.max_health * 0.2 * self.janela.delta_time()/3
        if self.old_health < 0:
            self.old_health = 0
        self.old_health_ratio = self.old_health/self.max_health