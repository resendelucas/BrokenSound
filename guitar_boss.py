from PPlay.sprite import Sprite
from PPlay.window import Window


class BossGuitarra:
    janela = Window(1200, 700)
    sprites = {
        # parada
        "idle_right": Sprite('Assets/boss_guitar/still_right.png', 20),
        "idle_left": Sprite('Assets/boss_guitar/still_left.png', 20),
        # invocando microfone
        "swing_summon_right": Sprite("Assets/boss_guitar/summon_left.png", 6),
        "swing_summon_left": Sprite("Assets/boss_guitar/summon_right.png", 6),
        # girando microfone
        "swinging_right": Sprite("Assets/boss_guitar/swinging_left.png", 10),
        "swinging_left": Sprite("Assets/boss_guitar/swinging_right.png", 10),
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
    hitbox = Sprite("Assets/boss_guitar/hitbox.png")
    hitbox.set_position(-9999, -9999)
    gravity = 4500

    def __init__(self, janela):
        self.sprite_atual = self.sprites["arriving_left"]
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.is_imune = True
        self.is_started = False
        self.is_arriving = False
        self.sprite_atual.play()
        self.vely = self.velx = 0
        self.direction = -1
        self.is_falling = False
        self.cronometro_animacao = 0
        self.max_health = 100
        self.health = 100
        self.idle = False
        self.playing = False
        self.summoning = False
        self.swinging = False
        self.raining = False
        self.mini_game = False
        self.looking_direction = 'left'

    def start_arrive(self):
        self.sprite_atual = self.sprites["arriving_left"]
        self.hitbox.x = self.janela.width + self.sprites["arriving_left"].width
        self.hitbox.y = 0 - self.sprites["arriving_left"].height
        self.is_arriving = True
        self.is_falling = True
        self.is_started = True
        self.vely = 0
        self.cronometro_animacao = 0
        self.cronometro_still = 0
        self.sprites["arriving_left"].set_total_duration(0.1)

    def feel_gravity(self):
        if self.is_falling is True:
            self.vely -= self.gravity * self.janela.delta_time()

    def apply_motion(self):
        self.hitbox.y -= self.vely * self.janela.delta_time()
        self.hitbox.x += self.velx * self.janela.delta_time()

    def update(self):
        self.check_hit()
        # print(f"{self.vely}")
        if self.is_arriving:
            self.hitbox.x -= 1000 * self.janela.delta_time()
        self.feel_gravity()
        self.apply_motion()

        # Parada
        if self.idle:
            self.cronometro_still += self.janela.delta_time()
            if self.cronometro_still >= 4:
                self.idle = False
                self.playing = True
                self.cronometro_still = 0

        # Começa a tocar 
        if self.playing:
            self.sprite_atual = self.sprites['playing_left']
            self.sprites['playing_left'].set_total_duration(0.4)
            if self.health < 0.8 * self.max_health:
                self.is_imune = True
                self.summoning = True
                self.playing = False

        # Invoca o microfone
        if self.summoning:
            self.sprite_atual = self.sprites['swing_summon_left']
            self.sprites['swing_summon_left'].set_total_duration(1)
            if self.sprite_atual.get_final_frame() - 1 == self.sprites['swing_summon_left'].get_curr_frame():
                self.swinging = True
                self.summoning = False
                self.is_imune = False

        # Gira o microfone andando para esquerda ou direita
        if self.swinging:
            self.hitbox.x += 400 * self.direction * self.janela.delta_time()
            if self.hitbox.x + self.hitbox.width >= self.janela.width:
                self.sprite_atual = self.sprites['swinging_left']
                self.sprites['swinging_left'].set_total_duration(0.3)
                self.direction *= -1
            if self.hitbox.x <= 0:
                self.sprite_atual = self.sprites['swinging_right']
                self.sprites['swinging_right'].set_total_duration(0.3)
                self.direction *= -1
            if self.health <= self.max_health * 0.5:
                self.swinging = False
                self.mini_game = True

        # minigame
        if self.mini_game:
            self.sprite_atual = self.sprites['meteoro_left']
            self.sprites['meteoro_left'].set_total_duration(0.3)
            

    def update_frame(self):
        if self.is_started:
            duracao = self.sprite_atual.get_total_duration()
            qtdframes = self.sprite_atual.get_final_frame()
            intervalo = duracao / qtdframes
            print(f'Duracao: {duracao:.2f}, qtdframes: {qtdframes}, cronometro: {self.cronometro_animacao:.2f}')
            self.cronometro_animacao += self.janela.delta_time()
            self.sprite_atual.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)

    def draw_boss(self):
        # print(self.hitbox.x, self.hitbox.y, self.vely)
        if self.is_started:
            self.janela.draw_text(f'{self.health}', self.janela.width * 5 / 10, self.janela.height * 1 / 12, 30, (255, 255, 80))
            diferenca_hitbox_y = abs(self.hitbox.height - self.sprite_atual.height)
            diferenca_hitbox_x = abs(self.hitbox.width - self.sprite_atual.width)
            self.sprite_atual.x = self.hitbox.x - diferenca_hitbox_x/2
            self.sprite_atual.y = self.hitbox.y - diferenca_hitbox_y
            self.update_frame()
            self.sprite_atual.draw()

    def check_hit(self):
        if self.teclado.key_pressed('m') and not self.is_imune:
            self.health -= 0.25