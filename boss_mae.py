from pygame.draw import rect as drawrect

from PPlay.sprite import Sprite
from PPlay.window import Window


class BossClasseMae:
    janela = Window(1365, 768)
    player = None
    healthbar_sprite = Sprite("Assets/hud/boss-healthbar.png")
    healthbar_sprite.x = janela.width / 2 - healthbar_sprite.width / 2
    healthbar_sprite.y = 675

    def __init__(self, janela, player=None, starting_health=10000, max_health=10000):
        BossClasseMae.janela = janela
        if player:
            self.player = player
        self.health_color = (255, 0, 0)
        self.teclado = janela.get_keyboard()
        self.max_health = max_health
        self.health_atual = starting_health
        self.old_health = self.health_atual
        self.health_ratio = self.health_atual / self.max_health
        self.old_health_ratio = self.health_atual / self.max_health
        self.is_started = False
        self.is_imune = False
        self.is_dying = False
        self.vely = self.velx = 0
        self.aceleracao_x = 0
        self.is_finished = False
        self.is_arriving = False
        self.cronometro_animacao = 0
        self.is_underground = False
        self.m_pressed_past = False
        self.is_mini_game_on = False
        self.is_mini_game_done = False

    def cheat_hit(self):
        if not self.teclado.key_pressed('m') and self.m_pressed_past and not self.is_imune:
            self.levar_dano(self.max_health * 0.05)
        self.m_pressed_past = self.teclado.key_pressed('m')

    def update_frame(self):
        if self.is_started:
            duracao = self.sprite_atual.get_total_duration()
            qtdframes = self.sprite_atual.get_final_frame()
            intervalo = duracao / qtdframes
            # print(f'Duracao: {duracao:.2f}, qtdframes: {qtdframes}, cronometro: {self.cronometro_animacao:.2f}')
            self.cronometro_animacao += self.janela.delta_time()
            self.sprite_atual.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)
            if self.sprite_atual.loop is False and \
                    self.cronometro_animacao // intervalo >= self.sprite_atual.get_final_frame():
                self.sprite_atual.set_curr_frame(self.sprite_atual.get_final_frame() - 1)

    def draw_boss(self):
        # print(self.hitbox.x, self.hitbox.y, self.vely)
        if self.is_started and not self.is_finished:
            self.janela.draw_text(f'{self.health_atual}', self.janela.width * 5 / 10, self.janela.height * 1 / 12, 30,
                                  (255, 255, 80))
            self.calibrar_posicao_sprite()
            self.update_frame()
            self.draw_healthbar()
            if not self.is_underground:
                self.sprite_atual.draw()

        if self.is_dying:
            if self.hitbox.y > 200:
                self.hitbox.y -= 50 * self.janela.delta_time()
            else:
                if self.is_started:
                    self.sprites['explosion'].set_position(self.sprite_atual.x - 80, self.sprite_atual.y - 80)
                    self.sprites['explosion'].update()
                    self.sprites['explosion'].draw()
                    if self.sprites['explosion'].get_curr_frame() == 4:
                        self.is_finished = True
                    elif self.sprites['explosion'].get_final_frame() - 1 \
                            == self.sprites['explosion'].get_curr_frame():
                        self.is_started = False

    def feel_gravity(self):
        if self.is_falling is True:
            self.vely -= self.gravity * self.janela.delta_time()

    def apply_motion(self):
        self.last_position = (self.hitbox.x, self.hitbox.y)
        self.hitbox.y -= self.vely * self.janela.delta_time()
        if abs(self.velx) > 0:
            self.hitbox.x += self.velx * self.direction * self.janela.delta_time()

    def draw_healthbar(self):
        self.mostrar_dano_levado()
        drawrect(self.janela.screen, self.health_color, (self.healthbar_sprite.x + 2, self.healthbar_sprite.y + 8,
                                                   (self.healthbar_sprite.width - 5) * self.health_ratio,
                                                   self.healthbar_sprite.height - 15))
        self.healthbar_sprite.draw()

    @classmethod
    def set_player(cls, player):
        cls.player = player

    def levar_dano(self, qtd_dano):
        self.old_health = self.health_atual
        self.old_health_ratio = self.old_health / self.max_health
        self.health_atual -= qtd_dano
        if self.health_atual < 0:
            self.health_atual = 0
        self.health_ratio = self.health_atual / self.max_health

    def mostrar_dano_levado(self):
        drawrect(self.janela.screen, (255, 255, 255), (self.healthbar_sprite.x + 2, self.healthbar_sprite.y + 8,
                                                       (self.healthbar_sprite.width - 5) * self.old_health_ratio,
                                                       self.healthbar_sprite.height - 15))
        self.old_health -= self.max_health * 0.05 * self.janela.delta_time()
        if self.old_health < 0:
            self.old_health = 0
        self.old_health_ratio = self.old_health / self.max_health
