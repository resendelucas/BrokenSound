from PPlay.gameimage import GameImage
from player import Player
from os import getcwd
class Chao(GameImage):
    path = f'{getcwd()}\\assets\\imagens\\Floors'
    
    def __init__(self, image_filename: str, y: float, buracos:list = []):
        """ Buracos será uma lista de tuplas com x iniciais e finais onde o player pode cair e morrer"""
        super().__init__(f'{self.path}\\{image_filename}')
        self.x = 0
        self.y = y
        self.buracos = buracos
        
    def try_landing(self, entity:Player):
        if entity.hitbox.y + entity.hitbox.height >= self.y:
            entity_no_buraco = False
            if self.buracos:
                for buraco in self.buracos:
                    x_inicial, x_final = buraco[0], buraco[1]
                    if entity.hitbox.x > x_inicial and entity.hitbox.x + entity.hitbox.width < x_final:
                        entity_no_buraco = True
            if entity_no_buraco is False:
                entity.hitbox.y = self.y - entity.hitbox.height
                entity.vely = 0
                
                entity.can_jump = True
                entity.is_falling = False