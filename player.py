from PPlay.sprite import *
from PPlay.window import *
from tiros import Tiro


class Player:
    # sprites visuais:
    Window(1365, 768)
    gravity = 4500
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

    def __init__(self, janela: Window, mapa, instrumento: str):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.walkspeed = 200
        self.instrumento = instrumento
        self.last_direction = 'right'
        self.cooldown_passado = 0
        self.hitbox = self.hitboxes['desmontado']
        self.ready = True  # se pode atirar (não está em cooldown)
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
        self.piano_charge_time, self.delay_piano_valor = 3, 0.15
        self.show_piano, self.playing_piano = False, False
        self.c_pressed_past = False
        self.changing_character = False
        self.imune = False
        self.imune_cooldown = 0

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

    def check_events(self) -> None:
        """Checa inputs do player e muda as variáveis de estado de acordo."""
        # checar se está tocando música
        self.last_position[0], self.last_position[1] = self.hitbox.x, self.hitbox.y
        self.is_playing = self.teclado.key_pressed("z")

        hitbox_anterior = self.hitbox
        self.hitbox = self.hitboxes['desmontado' if not self.playing_piano else 'montado']
        self.hitbox.set_position(hitbox_anterior.x, hitbox_anterior.y)

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
        # Se o piano estiver na tela, terá um tempo de recarga para o personagem tocar
        if self.show_piano is True:
            self.delay_piano_atual += self.janela.delta_time()
            if self.delay_piano_atual >= self.delay_piano_valor:
                self.delay_piano_atual = 0
                self.show_piano = False
                self.playing_piano = True

        # Enquanto estiver tocando piano, o player não poderá se mover
        if self.playing_piano:
            self.can_jump = False
            self.can_move = False
            self.sprite_atual = self.sprites[self.instrumento][f"playing_{self.last_direction}"]
        else:
            self.can_move = True

        # O jogador sai do piano
        if self.teclado.key_pressed('x'):
            self.playing_piano = False
        if self.c_pressed_past and not self.teclado.key_pressed('c'):
            self.changecharacter(self.proximo_instrumento[self.instrumento])
        self.c_pressed_past = self.teclado.key_pressed('c')
        # checar pulo 
        if self.teclado.key_pressed("UP"):
            if self.can_jump:
                self.jump()
        else:
            if self.can_jump is False and self.is_falling is False:
                self.vely *= 0.07
                self.is_falling = True
        # checar se está apertando pra direita
        if self.teclado.key_pressed("RIGHT"):
            self.last_direction = 'right'
            if self.can_move:
                self.hitbox.x += self.walkspeed * self.janela.delta_time()
                if not self.is_playing:
                    self.sprite_atual = self.sprites[self.instrumento]["walk_right"]
                else:
                    if self.instrumento == 'violao':
                        self.sprite_atual = self.sprites[self.instrumento][f'walk_attack_{self.last_direction}']

        # checar se está apertando pra esquerda
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

        # Atualiza o tempo de recarga
        self.cooldown_passado += self.janela.delta_time()
        if self.cooldown_passado >= self.cooldown_value and self.is_playing:
            self.cooldown_passado = 0
            # Atualiza os tiros
            if self.instrumento == 'piano' and self.playing_piano \
                    or self.instrumento == 'violao':
                if self.teclado.key_pressed("down"):
                    self.shoot(self.instrumento, (0, -1), self.hitbox)
                elif self.last_direction == 'right':
                    self.shoot(self.instrumento, (1, 0), self.hitbox)
                elif self.last_direction == 'left':
                    self.shoot(self.instrumento, (-1, 0), self.hitbox)
                elif self.teclado.key_pressed("up"):
                    self.shoot(self.instrumento, (0, 1), self.hitbox)

        # Imunidade player
        if self.imune:
            self.imune_cooldown += self.janela.delta_time()
            if self.imune_cooldown > 0.5:
                self.imune = False

    def update_frame(self, sprite, ms):
        sprite.set_total_duration(ms)
        sprite.draw()
        sprite.set_position(self.hitbox.x, self.hitbox.y)
        sprite.update()

    def changecharacter(self, instrumento: str):
        self.changing_character = True
        self.sprites['changing'].set_curr_frame(0)
        self.instrumento = instrumento
        self.sprites['changing'].set_position(self.hitbox.x, self.hitbox.y)
        # resetando estados
        self.piano_charge = 0
        self.playing_piano = False
        self.can_move = True

    def shoot(self, tipo, direcao, player):
        Tiro(tipo, direcao, player)

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
            self.sprites[self.instrumento][f'piano_{self.last_direction}'].draw()
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
