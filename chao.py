from os import getcwd

from PPlay.gameimage import GameImage


class Chao(GameImage):
    path = f'{getcwd()}\\assets\\imagens\\Floors'

    def __init__(self, image_filename: str, buracos: list = None):
        """ Buracos será uma lista de tuplas com distancia iniciais e finais do
        inicio do chão onde o player pode cair e morrer"""
        super().__init__(f'{self.path}\\{image_filename}')
        self.x = 0
        self.buracos = buracos

    def try_landing_boss(self, boss):
        if boss.hitbox.y + boss.hitbox.height > self.y:
            boss.hitbox.y = self.y - boss.hitbox.height
            boss.vely = 0
            boss.is_falling = False

            if boss.is_arriving:
                boss.is_arriving = False
                boss.is_imune = False
                boss.is_idle = True
                boss.sprite_atual = boss.sprites["idle_left"]
                boss.cronometro_animacao = 0
                boss.sprite_atual.set_total_duration(1.7)

    def try_landing_player(self, player):
        if player.hitbox.y + player.hitbox.height >= self.y:
            entity_no_buraco = False
            ''' # A ser implementado
            if self.buracos:
                for buraco in self.buracos:
                    x_inicial, x_final = buraco[0], buraco[1]
                    if player.hitbox.x > x_inicial and player.hitbox.x + player.hitbox.width < x_final:
                        entity_no_buraco = True'''
            if entity_no_buraco is False:
                player.hitbox.y = self.y - player.hitbox.height
                player.vely = 0
                player.can_jump = True
                player.is_falling = False
                
    def try_landing_sprite(self, sprite):
        if sprite.y + sprite.height >= self.y:
            entity_no_buraco = False
            ''' # A ser implementado
            if self.buracos:
                for buraco in self.buracos:
                    x_inicial, x_final = buraco[0], buraco[1]
                    if player.hitbox.x > x_inicial and player.hitbox.x + player.hitbox.width < x_final:
                        entity_no_buraco = True'''
            if entity_no_buraco is False:
                sprite.y = self.y - sprite.height
                sprite.vely = 0
                sprite.can_jump = True
                sprite.is_falling = False
