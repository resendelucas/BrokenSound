from PPlay.window import *
from mapa import Mapa
from player import Player
from tiros import Tiro

# janela = Window(1366, 768)
janela = Window(800, 700)
mapa = Mapa(janela)
player = Player(janela, mapa)

while True:
    janela.update()
    # inputs
    player.check_events()
    # updates
    Tiro.update_tiros(janela)
    # draws
    mapa.draw_elements()
    player.draw_player()
    Tiro.draw_tiros(janela)
    
