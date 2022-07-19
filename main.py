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
from fase_tutorial import FaseTutorial
from PPlay.sprite import *
from boss_mae import BossClasseMae
from gaiola import Gaiola
from mini_game import MiniGame
from minigame_teclas import MiniGameTeclas
from playerhealthbar import PlayerHealthBar

while True:
    frames_acumulados = 0
    tempo_acumulado = 0
    fps = None
    # janela = Window(1365, 768)
    janela = Window(1365, 768)
    menu = Menu(janela)
    menu.playing = False
    teclado = janela.get_keyboard()
    janela.update()
    setinha = Sprite("Assets/imagens/arrow.png")
    setinha.set_position(janela.width - 60, janela.height - 150)
    tutorial = FaseTutorial(janela)
    while not menu.playing:
        janela.update()
        menu.check_events()
        menu.draw_menu()
    tutorial.is_done = False if menu.fase_inicial == 'tutorial' else True
    boss_atual = BossPiano(janela) if menu.fase_inicial != 'bruxa vermelha' else BossGuitarra(janela)
    mapa_atual = Fase2(janela, boss_atual) if menu.fase_inicial != 'bruxa vermelha' else Fase1(janela, boss_atual)
    player = Player(janela, mapa_atual, 'violao')
    boss_atual.set_player(player)
    while menu.playing:
        # print(boss_atual.boss_name)
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
        if not tutorial.is_done:
            tutorial.run_tutorial()
        # inputs
        boss_atual.cheat_hit()
        Plataforma.colisao_cima(player)
        if player.healthbar.health_atual > 0:
            player.check_events()
        else:
            if player.healthbar.old_health_ratio == 0:
                boss_atual = BossGuitarra(janela)
                tutorial = FaseTutorial(janela)
                mapa_atual = Fase1(janela, boss_atual)
                player = Player(janela, mapa_atual, 'piano')
                boss_atual.set_player(player)
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
        if not mapa_atual.over:
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

        if not mapa_atual.over:
            player.draw_hud()

        # Troca de fase
        if boss_atual.is_finished and not boss_atual.boss_final:
            setinha.draw()
            if player.hitbox.x > janela.width - 50:
                mapa_atual.limpar_plataformas()
                boss_atual = BossGuitarra(janela)
                mapa_atual = Fase1(janela, boss_atual)
                player = Player(janela, mapa_atual, 'violao')
                boss_atual.set_player(player)
        if player.teclado.key_pressed('esc'):
            break
    Player.reset_class()
    BossGuitarra.reset_class()
    BossClasseMae.reset_class()
    Gaiola.reset_class()
    BossPiano.reset_class()
    Tiro.reset_class()
    MiniGameTeclas.reset_class()
    MiniGame.reset_class()
    PlayerHealthBar.reset_class()
    Obelisco.reset_class()
    Plataforma.reset_class()
    Player.reset_class()
    Skeleton.reset_class()
    TiroTeleguiado.reset_class()
