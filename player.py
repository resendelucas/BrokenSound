from PPlay.sprite import *
from PPlay.window import *
from caixadesom import CaixaDeSom
from playerhealthbar import PlayerHealthBar
from tiros_player import Tiro


class Player:
    # sprites visuais:
    Window(1365, 768)
    instrumento = 'violao'
    proximo_instrumento = {'violao': 'piano',
                           'piano': 'violao'}
    sprites = {'violao': {"walk_right": Sprite(f"Assets/character/violao/walking/walk_right.png", 6),
                          'walk_left': Sprite(f"Assets/character/violao/walking/walk_left.png", 6),
                          'walk_attack_right': Sprite(f"Assets/character/violao/walking/walk_attack_right.png", 6),
                          'walk_attack_left': Sprite(f"Assets/character/violao/walking/walk_attack_left.png", 6),
                          'playing_right': Sprite(f"Assets/character/violao/parado/attack_right.png", 4),
                          'playing_left': Sprite(f"Assets/character/violao/parado/attack_left.png", 4),
                          'still_right': Sprite(f"Assets/character/violao/parado/player_still_right.png"),
                          'still_left': Sprite(f"Assets/character/violao/parado/player_still_left.png")},
               'piano': {"walk_right": Sprite(f"Assets/character/piano/walking/walk_right.png", 6),
                         'walk_left': Sprite(f"Assets/character/piano/walking/walk_left.png", 6),
                         'playing_right': Sprite(f"Assets/character/piano/parado/attack_right.png", 2),
                         'playing_left': Sprite(f"Assets/character/piano/parado/attack_left.png", 2),
                         'still_right': Sprite(f"Assets/character/piano/parado/player_still_right.png", 4),
                         'still_left': Sprite(f"Assets/character/piano/parado/player_still_left.png", 4),
                         'charging_left': Sprite(f"Assets/character/piano/parado/charging_left.png", 6),
                         'charging_right': Sprite(f"Assets/character/piano/parado/charging_right.png", 6),
                         'piano_left': Sprite(f"Assets/character/piano/piano_left.png"),
                         'piano_right': Sprite(f"Assets/character/piano/piano_right.png"), },
               'changing': Sprite(f'Assets/character/changing.png', 10)}
    # sprites usadas no backend:
    hitboxes = {'desmontado': Sprite("Assets/character/player_hitbox.png"),
                'montado': Sprite("Assets/character/player_hitbox_piano.png")}
    sprite_atual = sprites["violao"]["walk_right"]
    # cooldown tiros:
    cooldown_value = 0.3
    walkspeed_padrao = 200

    hud_instrumento_frame = Sprite("Assets/hud/hud-instrumento-frame.png")
    hud_instrumento_frame.set_position(40, 40)
    hud_instrumento_violao = Sprite("Assets/hud/hud-instrumento-violao.png")
    hud_instrumento_violao.set_position(72, 60)
    hud_instrumento_piano = Sprite("Assets/hud/hud-instrumento-piano.png")
    hud_instrumento_piano.set_position(72, 60)
    gravity = 4500
    key_pressed_past = {"x": False,
                        "q": False,
                        "w": False,
                        "e": False,
                        "r": False, }

    @classmethod
    def reset_class(cls):
        # sprites visuais:
        Window(1365, 768)
        cls.instrumento = 'violao'
        cls.proximo_instrumento = {'violao': 'piano',
                                   'piano': 'violao'}
        cls.sprites = {'violao': {"walk_right": Sprite(f"Assets/character/violao/walking/walk_right.png", 6),
                                  'walk_left': Sprite(f"Assets/character/violao/walking/walk_left.png", 6),
                                  'walk_attack_right': Sprite(f"Assets/character/violao/walking/walk_attack_right.png",
                                                              6),
                                  'walk_attack_left': Sprite(f"Assets/character/violao/walking/walk_attack_left.png",
                                                             6),
                                  'playing_right': Sprite(f"Assets/character/violao/parado/attack_right.png", 4),
                                  'playing_left': Sprite(f"Assets/character/violao/parado/attack_left.png", 4),
                                  'still_right': Sprite(f"Assets/character/violao/parado/player_still_right.png"),
                                  'still_left': Sprite(f"Assets/character/violao/parado/player_still_left.png")},
                       'piano': {"walk_right": Sprite(f"Assets/character/piano/walking/walk_right.png", 6),
                                 'walk_left': Sprite(f"Assets/character/piano/walking/walk_left.png", 6),
                                 'playing_right': Sprite(f"Assets/character/piano/parado/attack_right.png", 2),
                                 'playing_left': Sprite(f"Assets/character/piano/parado/attack_left.png", 2),
                                 'still_right': Sprite(f"Assets/character/piano/parado/player_still_right.png", 4),
                                 'still_left': Sprite(f"Assets/character/piano/parado/player_still_left.png", 4),
                                 'charging_left': Sprite(f"Assets/character/piano/parado/charging_left.png", 6),
                                 'charging_right': Sprite(f"Assets/character/piano/parado/charging_right.png", 6),
                                 'piano_left': Sprite(f"Assets/character/piano/piano_left.png"),
                                 'piano_right': Sprite(f"Assets/character/piano/piano_right.png"), },
                       'changing': Sprite(f'Assets/character/changing.png', 10)}
        # sprites usadas no backend:
        cls.hitboxes = {'desmontado': Sprite("Assets/character/player_hitbox.png"),
                        'montado': Sprite("Assets/character/player_hitbox_piano.png")}
        cls.sprite_atual = cls.sprites["violao"]["walk_right"]
        # cooldown tiros:
        cls.cooldown_value = 0.3
        cls.walkspeed_padrao = 200

        cls.hud_instrumento_frame = Sprite("Assets/hud/hud-instrumento-frame.png")
        cls.hud_instrumento_frame.set_position(40, 40)
        cls.hud_instrumento_violao = Sprite("Assets/hud/hud-instrumento-violao.png")
        cls.hud_instrumento_violao.set_position(72, 60)
        cls.hud_instrumento_piano = Sprite("Assets/hud/hud-instrumento-piano.png")
        cls.hud_instrumento_piano.set_position(72, 60)
        cls.gravity = 4500
        cls.key_pressed_past = {"x": False,
                                "q": False,
                                "w": False,
                                "e": False,
                                "r": False, }

    def __init__(self, janela: Window, mapa, instrumento: str):
        self.reset_instance()

        self.hud_instrumento_frame = Sprite("Assets/hud/hud-instrumento-frame.png")
        self.hud_instrumento_frame.set_position(40, 40)
        self.hud_instrumento_violao = Sprite("Assets/hud/hud-instrumento-violao.png")
        self.hud_instrumento_violao.set_position(72, 60)
        self.hud_instrumento_piano = Sprite("Assets/hud/hud-instrumento-piano.png")
        self.hud_instrumento_piano.set_position(72, 60)
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.walkspeed = 200
        self.instrumento = instrumento
        self.last_direction = 'right'
        self.cooldown_passado = 0
        self.hitbox = self.hitboxes['desmontado']
        self.ready = True  # se pode atirar (n??o est?? em cooldown)
        self.hitbox.set_position(50, 608)
        self.is_playing = False
        self.gravity_on = False
        self.can_jump = True
        self.is_falling = False
        self.vely = self.velx = 0
        self.jumpspeed = 1200
        self.last_position = [0, 0]
        self.v_camera = 200
        self.can_move = True
        self.piano_charge = self.delay_piano_atual = 0
        self.piano_charge_time, self.delay_piano_valor = 0.2, 0.05
        self.show_piano, self.playing_piano = False, False
        self.c_pressed_past = False
        self.changing_character = False
        self.is_imune = False
        self.imune_duracao = 3
        self.imune_cronometro = 0
        self.healthbar = PlayerHealthBar(5, 5, self.janela)
        self.caixa_de_som = None

    def reset_instance(self):
        self.instrumento = 'violao'
        self.proximo_instrumento = {'violao': 'piano',
                                    'piano': 'violao'}
        self.sprites = {'violao': {"walk_right": Sprite(f"Assets/character/violao/walking/walk_right.png", 6),
                                   'walk_left': Sprite(f"Assets/character/violao/walking/walk_left.png", 6),
                                   'walk_attack_right': Sprite(f"Assets/character/violao/walking/walk_attack_right.png",
                                                               6),
                                   'walk_attack_left': Sprite(f"Assets/character/violao/walking/walk_attack_left.png",
                                                              6),
                                   'playing_right': Sprite(f"Assets/character/violao/parado/attack_right.png", 4),
                                   'playing_left': Sprite(f"Assets/character/violao/parado/attack_left.png", 4),
                                   'still_right': Sprite(f"Assets/character/violao/parado/player_still_right.png"),
                                   'still_left': Sprite(f"Assets/character/violao/parado/player_still_left.png")},
                        'piano': {"walk_right": Sprite(f"Assets/character/piano/walking/walk_right.png", 6),
                                  'walk_left': Sprite(f"Assets/character/piano/walking/walk_left.png", 6),
                                  'playing_right': Sprite(f"Assets/character/piano/parado/attack_right.png", 2),
                                  'playing_left': Sprite(f"Assets/character/piano/parado/attack_left.png", 2),
                                  'still_right': Sprite(f"Assets/character/piano/parado/player_still_right.png", 4),
                                  'still_left': Sprite(f"Assets/character/piano/parado/player_still_left.png", 4),
                                  'charging_left': Sprite(f"Assets/character/piano/parado/charging_left.png", 6),
                                  'charging_right': Sprite(f"Assets/character/piano/parado/charging_right.png", 6),
                                  'piano_left': Sprite(f"Assets/character/piano/piano_left.png"),
                                  'piano_right': Sprite(f"Assets/character/piano/piano_right.png"), },
                        'changing': Sprite(f'Assets/character/changing.png', 10)}
        # sprites usadas no backend:
        self.hitboxes = {'desmontado': Sprite("Assets/character/player_hitbox.png"),
                         'montado': Sprite("Assets/character/player_hitbox_piano.png")}
        self.sprite_atual = self.sprites["violao"]["walk_right"]
        # cooldown tiros:
        self.cooldown_value = 0.3
        self.walkspeed_padrao = 200

    def check_hit_boss(self, boss, inimigos):
        if not self.is_imune and not boss.is_dying:
            if boss.is_sprites_individuais:
                indice_frame = int(boss.sprite_atual.get_curr_frame())
                print(indice_frame)
                colisao_boss = boss.lista_sprite_atual[indice_frame].collided_perfect(self.sprite_atual)
            else:
                colisao_boss = boss.sprite_atual.collided_perfect(self.sprite_atual)
            if colisao_boss:
                self.levar_dano(1)
                return
            for tiro in boss.lista_tiros:
                if self.sprite_atual.collided_perfect(tiro):
                    self.levar_dano(1)
                    return
            for inimigo in inimigos:
                if inimigo.sprite_atual.collided(self.sprite_atual) and not inimigo.is_dying and not \
                        inimigo.is_spawning:
                    self.levar_dano(1)
                    return

    def levar_dano(self, qtd_dano):
        self.healthbar.levar_dano(qtd_dano)
        self.is_imune = True

    def spawn_caixa_de_som(self):
        self.caixa_de_som = CaixaDeSom(self.last_direction, self.hitbox, self.janela)
        self.caixa_de_som.set_total_duration(self.cooldown_value)

    def feel_gravity(self):
        if self.is_falling is True:
            self.can_jump = False
            self.vely -= self.gravity * self.janela.delta_time()

    def apply_motion(self):
        self.hitbox.y -= self.vely * self.janela.delta_time()
        self.hitbox.x += self.velx * self.janela.delta_time()

    def jump(self):
        self.vely = self.jumpspeed
        self.can_jump = False
        self.is_falling = True

    def update_caixa_de_som(self, mapa):
        if self.caixa_de_som:
            self.caixa_de_som.is_falling = True
            self.caixa_de_som.feel_gravity(self.gravity)
            self.caixa_de_som.apply_motion()
            self.caixa_de_som.tick_time()
            mapa.floor.try_landing_sprite(self.caixa_de_som)
            if hasattr(mapa, 'Plataforma_classe'):
                mapa.Plataforma_classe.colisao_cima_sprite(self.caixa_de_som)
            if self.is_playing and self.instrumento == 'violao':
                duracao = self.caixa_de_som.get_total_duration()
                qtdframes = self.caixa_de_som.get_final_frame()
                intervalo = duracao / qtdframes
                self.caixa_de_som.set_curr_frame((self.caixa_de_som.cronometro // intervalo) % qtdframes)
            else:
                self.caixa_de_som.set_curr_frame(0)
                self.caixa_de_som.cronometro = 0
            if self.caixa_de_som.health_ratio == 0:
                self.caixa_de_som = None

    def check_events(self) -> None:
        inicio = self.instrumento
        """Checa inputs do player e muda as vari??veis de estado de acordo."""
        # checar se est?? tocando m??sica
        self.last_position[0], self.last_position[1] = self.hitbox.x, self.hitbox.y
        self.is_playing = self.teclado.key_pressed("z")
        hitbox_anterior = self.hitbox

        self.hitbox = self.hitboxes['desmontado' if not self.playing_piano else 'montado']
        self.hitbox.set_position(hitbox_anterior.x, hitbox_anterior.y)

        if not self.key_pressed_past["x"] and self.teclado.key_pressed("x") and self.instrumento == 'violao':
            self.playing_piano = False
            if self.caixa_de_som:
                self.caixa_de_som = None
            else:
                self.spawn_caixa_de_som()
        self.key_pressed_past["x"] = self.teclado.key_pressed("x")

        if self.is_playing:
            # Se tocar piano, o personagem carrega o piano na tela
            if self.instrumento == 'piano':
                self.can_move = False
                self.sprite_atual = self.sprites[self.instrumento][f'charging_{self.last_direction}']
                self.piano_charge += self.janela.delta_time()
                if self.piano_charge >= self.piano_charge_time and not self.show_piano and not self.playing_piano:
                    self.show_piano = True
                    self.sprites[self.instrumento]["piano_left"].set_position(self.hitbox.x - 110, self.hitbox.y)
                    self.sprites[self.instrumento]["piano_right"].set_position(self.hitbox.x + 70, self.hitbox.y)
                    self.piano_charge = 0
                    self.is_playing = False
            else:
                self.can_move = True
                self.sprite_atual = self.sprites[self.instrumento][f'playing_{self.last_direction}']
        else:
            self.piano_charge = 0
            self.delay_piano_atual = 0
        # Se o piano estiver na tela, ter?? um tempo de recarga para o personagem tocar
        if self.show_piano is True:
            self.delay_piano_atual += self.janela.delta_time()
            if self.delay_piano_atual >= self.delay_piano_valor:
                self.delay_piano_atual = 0
                self.show_piano = False
                self.playing_piano = True

        # Enquanto estiver tocando piano, o player n??o poder?? se mover
        if self.playing_piano:
            self.vely = 0
            self.is_falling = False
            self.can_jump = False
            self.can_move = False
            self.y = self.last_position[1]
            self.sprite_atual = self.sprites[self.instrumento][f"playing_{self.last_direction}"]
        else:
            self.can_move = True

        # Usar especial do piano
        if self.c_pressed_past and not self.teclado.key_pressed('c'):
            if self.healthbar.mana_ratio == 1:
                self.changecharacter('piano')
                self.healthbar.perder_mana(100)
                self.is_imune = True
                self.cooldown_value = 0.05
            elif self.instrumento != 'violao':
                self.changecharacter('violao')
                self.cooldown_value = 0.3
        if self.instrumento == 'piano' and not self.is_imune:
            self.changecharacter('violao')
            self.cooldown_value = 0.3

        self.c_pressed_past = self.teclado.key_pressed('c')
        # checar pulo 
        if self.teclado.key_pressed("UP"):
            if self.can_jump:
                self.jump()
        else:
            if self.can_jump is False and self.is_falling is False:
                self.vely *= 0.07
                self.is_falling = True
        # checar se est?? apertando pra direita
        if self.teclado.key_pressed("RIGHT"):
            self.last_direction = 'right'
            if self.can_move:
                self.hitbox.x += self.walkspeed * self.janela.delta_time()
                if not self.is_playing:
                    self.sprite_atual = self.sprites[self.instrumento]["walk_right"]
                else:
                    if self.instrumento == 'violao':
                        self.sprite_atual = self.sprites[self.instrumento][f'walk_attack_{self.last_direction}']

        # checar se est?? apertando pra esquerda
        elif self.teclado.key_pressed("LEFT"):
            self.last_direction = 'left'
            if self.can_move:
                self.hitbox.x -= self.walkspeed * self.janela.delta_time()
                if not self.is_playing:
                    self.sprite_atual = self.sprites[self.instrumento]["walk_left"]
                else:
                    if self.instrumento == 'violao':
                        self.sprite_atual = self.sprites[self.instrumento][f'walk_attack_{self.last_direction}']
        else:  # se nenhuma tecla de movimento estiver sendo apertada
            if not self.is_playing and not self.playing_piano:
                self.sprite_atual = self.sprites[self.instrumento][f'still_{self.last_direction}']
            else:
                if self.instrumento == 'violao':
                    self.sprite_atual = self.sprites[self.instrumento][f'playing_{self.last_direction}']
        # se, ap??s os movimentos, o player estiver fora da tela, volta pra dentro:
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        elif self.hitbox.x + self.hitbox.width > self.janela.width:
            self.hitbox.x = self.janela.width - self.hitbox.width

        # Atualiza o tempo de recarga
        self.cooldown_passado += self.janela.delta_time()
        if self.cooldown_passado >= self.cooldown_value and self.is_playing:
            self.cooldown_passado = 0
            # Atualiza os tiros
            if self.instrumento == 'piano' and self.playing_piano \
                    or self.instrumento == 'violao':
                if self.caixa_de_som and self.instrumento == 'violao':
                    self.shoot('caixa_de_som', Tiro.direcoes_string[self.caixa_de_som.direction],
                               self.caixa_de_som)

                elif self.teclado.key_pressed("down"):
                    self.shoot(self.instrumento, (0, -1), self.hitbox)
                elif self.last_direction == 'right':
                    self.shoot(self.instrumento, (1, 0), self.hitbox)
                elif self.last_direction == 'left':
                    self.shoot(self.instrumento, (-1, 0), self.hitbox)
                elif self.teclado.key_pressed("up"):
                    self.shoot(self.instrumento, (0, 1), self.hitbox)

        # Imunidade player
        if self.is_imune:
            self.imune_cronometro += self.janela.delta_time()
            if self.imune_cronometro > self.imune_duracao:
                self.is_imune = False
                self.imune_cronometro = 0
        else:
            self.imune_cronometro = 0

    def update_frame(self, sprite, ms: float = None):
        if ms:
            sprite.set_total_duration(ms)
        sprite.draw()
        sprite.set_position(self.hitbox.x, self.hitbox.y)
        sprite.update()

    def changecharacter(self, instrumento: str):
        if instrumento == 'piano':
            self.is_imune = True
            self.imune_cronometro = 0
        self.changing_character = True
        self.instrumento = instrumento
        self.sprites['changing'].set_curr_frame(0)
        self.sprite_atual = self.sprites[instrumento][f'still_{self.last_direction}']
        self.sprites['changing'].set_position(self.hitbox.x, self.hitbox.y)
        # resetando estados
        self.piano_charge = 0
        self.playing_piano = False
        self.can_move = True

    def shoot(self, tipo, direcao, sprite):
        Tiro(tipo, direcao, sprite)

    def draw_player(self):
        self.sprite_atual.set_position(self.hitbox.x, self.hitbox.y)
        # if not self.is_playing:
        #     if self.show_piano:
        #         self.sprites[f'piano_{self.last_direction}'].draw()
        #     else:
        #         self.update_frame(self.sprite_atual, 800)
        # else:
        #     self.update_frame(self.sprite_atual, 600)
        if self.show_piano:
            self.sprites['piano'][f'piano_{self.last_direction}'].draw()
        if self.is_playing:
            self.update_frame(self.sprite_atual, 600)
        else:
            self.update_frame(self.sprite_atual, 800)
        if self.changing_character and self.sprites['changing'].get_curr_frame() != 9:
            self.update_frame(self.sprites['changing'], 350)

    def check_camera(self, lista_gameobjects: list, mapa):
        self.v_camera = 200
        if self.hitbox.x + self.hitbox.width >= self.janela.width / 2 \
                and mapa.floor.x > mapa.boss_x_start:
            self.walkspeed = 0
            for gameobject in lista_gameobjects:
                if self.can_move:
                    if self.teclado.key_pressed("RIGHT"):
                        gameobject.x -= self.v_camera * self.janela.delta_time()
                    elif self.teclado.key_pressed("LEFT"):
                        if not mapa.floor.x > 0:
                            gameobject.x += self.v_camera * self.janela.delta_time()
                        else:
                            self.walkspeed = 200
        else:
            self.walkspeed = 200
            if mapa.floor.x < mapa.boss_x_start:
                mapa.floor.x = mapa.boss_x_start
                mapa.boss.spawn()

    def draw_hud(self):
        self.healthbar.draw()
        if self.instrumento == 'violao':
            self.hud_instrumento_violao.draw()
        elif self.instrumento == 'piano':
            self.hud_instrumento_piano.draw()
        self.hud_instrumento_frame.draw()
