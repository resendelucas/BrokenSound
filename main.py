from PPlay.window import *
from mapa import Mapa
from player import Player
from tiros import Tiro
from plataforma import Plataforma
# janela = Window(1366, 768)
janela = Window(800, 700)
mapa = Mapa(janela)
player = Player(janela, mapa)
Plataforma(32*7, 32*15, '1x4')
player.hitbox.vely = 0
while True:
    janela.update()
    # inputs
    Plataforma.colisao(player)
    player.check_events()
    if janela.keyboard.key_pressed("up"):
        player.hitbox.y -= 150 * janela.delta_time()
    if janela.keyboard.key_pressed("down"):
        player.hitbox.y += 150 * janela.delta_time() 
    player.hitbox.y += 0.05
    # updates
    Tiro.update_tiros(janela)
    # draws
    mapa.draw_elements()
    player.draw_player()
    Plataforma.draw_plataformas(janela)
    Tiro.draw_tiros(janela)
    # print(player.hitbox.x, player.hitbox.y)
    # print(Plataforma.lista[0].y)