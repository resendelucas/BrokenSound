from PPlay.window import *
from fase2 import Fase2
from fase1 import Fase1
from menu import Menu
from piano_boss import BossPiano
from guitar_boss import BossGuitarra
from obeliscos import Obelisco
from plataforma import Plataforma
from player import Player
from skeletons import Skeleton
from teleguiados import TiroTeleguiado
from tiros_player import Tiro

frames_acumulados = 0
tempo_acumulado = 0
fps = None
# janela = Window(1365, 768)
janela = Window(1365, 768)
boss_atual = BossPiano(janela)
# mapa_atual = Fase1x(janela, boss_atual)
mapa_atual = Fase2(janela, boss_atual)
mapa_atual.inicializar_plataformas()
player = Player(janela, mapa_atual, 'piano')
boss_atual.set_player(player)
player.hitbox.vely = 0
menu = Menu(janela)
menu.playing = False
teclado = janela.get_keyboard()
janela.update()

while True:
    # print(boss_atual.sprites["summoner_arriving"] == boss_atual.sprite_atual)
    frames_acumulados += 1
    tempo_acumulado += janela.delta_time()
    if tempo_acumulado > 0.3:
        fps = frames_acumulados / tempo_acumulado
        tempo_acumulado = frames_acumulados = 0
    janela.update()
    # if janela.delta_time() > 0.005:
    #     # evita bugs de física
    #     continue
    if not menu.playing:
        menu.check_events()
        menu.draw_menu()
    else:
        # inputs
        boss_atual.cheat_hit()
        if teclado.key_pressed("f"):
            player.vely = 50
            boss_atual.spawn()
            boss_atual.velx = 0
            boss_atual.y = 0
        if teclado.key_pressed("v"):
            player.healthbar.mana_atual = 100
            '''boss_atual.vely = 0
            boss_atual.hitbox.x += 1000 * janela.delta_time()'''
        if teclado.key_pressed("b"):
            boss_atual.vely = 0
            boss_atual.hitbox.x -= 1000 * janela.delta_time()
        Plataforma.colisao_cima(player)
        if player.healthbar.health_atual > 0:
            player.check_events()
        else:
            if player.healthbar.old_health_ratio == 0:
                menu.playing = False
        # updates
        listaobjetos = [mapa_atual.background, mapa_atual.floor] + Plataforma.lista \
                       + Tiro.get_every_tiro() + [boss_atual.hitbox] + Skeleton.get_hitboxes() + Obelisco.lista
        if player.caixa_de_som:
            listaobjetos.append(player.caixa_de_som)
        player.apply_motion()
        Tiro.update_tiros(janela, [boss_atual] + Skeleton.lista_inimigos + Obelisco.lista)
        player.feel_gravity()
        player.check_camera(listaobjetos, mapa_atual)
        mapa_atual.floor.try_landing_player(player)
        player.update_caixa_de_som(mapa_atual)
        mapa_atual.try_landing_boss()
        boss_atual.update()
        # player.check_camera()
        # draws
        player.hitbox.draw()  # draw visualmente inútil, já que é antes do mapa, mas importante pro c. perfect funcionar
        mapa_atual.draw_elements()
        player.draw_player()
        if player.caixa_de_som:
            player.caixa_de_som.draw_sprite_and_healthbar()
        Plataforma.draw_plataformas(janela)
        boss_atual.draw_boss()
        player.check_hit_boss(boss_atual, Skeleton.lista_inimigos)
        Tiro.draw_tiros(janela)
        Skeleton.draw_esqueletos()
        # boss_atual.hitbox.draw()
        # print(player.hitbox.x, player.hitbox.y)
        # print(Plataforma.lista[0].y)
        TiroTeleguiado.draw_tiros_teleguiados()
        if boss_atual.is_mini_game_on and not boss_atual.is_mini_game_done:
            boss_atual.mini_game.draw_elements()

        if player.healthbar.health_atual <= 0:
            menu.you_died_screen()
        player.draw_hud()
    janela.draw_text(f'{fps:.2f}', janela.width * 1 / 10, janela.height * 1 / 12, 30, (255, 255, 0))
