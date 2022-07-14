from PPlay.sprite import Sprite
from PPlay.window import *
from caixa_dialogo import CaixaDialogo
from player import Player


class FaseTutorial:
    fundo = Sprite('Assets/imagens/skies/casa_bethoven.png')
    bethoven = Sprite('Assets/character/bethoven.png', )
    def __init__(self, janela: Window):
        self.janela = janela
        self.bethoven.set_position(144, 502)
        self.player = Player(janela, self, 'violao')
        self.player.hitbox.set_position(500, 603)
        self.fundo.y = self.janela.height - self.fundo.height

    def run_tutorial(self):
        dialogo = CaixaDialogo(['Há muito tempo, a Bruxa Vermelha lançou um feitiço',
                                'sob o mundo, e todos os que não detinham excepcional poder musical',
                                'se tornaram incapazes de ouvir e tocar qualquer nota musical.'], self.bethoven)
        dialogo.set_player(self.player)
        while True:
            self.janela.update()
            self.janela.set_background_color((0, 0, 0))
            self.fundo.draw()
            self.bethoven.draw()
            self.player.draw_player()
            dialogo.update()
            dialogo.draw()
