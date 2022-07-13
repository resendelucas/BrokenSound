from random import randint

from PPlay.sprite import *
from PPlay.window import *


class Skeleton:
    janela = Window(1365, 768)
    player = None
    lista_inimigos = []
    walkspeed = 75
    jumpspeed = 1200
    gravity = 4500
    is_imune = False

    def __init__(self):
        self.lista_inimigos.append(self)
        self.sprites = {
            "idle_right": Sprite('Assets/boss_piano/skeletons/idle_left.png', 4),
            "idle_left": Sprite('Assets/boss_piano/skeletons/idle_right.png', 4),
            # aparecendo
            "spawning_right": Sprite("Assets/boss_piano/skeletons/spawning_right.png", 8),
            "spawning_left": Sprite("Assets/boss_piano/skeletons/spawning_left.png", 8),
            # andando
            "walking_left": Sprite("Assets/boss_piano/skeletons/walking_left.png", 8),
            "walking_right": Sprite("Assets/boss_piano/skeletons/walking_right.png", 8),
            # atacando
            "attacking_right": Sprite("Assets/boss_piano/skeletons/attacking_right.png", 8),
            "attacking_left": Sprite("Assets/boss_piano/skeletons/attacking_left.png", 8),
            # morrendo
            "dying_right": Sprite("Assets/boss_piano/skeletons/dying_right.png", 14),
            "dying_left": Sprite("Assets/boss_piano/skeletons/dying_left.png", 14),
        }
        self.hitbox = Sprite("Assets/boss_piano/skeletons/hitbox.png")
        self.sprite_atual = self.sprites["spawning_right"]
        self.hitbox.x = randint(0, self.janela.width)
        self.hitbox.y = 676 - self.sprite_atual.height
        self.sprites['idle_right'].set_total_duration(4/3)
        self.sprites['spawning_right'].set_total_duration(2)
        self.sprites['walking_right'].set_total_duration(1.6)
        self.sprites['walking_left'].set_total_duration(1.6)
        self.sprites['dying_right'].set_total_duration(1.75)
        self.sprites['dying_right'].loop = False
        self.is_spawning = True
        self.is_walking = False
        self.vely = self.velx = 0
        self.can_jump = True
        self.cronometro_animacao = 0
        self.cronometro_pulo = 0
        self.last_position = (0, 0)
        self.is_morto = self.is_dying = False

    @classmethod
    def set_player_e_janela(cls, player, janela):
        cls.player = player
        cls.janela = janela

    def update_sprite(self):
        self.sprite_atual.set_position(self.hitbox.x, self.hitbox.y)
        if self.is_spawning:
            self.sprite_atual.loop = False
            if self.sprite_atual.get_final_frame() - 1 == self.sprites['spawning_right'].get_curr_frame():
                self.is_spawning = False
                self.is_walking = True
                self.cronometro_animacao = 0

    def update_frame(self):
        duracao = self.sprite_atual.get_total_duration()
        qtdframes = self.sprite_atual.get_final_frame()
        intervalo = duracao / qtdframes

        self.cronometro_animacao += self.janela.delta_time()
        self.sprite_atual.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)
        if self.sprite_atual.loop is False and \
                self.cronometro_animacao // intervalo >= self.sprite_atual.get_final_frame():
            self.sprite_atual.set_curr_frame(self.sprite_atual.get_final_frame() - 1)
            if self.is_dying:
                self.is_morto = True

    def seguir_player(self):
        self.cronometro_pulo += self.janela.delta_time()
        if self.is_walking and not self.is_dying:
            deslocamento_x = (self.player.hitbox.x + self.player.hitbox.width / 2) - \
                             (self.hitbox.x + self.hitbox.width / 2)
            deslocamento_y = (self.player.hitbox.y + self.player.hitbox.height / 2) - \
                             (self.hitbox.y + self.hitbox.height / 2)
            direcao_x = 1 if deslocamento_x >= 0 else -1
            self.hitbox.x += self.walkspeed * direcao_x * self.janela.delta_time()
            if deslocamento_y < 0 and self.can_jump and int(self.cronometro_pulo) % 3 == 0:
                self.jump()
            if deslocamento_x < -0.5:
                self.sprite_atual = self.sprites['walking_left']
            elif deslocamento_x > 0.5:
                self.sprite_atual = self.sprites['walking_right']
            else:
                self.sprite_atual = self.sprites['idle_right']

    def jump(self):
        self.vely = self.jumpspeed
        self.can_jump = False
        self.is_falling = True

    def apply_motion(self):
        self.last_position = (self.hitbox.x, self.hitbox.y)
        self.hitbox.y -= self.vely * self.janela.delta_time()
        self.hitbox.x += self.velx * self.janela.delta_time()

    def feel_gravity(self):
        self.vely -= self.gravity * self.janela.delta_time()

    @classmethod
    def update_esqueletos(cls):
        for i, esqueleto in enumerate(cls.lista_inimigos):
            if esqueleto.is_morto:
                cls.lista_inimigos.pop(i)
                continue
            esqueleto.seguir_player()
            esqueleto.feel_gravity()
            esqueleto.apply_motion()

    @classmethod
    def try_landing_esqueletos(cls, chao, plataformas):
        for esqueleto in cls.lista_inimigos:
            esqueleto.is_falling = True
            if esqueleto.hitbox.y + esqueleto.hitbox.height >= chao.y:
                esqueleto.hitbox.y = chao.y - esqueleto.hitbox.height
                esqueleto.vely = 0
                esqueleto.is_falling = False
                esqueleto.is_underground = False
                esqueleto.can_jump = True
                continue
            for plataforma in plataformas:
                plataforma.colisao_cima(esqueleto)

    @classmethod
    def draw_esqueletos(cls):
        for esqueleto in cls.lista_inimigos:
            esqueleto.update_sprite()
            esqueleto.update_frame()
            esqueleto.sprite_atual.draw()

    @classmethod
    def get_hitboxes(cls):
        lista_hitboxes = []
        for esqueleto in cls.lista_inimigos:
            lista_hitboxes.append(esqueleto.hitbox)
        return lista_hitboxes

    def levar_dano(self, _):
        if not self.is_dying:
            self.sprite_atual = self.sprites['dying_right']
            self.cronometro_animacao = 0
            self.is_dying = True
