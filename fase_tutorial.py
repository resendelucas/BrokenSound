from PPlay.sprite import Sprite
from PPlay.window import *
from caixa_dialogo import CaixaDialogo
from player import Player
from tiros_player import Tiro
from chao import Chao


class FaseTutorial:
    fundo = Sprite('Assets/imagens/skies/casa_bethoven.png')
    bethoven = Sprite('Assets/character/bethoven.png', )
    cronometro_global = 0
    cronometro_opcional = 0
    pressed_past = {'esc': False,
                    'e': False}
    pressed_ever = {'z': False,
                    'x': False,
                    'left': False,
                    'right': False,
                    'up': False,
                    'down': False}
    sprites_teclas = {}

    def __init__(self, janela: Window):
        self.janela = janela
        self.floor = Chao('floor.png')
        self.floor.y = janela.height-18
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
        self.player_can_shoot = False
        self.player_can_soltar_caixa = False
        self.draw_player_hud = False
        # self.can_change

    def passar_dialogos(self, dialogos: dict, numero_dialogo: int):
        dialogo_atual = dialogos[f'dialogo{numero_dialogo}']
        dialogo_anterior = dialogos.get(f'dialogo{numero_dialogo - 1}')

        if dialogo_anterior:  # se não for o primeiro dialogo
            if dialogo_anterior.is_desativado and not dialogo_atual.is_desativado:  # se passou o anterior e esse não
                dialogo_atual.aparecer(1)
        else:
            if not dialogo_atual.is_desativado:
                dialogo_atual.aparecer(1)

        if self.teclado.key_pressed('e') and not self.pressed_past['e'] and not dialogo_atual.is_desativado:
            self.pressed_past['e'] = True
            dialogo_atual.desaparecer()

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
                               'dialogo8': CaixaDialogo(['A Bruxa Vermelha é uma musicista extremamente poderosa.',
                                                         'Esta é a última fortaleza protegida das garras dela.'],
                                                        self.bethoven),
                               'dialogo9': CaixaDialogo(['Vocês são os escolhidos da profecia da música suprema,',
                                                         'os destinados a libertar o poder musical para o mundo novamente.'],
                                                        self.bethoven),
                               'dialogo10': CaixaDialogo(['Como o último dos 12 grandes músicos, é minha tarefa ',
                                                          'guiar vocês, os escolhidos.',
                                                          'Lhes ensinarei tudo o que sei!!'], self.bethoven),
                               }
        dialogos_tutorial = {'dialogo1': CaixaDialogo(['Não se preocupem, tenho certeza que os escolhidos irão',
                                                       'facilmente aprender as técnicas que ensinarei.'],
                                                      self.bethoven),
                             'dialogo2': CaixaDialogo(['Para se mexer para os lados, aperte (esquerda, direita)',
                                                       'Para pular, aperte (cima).'], self.bethoven),
                             'dialogo3': CaixaDialogo(['Você está no modo violão, uma arma musical versátil e ',
                                                       'razoavelmente poderosa. Aperte (z) para atirar com ela.'],
                                                      self.bethoven),
                             'dialogo4': CaixaDialogo(['Ótimo!'], self.bethoven),
                             'dialogo5': CaixaDialogo(['Os tiros sairão na direção que você estiver olhando. ',
                                                       'Você também pode apertar (baixo) para atirar ',
                                                       'para para baixo. Tente agora.'], self.bethoven),
                             'dialogo6': CaixaDialogo(['Ótimo!'], self.bethoven),
                             'dialogo7': CaixaDialogo(['Durante o modo violão, você tem a habilidade de posicionar ',
                                                       'uma caixa de som apertando X. Aperte (X).'], self.bethoven),
                             'dialogo8': CaixaDialogo(['Muito bem!',
                                                       'Ela dura 6 segundos, e enquanto estiver viva, todos os tiros do',
                                                       'violão sairão por ela.'], self.bethoven),
                             'dialogo9': CaixaDialogo(['A caixa de som pode ser muito útil em algumas situações.',
                                                       'Porém, a depender da situação, se preferir, pode apertar X de',
                                                       'novo para fazê-la desaparecer.'], self.bethoven),
                             'dialogo10': CaixaDialogo(['Os escolhidos têm uma barra de mana.',
                                                        'Com o tempo, ela recarrega.'], self.bethoven),
                             'dialogo11': CaixaDialogo(['Quando a barra de mana estiver cheia, você pode apertar (C) ',
                                                        'para ativar o especial do piano. Aperte (C)'], self.bethoven),
                             'dialogo12': CaixaDialogo(['Enquanto estiver no modo pianista, você estará invulnerável.',
                                                        'Ao apertar (Z) ou segurar, você invoca e atira com seu piano'],
                                                       self.bethoven),
                             'dialogo13': CaixaDialogo(['O modo piano dura um máximo de 3 segundos, mas você pode sair',
                                                        'antes apertando C de novo. Aperte (C)'], self.bethoven),
                             'dialogo14': CaixaDialogo(['Vocês estão prontos! Vão!',
                                                        'Restaurem a música!!'], self.bethoven)

                             }
        # 'dialogo3':CaixaDialogo([''], self.bethoven)
        self.is_player_spawning = True
        while self.is_running:
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
                        for i in range(1, 10):
                            self.passar_dialogos(dialogos_introducao, i)

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
            elif self.tutorial:
                self.is_player_spawning = False
                self.player.update_caixa_de_som(self)
                if not self.player_can_soltar_caixa:
                    self.player.caixa_de_som = None
                # dialogos bethoven
                dialogos_passaveis = (1, 4, 6, 8, 9, 10)
                for i in dialogos_passaveis:
                    self.passar_dialogos(dialogos_tutorial, i)
                moving_keys = ('left', 'right', 'up')
                if dialogos_tutorial['dialogo1'].is_desativado:
                    if dialogos_tutorial['dialogo2'] not in CaixaDialogo.dialogos_ativos:
                        dialogos_tutorial['dialogo2'].aparecer()
                    elif dialogos_tutorial['dialogo2'].is_finished:
                        for key in moving_keys:
                            if self.teclado.key_pressed(key):
                                dialogos_tutorial['dialogo2'].desaparecer()
                                dialogos_tutorial['dialogo3'].aparecer()
                if dialogos_tutorial['dialogo3'].is_finished:
                    self.player_can_shoot = True
                    if self.teclado.key_pressed('z'):
                        dialogos_tutorial['dialogo3'].desaparecer()
                if dialogos_tutorial['dialogo4'].is_desativado:
                    if dialogos_tutorial['dialogo5'] not in CaixaDialogo.dialogos_ativos:
                        dialogos_tutorial['dialogo5'].aparecer()
                    elif dialogos_tutorial['dialogo5'].is_finished:
                        if self.teclado.key_pressed('z') and self.teclado.key_pressed('down'):
                            dialogos_tutorial['dialogo5'].desaparecer()
                if dialogos_tutorial['dialogo6'].is_desativado:
                    dialogos_tutorial['dialogo7'].aparecer()

                if dialogos_tutorial['dialogo7'].is_finished:
                    if self.teclado.key_pressed('x'):
                        dialogos_tutorial['dialogo7'].desaparecer()
                        self.player_can_soltar_caixa = True

                if dialogos_tutorial['dialogo10'] in CaixaDialogo.dialogos_ativos:
                    self.draw_player_hud = True
                if dialogos_tutorial['dialogo10'].is_desativado:
                    dialogos_tutorial['dialogo11'].aparecer()

                if dialogos_tutorial['dialogo11'].is_finished:
                    self.player.healthbar.mana_atual += 35 * self.janela.delta_time()
                    if not dialogos_tutorial['dialogo11'].is_desativado:
                        if self.player.instrumento == 'piano':
                            dialogos_tutorial['dialogo11'].desaparecer()
                            dialogos_tutorial['dialogo12'].aparecer()

                if dialogos_tutorial['dialogo12'].is_finished and not dialogos_tutorial['dialogo12'].is_desativado:
                    if self.player.instrumento == 'piano':
                        dialogos_tutorial['dialogo12'].desaparecer()
                        dialogos_tutorial['dialogo13'].aparecer()
                if dialogos_tutorial['dialogo13'] in CaixaDialogo.dialogos_ativos:
                    self.player.is_imune = True
                    self.player.imune_cronometro = 0
                    if self.player.instrumento == 'piano' and self.teclado.key_pressed('c'):
                        dialogos_tutorial['dialogo13'].desaparecer()
                        dialogos_tutorial['dialogo14'].aparecer()

                # gravidade
                self.player.feel_gravity()
                self.player.apply_motion()
                # movimentos
                if self.player_can_move:
                    self.player.check_events()
                # tiros
                if not self.player_can_shoot:
                    for lista in Tiro.tiros.values():
                        lista.clear()
                else:
                    if self.player.caixa_de_som and not self.player_can_soltar_caixa:
                        self.player.caixa_de_som = None
                    Tiro.update_tiros(self.janela)

                # equivalente ao try landing
                if self.player.hitbox.y > self.janela.height - 18 - self.player.hitbox.height:
                    self.player.hitbox.y = self.janela.height - 18 - self.player.hitbox.height
                    self.player.is_falling = False
                    self.player.can_jump = True

            for key in self.pressed_past.keys():
                self.pressed_past[key] = self.teclado.key_pressed(key)

            if self.player.caixa_de_som and self.player_can_soltar_caixa:
                self.player.caixa_de_som.draw_sprite_and_healthbar()
            self.bethoven.draw()
            self.player.draw_player()
            if self.player2:
                self.player2.draw_player()
            if self.draw_player_hud:
                self.player.draw_hud()
            Tiro.draw_tiros(self.janela)
            CaixaDialogo.update_dialogos()
            CaixaDialogo.draw_dialogos()
