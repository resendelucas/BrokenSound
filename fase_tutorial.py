from PPlay.sprite import Sprite
from PPlay.window import *
from caixa_dialogo import CaixaDialogo
from player import Player


class FaseTutorial:
    fundo = Sprite('Assets/imagens/skies/casa_bethoven.png')
    bethoven = Sprite('Assets/character/bethoven.png', )
    cronometro_global = 0
    cronometro_opcional = 0
    pressed_past = {'esc': False,
                    'e': False}
    sprites_teclas = {}

    def __init__(self, janela: Window):
        self.janela = janela
        self.bethoven.set_position(196, 675)
        self.player = Player(janela, self, 'violao')
        self.player2 = Player(janela, self, 'piano')
        self.player.hitbox.set_position(278, 400)
        self.player2.hitbox.set_position(330, 415)
        self.fundo.y = self.janela.height - self.fundo.height
        self.is_running = True
        self.is_player_spawning = False
        self.teclado = self.janela.get_keyboard()
        self.player_can_move = False
        self.tutorial = False

    def passar_dialogos(self, dialogos: dict, numero_dialogo: int):
        dialogo_atual = dialogos[f'dialogo{numero_dialogo}']
        dialogo_anterior = dialogos.get(f'dialogo{numero_dialogo - 1}')

        if dialogo_anterior:  # se não for o primeiro dialogo
            if dialogo_anterior.is_desativado and not dialogo_atual.is_desativado:  # se passou o anterior e esse não
                dialogo_atual.aparecer(1)
        else:
            if not dialogo_atual.is_desativado:
                dialogo_atual.aparecer()

        if self.teclado.key_pressed('e') and not self.pressed_past['e'] and not dialogo_atual.is_desativado:
            self.pressed_past['e'] = True
            print('a')
            dialogo_atual.desaparecer()
            print(f' {numero_dialogo}desapareceu')

    def run_tutorial(self):
        CaixaDialogo.set_player(self.player)
        dialogos_introducao = {'dialogo1': CaixaDialogo(['Funcionou! Funcionou!!',
                                                         'Graças aos céus!!'], self.bethoven),
                               'dialogo2': CaixaDialogo(['???'], self.player.hitbox),
                               'dialogo3': CaixaDialogo(['???'], self.player2.hitbox),
                               'dialogo4': CaixaDialogo(
                                   ['perdão viajantes, permitam-me', 'explicar o que está acontecendo.'],
                                   self.bethoven),
                               'dialogo5': CaixaDialogo(['Eu lhes invoquei aqui para me ajudar em uma',
                                                         'tarefa de extrema importância!'], self.bethoven),
                               'dialogo6': CaixaDialogo(['Há muito tempo, a Bruxa Vermelha lançou um feitiço',
                                                         'sob o mundo, e todos os que não detinham excepcional poder musical'],
                                                        self.bethoven),
                               'dialogo7': CaixaDialogo(
                                   ['se tornaram incapazes de ouvir e tocar qualquer nota musical.'], self.bethoven),
                               'dialogo8': CaixaDialogo(['A Bruxa Vermelha é uma músicista extremamente poderosa.',
                                                         'Esta é a última fortaleza protegida das garras dela.'],
                                                        self.bethoven),
                               'dialogo9': CaixaDialogo(['Vocês são os escolhidos da profecia da música suprema,',
                                                         'os destinados a libertar o poder musical para o mundo novamente.'],
                                                        self.bethoven),
                               'dialogo10': CaixaDialogo(['Como o último dos 12 grandes músicos, é minha tarefa ',
                                                          'guiar vocês, os escolhidos.',
                                                          'Lhes ensinarei tudo o que sei!!'], self.bethoven),
                               }
        self.is_player_spawning = True
        while self.is_running:
            print(self.pressed_past['e'])
            # draws fundo
            self.janela.update()
            self.janela.set_background_color((0, 0, 0))
            self.fundo.draw()
            # updates basicos
            self.cronometro_global += self.janela.delta_time()

            # updates específicos à parte do tutorial
            if self.is_player_spawning:
                dialogos_introducao['dialogo1'].aparecer()
                # print(f'{self.player.hitbox.y}, {self.janela.height}, {260}, {self.player.hitbox.height}')
                # print(self.player.hitbox.y, self.player.hitbox.y < self.janela.height - 260 - self.player.hitbox.height)
                # fazendo cairem devagar
                # se player2 não pisou no chao
                if self.player2.hitbox.y < self.janela.height - 18 - self.player2.hitbox.height:
                    self.player2.hitbox.y -= -50 * self.janela.delta_time()
                    self.player2.changecharacter('piano')
                    self.player2.sprite_atual = self.player2.sprites['piano']['still_right']
                # se player não pisou no chão
                if self.player.hitbox.y < self.janela.height - 18 - self.player.hitbox.height:
                    self.player.changecharacter('violao')
                    self.player.hitbox.y -= -50 * self.janela.delta_time()
                    self.player.sprite_atual = self.player.sprites['violao']['still_left']
                    self.cronometro_global = 0
                else:
                    dialogos_introducao['dialogo1'].desaparecer()
                    dialogos_introducao['dialogo2'].aparecer()
                    dialogos_introducao['dialogo3'].aparecer()
                    if self.cronometro_global <= 4.2:
                        if int(self.cronometro_global) % 2 == 0:
                            self.player.sprite_atual = self.player.sprites['violao']['still_left']
                            self.player2.sprite_atual = self.player.sprites['piano']['still_left']
                        else:
                            self.player.sprite_atual = self.player.sprites['violao']['still_right']
                            self.player2.sprite_atual = self.player.sprites['piano']['still_right']
                    else:
                        dialogos_introducao['dialogo2'].desaparecer()
                        dialogos_introducao['dialogo3'].desaparecer()
                        self.passar_dialogos(dialogos_introducao, 4)
                        self.passar_dialogos(dialogos_introducao, 5)
                        self.passar_dialogos(dialogos_introducao, 6)
                        self.passar_dialogos(dialogos_introducao, 7)
                        self.passar_dialogos(dialogos_introducao, 8)
                        self.passar_dialogos(dialogos_introducao, 9)
                        if dialogos_introducao['dialogo9'].is_desativado and not dialogos_introducao[
                            'dialogo10'].is_desativado:
                            dialogos_introducao['dialogo10'].aparecer()
                            if self.teclado.key_pressed('e') and not self.pressed_past['e']:
                                dialogos_introducao['dialogo10'].desaparecer()
                                self.pressed_past['e'] = True

                                self.is_player_spawning = False
                                self.player2 = None
                                self.player_can_move = True
                                self.tutorial = True
                        self.cronometro_opcional += self.janela.delta_time()
                if self.tutorial:
                    self.player.check_events()

            for key in self.pressed_past.keys():
                self.pressed_past[key] = self.teclado.key_pressed(key)

            self.bethoven.draw()
            self.player.draw_player()
            if self.player2:
                self.player2.draw_player()
            self.player.draw_hud()
            CaixaDialogo.update_dialogos()
            CaixaDialogo.draw_dialogos()
