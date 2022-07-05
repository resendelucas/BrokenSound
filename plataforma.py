from operator import truediv
from PPlay.sprite import Sprite
from PPlay.window import Window
from player import Player
from os import getcwd
from pygame.rect import Rect
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
    def colisao(cls, player:Player):
        for i, plataforma in enumerate(cls.lista):
            if player.hitbox.collided(plataforma):
                if abs(player.hitbox.y + player.hitbox.height - plataforma.y) <= 1: 
                    player.hitbox.y = plataforma.y - player.hitbox.height
                    print('if 1')
                elif player.hitbox.y + player.hitbox.height >= plataforma.y:
                        player.hitbox.x = player.last_position[0]
                        print('if 2')
                else:
                    player.hitbox.set_position(player.last_position[0], player.last_position[1])
                    print('if 4')
            if player.hitbox.x + player.hitbox.width >= plataforma.x and player.hitbox.x <= plataforma.x + plataforma.width:
                if player.hitbox.y <= plataforma.y + plataforma.height and player.hitbox.y + player.hitbox.height >= plataforma.y:
                    player.hitbox.y = player.last_position[1]
                


    
    
    
    def colisao2(cls, player:Player):
        player_esquerda = player.hitbox.x
        player_direita = player.hitbox.x + player.hitbox.width
        player_cabeca = player.hitbox.y
        player_pe = player.hitbox.y + player.hitbox.height
        last_x, last_y = player.last_position[0], player.last_position[1]
        for i, plataforma in enumerate(cls.lista):
            if player.hitbox.collided(plataforma):
                if player_pe + player.hitbox.width < plataforma.x\
                    or player_cabeca + player.hitbox.width < plataforma.x:
                    print("esquerda")