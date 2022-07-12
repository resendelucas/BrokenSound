from os import getcwd

from PPlay.sprite import Sprite
from PPlay.window import Window


class Plataforma(Sprite):
    path_plataformas = f'{getcwd()}\\Assets\\plataformas'
    width1x4 = 128
    lista = []

    def __init__(self, x: float, y: float, tipo_plataforma: str):
        """
        tipo_plataforma: tipos implementados : 1x4
        """
        super().__init__(f'{self.path_plataformas}\\plataforma_{tipo_plataforma}.png')
        self.set_position(x, y)
        self.lista.append(self)

    @classmethod
    def draw_plataformas(cls, janela: Window):
        for plataforma in cls.lista:
            plataforma.draw()

    @classmethod
    def colisao_cima(cls, player):
        player.is_falling = True
        for i, plataforma in enumerate(cls.lista):
            # se a hitbox estava acima da plataforma, mas agora está abaixo, e a hitbox está colidindo
            if player.last_position[1] + \
                    player.hitbox.height <= plataforma.y < player.hitbox.y + player.hitbox.height and\
                    player.hitbox.collided(plataforma):
                player.hitbox.y = plataforma.y - player.hitbox.height
                player.vely = 0
                player.is_falling = False
                player.can_jump = True
                return True
        return False
    
    @classmethod
    def colisao_cima_sprite(cls, sprite):
        sprite.is_falling = True
        for i, plataforma in enumerate(cls.lista):
            # se a hitbox estava acima da plataforma, mas agora está abaixo, e a hitbox está colidindo
            if sprite.last_position[1] + \
                    sprite.height <= plataforma.y < sprite.y + sprite.height and\
                    sprite.collided(plataforma):
                sprite.y = plataforma.y - sprite.height
                sprite.vely = 0
                sprite.is_falling = False
                sprite.can_jump = True
                return True
        return False

    # @classmethod
    # def colisao(cls, player:Player):
    #     for i, plataforma in enumerate(cls.lista):
    #         if player.hitbox.collided(plataforma):
    #             if abs(player.hitbox.y + player.hitbox.height - plataforma.y) <= 1: 
    #                 player.hitbox.y = plataforma.y - player.hitbox.height
    #                 print('if 1')
    #             elif player.hitbox.y + player.hitbox.height >= plataforma.y:
    #                     player.hitbox.x = player.last_position[0]
    #                     print('if 2')
    #             else:
    #                 player.hitbox.set_position(player.last_position[0], player.last_position[1])
    #                 print('if 4')
    #         if player.hitbox.x + player.hitbox.width >= plataforma.x and player.hitbox.x <= plataforma.x + plataforma.width:
    #             if player.hitbox.y <= plataforma.y + plataforma.height and player.hitbox.y + player.hitbox.height >= plataforma.y:
    #                 player.hitbox.y = player.last_position[1]
