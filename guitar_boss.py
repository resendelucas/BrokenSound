from PPlay.sprite import Sprite
from boss_mae import BossClasseMae
from tiros_teleguiados import TiroTeleguiado


class BossGuitarra(BossClasseMae):
    sprites = {
        # parada
        "idle_right": Sprite('Assets/boss_guitar/still_right.png', 20),
        "idle_left": Sprite('Assets/boss_guitar/still_left.png', 20),
        # invocando microfone
        "swing_summon_right": Sprite("Assets/boss_guitar/summon_left.png", 6),
        "swing_summon_left": Sprite("Assets/boss_guitar/summon_right.png", 6),
        # girando microfone
        "swinging_left": Sprite("Assets/boss_guitar/swinging_left.png", 11),
        "swinging_right": Sprite("Assets/boss_guitar/swinging_right.png", 11),
        # tocando pra cima (ataque meteoro)
        "meteoro_right": Sprite("Assets/boss_guitar/meteoro_right.png", 4),
        "meteoro_left": Sprite("Assets/boss_guitar/meteoro_left.png", 4),
        # tocando agachada
        "playing_right": Sprite("Assets/boss_guitar/playing_right.png", 6),
        "playing_left": Sprite("Assets/boss_guitar/playing_left.png", 6),
        # arriving
        "arriving_left": Sprite("Assets/boss_guitar/falling.png", 2),
        # morte
        "dying_right": Sprite("Assets/boss_guitar/dying_right.png", 2),
        "dying_left": Sprite("Assets/boss_guitar/dying_left.png", 2),
    }
    sprites["arriving_left"].set_total_duration(0.05)
    sprites['playing_left'].set_total_duration(0.4)
    sprites['swing_summon_left'].set_total_duration(2)
    sprites['swing_summon_left'].loop = False
    sprites['swinging_left'].set_total_duration(0.7)
    sprites['swinging_right'].set_total_duration(0.7)
    sprites['meteoro_left'].set_total_duration(0.3)

    hitbox = Sprite("Assets/boss_guitar/hitbox.png")
    # hitbox_microfone = Sprite("Assets/boss_guitar/hitbox_microfone.png")
    hitbox.set_position(-9999, -9999)
    gravity = 4500
    cooldown_tiro = 3

    def __init__(self, janela, player=None):
        super().__init__(10000, 10000)
        self.sprite_atual = self.sprites["arriving_left"]
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.is_imune = True
        self.is_arriving = False
        self.sprite_atual.play()
        self.vely = self.velx = 0
        self.aceleracao_x = 0
        self.direction = -1
        self.is_falling = False
        self.player = player
        self.cronometro_animacao = 0
        self.is_idle = False
        self.is_playing = False
        self.is_summoning = False
        self.is_swinging = False
        self.is_raining = False
        self.is_mini_game_on = False
        self.looking_direction = 'left'
        self.cronometro_still = 0
        self.last_position = (self.hitbox.x, self.hitbox.y)
        self.m_pressed_past = False
        self.is_finished = False
        self.cronometro_tiro = 2

    def spawn(self):
        self.reset()
        self.health_atual = self.max_health
        self.sprite_atual = self.sprites["arriving_left"]
        self.hitbox.x = self.janela.width + self.sprites["arriving_left"].width
        self.hitbox.y = 0 - self.sprites["arriving_left"].height
        self.is_arriving = True
        self.is_falling = True
        self.is_started = True
        self.vely = 0
        self.aceleracao_x = 0
        self.velx = 0
        self.cronometro_animacao = 0
        self.cronometro_still = 0
        self.is_finished = False

    def reset(self):
        super().__init__(10000, 10000)
        self.sprite_atual = self.sprites["arriving_left"]
        self.is_imune = True
        self.is_arriving = False
        self.sprite_atual.play()
        self.vely = self.velx = 0
        self.aceleracao_x = 0
        self.direction = -1
        self.is_falling = False
        self.cronometro_animacao = 0
        self.is_idle = False
        self.is_playing = False
        self.is_summoning = False
        self.is_swinging = False
        self.is_raining = False
        self.is_mini_game_on = False
        self.looking_direction = 'left'
        self.cronometro_still = 0
        self.last_position = (self.hitbox.x, self.hitbox.y)

    def feel_gravity(self):
        if self.is_falling is True:
            self.vely -= self.gravity * self.janela.delta_time()

    def apply_motion(self):
        self.last_position = (self.hitbox.x, self.hitbox.y)
        self.hitbox.y -= self.vely * self.janela.delta_time()
        self.hitbox.x += self.velx * self.direction * self.janela.delta_time()

    def update(self):
        self.check_hit()
        # print(f"{self.vely}")
        if self.is_arriving:
            self.hitbox.x -= 1000 * self.janela.delta_time()
        self.feel_gravity()
        self.apply_motion()

        # Parada
        if self.is_idle:
            self.cronometro_still += self.janela.delta_time()
            if self.cronometro_still >= 2:
                self.is_idle = False
                self.is_playing = True
                self.cronometro_still = 0
                self.cronometro_animacao = 0
                self.sprite_atual = self.sprites['playing_left']

        # Começa a tocar 
        elif self.is_playing:
            self.cronometro_tiro += self.janela.delta_time()
            if self.cronometro_tiro > self.cooldown_tiro:
                TiroTeleguiado(self.sprite_atual, self.player)
                print('a')
                self.cronometro_tiro = 0
            TiroTeleguiado.update_tiros()
            if self.health_atual < 0.8 * self.max_health:
                self.is_imune = True
                self.is_summoning = True
                self.is_playing = False
                self.cronometro_animacao = 0
                self.sprite_atual = self.sprites['swing_summon_left']


        # Invoca o microfone
        elif self.is_summoning:
            self.sprite_atual.loop = False
            if self.sprite_atual.get_final_frame() - 1 == self.sprites['swing_summon_left'].get_curr_frame():
                self.is_swinging = True
                self.is_summoning = False
                self.is_imune = False
                self.cronometro_animacao = 0
                self.sprite_atual = self.sprites["swinging_right"]
                self.direction *= -1

        # Gira o microfone andando para esquerda ou direita
        elif self.is_swinging:
            if self.velx < 600:
                self.velx += 50 * self.janela.delta_time()
            else:
                self.velx = 600
            if self.hitbox.x + self.hitbox.width >= self.janela.width:
                self.sprite_atual = self.sprites['swinging_left']
                self.direction *= -1
                self.hitbox.set_position(self.last_position[0], self.last_position[1])
            elif self.hitbox.x <= 0:
                self.sprite_atual = self.sprites['swinging_right']
                self.direction *= -1
                self.hitbox.set_position(self.last_position[0], self.last_position[1])
            if self.health_atual <= 0:
                self.is_swinging = False
                self.is_mini_game_on = True
                self.cronometro_animacao = 0
                self.sprite_atual = self.sprites['meteoro_left']
                self.velx = 0

    def update_frame(self):
        if self.is_started:
            duracao = self.sprite_atual.get_total_duration()
            qtdframes = self.sprite_atual.get_final_frame()
            intervalo = duracao / qtdframes
            # print(f'Duracao: {duracao:.2f}, qtdframes: {qtdframes}, cronometro: {self.cronometro_animacao:.2f}')
            self.cronometro_animacao += self.janela.delta_time()
            self.sprite_atual.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)
            if self.sprite_atual == self.sprites["meteoro_left"]:
                print(f'sprite: meteoro_left, duracao: {duracao:.2f}, qtdframes: {qtdframes}')
            if self.sprite_atual.loop is False and \
                    self.cronometro_animacao // intervalo >= self.sprite_atual.get_final_frame():
                self.sprite_atual.set_curr_frame(self.sprite_atual.get_final_frame() - 1)
                print('b')

    def calibrar_posicao_sprite(self):
        if not self.is_swinging:
            diferenca_hitbox_y = abs(self.hitbox.height - self.sprite_atual.height)
            diferenca_hitbox_x = abs(self.hitbox.width - self.sprite_atual.width)
            self.sprite_atual.x = self.hitbox.x - diferenca_hitbox_x / 2
            self.sprite_atual.y = self.hitbox.y - diferenca_hitbox_y
        else:
            if self.sprite_atual is self.sprites["swinging_right"]:
                self.sprite_atual.x = self.hitbox.x - 64
            else:
                self.sprite_atual.x = self.hitbox.x - 180
            self.sprite_atual.y = self.hitbox.y - 120

    def draw_boss(self):
        # print(self.hitbox.x, self.hitbox.y, self.vely)
        if self.is_started and not self.is_finished:
            self.janela.draw_text(f'{self.health_atual}', self.janela.width * 5 / 10, self.janela.height * 1 / 12, 30,
                                  (255, 255, 80))
            self.calibrar_posicao_sprite()
            self.update_frame()
            self.sprite_atual.draw()
            self.draw_healthbar()

    def check_hit(self):
        if not self.teclado.key_pressed('m') and self.m_pressed_past and not self.is_imune:
            self.levar_dano(self.max_health * 0.05)
        self.m_pressed_past = self.teclado.key_pressed('m')
