from PPlay import gameimage
from PPlay.window import *
from mapa import Mapa
from player import Player
from tiros import Tiro
from plataforma import Plataforma
from chao import Chao
# janela = Window(1366, 768)
janela = Window(800, 700)
mapa = Mapa(janela)
player = Player(janela, mapa)
Plataforma(32*7, 32*15, '1x4')
Plataforma(32*20, 32*15, '1x4')
Plataforma(32*27, 32*11, '1x4')
player.hitbox.vely = 0
while True:
    janela.update()
    # inputs
    Plataforma.colisao_horizontal(player)
    Plataforma.colisao_vertical(player)
    player.check_events()
    # updates
    player.apply_motion()
    Tiro.update_tiros(janela)
    player.feel_gravity()

    player.check_camera([mapa.background, mapa.floor])
    player.check_camera(Plataforma.lista)
    mapa.floor.try_landing(player)
    # player.check_camera()
    # draws
    mapa.draw_elements()
    player.draw_player()
    Plataforma.draw_plataformas(janela)
    Tiro.draw_tiros(janela)
    # print(player.hitbox.x, player.hitbox.y)
    # print(Plataforma.lista[0].y)