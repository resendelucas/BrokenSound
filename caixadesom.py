from pygame.draw import rect as drawrect

from PPlay.sprite import Sprite
from PPlay.window import Window


def draw_healthbar(self):
    drawrect(self.janela.screen, (0, 0, 0), (self.x - self.width / 2 - 2, self.y - 6 - self.health_height + 2,
                                             self.width * 2 + 4, self.health_height - 4))
    drawrect(self.janela.screen, (255, 255, 255), (self.x - self.width / 2, self.y - 6 - self.health_height,
                                                   self.width * 2 * self.old_health_ratio, self.health_height))
    drawrect(self.janela.screen, (255, 0, 0), (self.x - self.width / 2, self.y - 6 - self.health_height,
                                               self.width * 2 * self.health_ratio, self.health_height))


class CaixaDeSom(Sprite):
    Window(1365, 768)
    caminho_sprites = dict()
    caminho_sprites["right"] = 'Assets/caixadesom/sprite_right.png'
    caminho_sprites["left"] = 'Assets/caixadesom/sprite_left.png'

    @classmethod
    def reset_class(cls):
        Window(1365, 768)
        cls.caminho_sprites = dict()
        cls.caminho_sprites["right"] = 'Assets/caixadesom/sprite_right.png'
        cls.caminho_sprites["left"] = 'Assets/caixadesom/sprite_left.png'

    def __init__(self, direction: str, player_hitbox: Sprite, janela: Window, lifetime: int = 6, max_lifetime: int = 6):
        super().__init__(self.caminho_sprites[direction], 3)
        self.set_position(player_hitbox.x, player_hitbox.y)
        self.direction = direction
        self.lifetime = lifetime
        self.max_lifetime = max_lifetime
        self.janela = janela
        self.health_ratio = lifetime / max_lifetime
        self.old_health_ratio = lifetime / max_lifetime
        self.health_height = 6
        self.vely = 0
        self.is_falling = False
        self.last_position = (self.x, self.y)
        self.cronometro = 0

    def feel_gravity(self, gravidade):
        self.vely -= gravidade * self.janela.delta_time()

    def apply_motion(self):
        if self.is_falling:
            self.last_position = (self.x, self.y)
            self.y -= self.vely * self.janela.delta_time()

    def tick_time(self):
        self.old_health_ratio = self.lifetime / self.max_lifetime
        self.lifetime -= self.janela.delta_time()
        if self.lifetime < 0:
            self.lifetime = 0
        self.health_ratio = self.lifetime / self.max_lifetime
        self.cronometro += self.janela.delta_time()

    def draw_healthbar(self):
        draw_healthbar(self)

    def draw_sprite_and_healthbar(self):
        self.draw()
        self.draw_healthbar()
