from PPlay.sprite import Sprite
from PPlay.window import Window
from os import getcwd

class Plataforma(Sprite):
    path_plataformas = f'{getcwd()}\\Assets\\plataformas'
    lista = []
    def __init__(self, x:float, y:float, tipo_plataforma:str):
        """
        tipo_plataforma: tipos implementados : 1x4
        """
        super().__init__(f'{self.path_plataformas}\\plataforma_{tipo_plataforma}.png')
        self.set_position(x, y)
        self.lista.append(self)
        
    @classmethod
    def draw_plataformas(cls, janela:Window):
        for plataforma in cls.lista:
            plataforma.draw()
    @staticmethod
    def colisao_ponto_sprite(ponto:tuple, sprite:Sprite):
        x, y = ponto[0], ponto[1]
        if sprite.x < x < sprite.x + sprite.width and\
            sprite.y < y < sprite.y + sprite.height:
                return True
        return False


    @classmethod
    def colisao_horizontal(cls, player):
        for i, plataforma in enumerate(cls.lista):
            if player.hitbox.collided(plataforma):
                if player.hitbox.y + player.hitbox.height > plataforma.y + 4 and player.hitbox.y < plataforma.y + plataforma.height - 10:
                    player.can_move = False
                    if player.last_direction == 'right':
                        player.hitbox.x = plataforma.x - player.hitbox.width
                    elif player.last_direction == 'left':
                        player.hitbox.x = plataforma.x + plataforma.width
            else:
                player.can_move = True
    @classmethod
    def colisao_vertical(cls, player):
        for i, plataforma in enumerate(cls.lista):
            if player.hitbox.collided(plataforma):
                # Colisão com a parte de baixo da plataforma
                if player.vely > 0 and abs(player.hitbox.y - plataforma.y + plataforma.height) >= 10:
                    if player.hitbox.x < plataforma.x + plataforma.width - 3\
                        and player.hitbox.x + player.hitbox.width > plataforma.x + 3:
                        player.hitbox.y = plataforma.y + plataforma.height
                        player.vely = 0
                        player.can_jump = False
                        player.is_falling = True
                
                # Colisão com a parte de cima da plataforma
                elif player.vely < 0 and abs(player.hitbox.y + player.hitbox.height - plataforma.y) <= 10:
                    player.hitbox.y = plataforma.y - player.hitbox.height
                    player.vely = 0
                    player.can_jump = True
                    player.is_falling = False
            else:
                player.is_falling = True

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
                
