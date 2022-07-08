from PPlay.sprite import Sprite
from PPlay.window import Window


class BossGuitarra:
    janela = Window(1200, 700)
    sprites = {
        # parada
        "idle_right": Sprite('Assets/boss_guitar/still_right.png', 20),
        "idle_left": Sprite('Assets/boss_guitar/still_left.png', 20),
        # invocando microfone
        "swing_summon_right": Sprite("Assets/boss_guitar/summon_right.png", 6),
        "swing_summon_left": Sprite("Assets/boss_guitar/summon_right.png", 6),
        # girando microfone
        "swinging_right": Sprite("Assets/boss_guitar/swinging_right.png", 10),
        "swinging_left": Sprite("Assets/boss_guitar/swinging_left.png", 10),
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
        self.is_imune = True
        self.is_started = False
        self.is_arriving = False
        self.sprite_atual.play()
        self.vely = self.velx = 0
        self.is_falling = False
        self.cronometro_animacao = 0

    def start_arrive(self):
        self.sprite_atual = self.sprites["arriving_left"]
        self.hitbox.x = self.janela.width + self.sprites["arriving_left"].width
        self.hitbox.y = 0 - self.sprites["arriving_left"].height
        self.is_arriving = True
        self.is_falling = True
        self.is_started = True
        self.vely = 0
        self.cronometro_animacao = 0
        self.sprites["arriving_left"].set_total_duration(100)

    def feel_gravity(self):
        if self.is_falling is True:
            self.vely -= self.gravity * self.janela.delta_time()

    def apply_motion(self):
        self.hitbox.y -= self.vely * self.janela.delta_time()
        self.hitbox.x += self.velx * self.janela.delta_time()

    def update(self):
        # print(f"{self.vely}")
        if self.is_arriving:
            self.hitbox.x -= 1000 * self.janela.delta_time()
        self.feel_gravity()
        self.apply_motion()

    def update_frame(self):
        if self.is_started:
            duracao = self.sprite_atual.get_total_duration()
            qtdframes = self.sprite_atual.get_final_frame()
            intervalo = duracao / qtdframes
            # print(f'Duracao: {duracao:.2f}, qtdframes: {qtdframes}, cronometro: {self.cronometro_animacao:.2f}')
            self.cronometro_animacao += self.janela.delta_time()
            self.sprite_atual.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)

    def draw_boss(self):
        # print(self.hitbox.x, self.hitbox.y, self.vely)
        if self.is_started:
            diferenca_hitbox_y = abs(self.hitbox.height - self.sprite_atual.height)
            diferenca_hitbox_x = abs(self.hitbox.width - self.sprite_atual.width)
            self.sprite_atual.x = self.hitbox.x - diferenca_hitbox_x/2
            self.sprite_atual.y = self.hitbox.y - diferenca_hitbox_y
            self.update_frame()
            self.sprite_atual.draw()
