from PPlayTeste.window import *
from mapa import Mapa
from player import Player


# janela = Window(1366, 768)
janela = Window(800, 700)
mapa = Mapa(janela)
player = Player(janela, mapa)

while True:
    mapa.draw_elements()
    player.check_events()
    player.draw_player()
    janela.update()
