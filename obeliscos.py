from PPlay.sprite import Sprite
from caixadesom import draw_healthbar


class Obelisco(Sprite):
    caminho = 'Assets/boss_piano/obelisco.png'
    caminho_hitbox = 'Assets/boss_piano/obelisco_hitbox.png'
    lista = []
    is_imune = False
    is_spawning = False
    is_dying = False

    @classmethod
    def reset_class(cls):
        cls.caminho = 'Assets/boss_piano/obelisco.png'
        cls.caminho_hitbox = 'Assets/boss_piano/obelisco_hitbox.png'
        cls.lista = []
        cls.is_imune = False
        cls.is_spawning = False
        cls.is_dying = False

    def __init__(self, plataforma: Sprite, janela):
        super().__init__(self.caminho, 10)
        self.hitbox = Sprite(self.caminho_hitbox)
        self.janela = janela
        self.sprite_atual = self
        self.x = plataforma.x + plataforma.width / 2 - self.width / 2
        self.y = plataforma.y - self.height
        self.lista.append(self)
        self.set_total_duration(2)
        self.cronometro_animacao = 0
        # variaveis de healthbar:
        self.health = 2300
        self.max_health = 2300
        self.health_ratio = self.health / self.max_health
        self.old_health_ratio = self.health_ratio
        self.old_health = self.health
        self.health_height = 6


    def update_frame(self):
        duracao = self.get_total_duration()
        qtdframes = self.get_final_frame()
        intervalo = duracao / qtdframes
        self.cronometro_animacao += self.janela.delta_time()
        self.set_curr_frame((self.cronometro_animacao // intervalo) % qtdframes)

    @classmethod
    def update(cls):
        for i, obelisco in enumerate(cls.lista):
            obelisco.update_frame()
            obelisco.hitbox.set_position(obelisco.x, obelisco.y)
            if obelisco.health_ratio <= 0:
                cls.lista.pop(i)

    def draw_healthbar(self):
        draw_healthbar(self)

    def levar_dano(self, qtd_dano):
        self.old_health = self.health
        self.old_health_ratio = self.health_ratio
        self.health -= qtd_dano
        if self.health < 0:
            self.health = 0
        self.health_ratio = self.health/self.max_health

    @classmethod
    def draw_obeliscos(cls):
        for obelisco in cls.lista:
            obelisco.draw()
            obelisco.draw_healthbar()
            obelisco.old_health -= 0.05 * obelisco.max_health * obelisco.janela.delta_time()
            obelisco.old_health_ratio = obelisco.old_health / obelisco.max_health

    @classmethod
    def get_hitboxes(cls):
        hitboxes = []
        for obelisco in cls.lista:
            hitboxes.append(obelisco.hitbox)
        return hitboxes