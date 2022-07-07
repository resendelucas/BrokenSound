from PPlay.sprite import *
from PPlay.window import *
from tiros import Tiro


class Player:
    # sprites visuais:
    Window(800,700)
    instrumento = 'violao'
    sprites = {
            "walk_right": Sprite(f"Assets/character/{instrumento}/walking/walk_right.png", 6),
            'walk_left' : Sprite(f"Assets/character/{instrumento}/walking/walk_left.png", 6),
            'walk_attack_right' : Sprite(f"Assets/character/violao/walking/walk_attack_right.png", 6),
            'walk_attack_left' : Sprite(f"Assets/character/violao/walking/walk_attack_left.png", 6),
            'playing_right' : Sprite(f"Assets/character/{instrumento}/parado/attack_right.png", 4),
            'playing_left' : Sprite(f"Assets/character/{instrumento}/parado/attack_left.png", 4),
            'still_right' : Sprite(f"Assets/character/{instrumento}/parado/player_still_right.png"),
            'still_left' : Sprite(f"Assets/character/{instrumento}/parado/player_still_left.png")
    }
    if instrumento == 'piano':
        sprites["charging_left"] = Sprite(f"Assets/character/piano/parado/charging_left.png", 6)
        sprites["charging_right"] = Sprite(f"Assets/character/piano/parado/charging_right.png", 6)
        sprites["playing_left"] = Sprite(f"Assets/character/piano/parado/attack_left.png", 2)
        sprites["playing_right"] = Sprite(f"Assets/character/piano/parado/attack_right.png", 2)
        sprites["piano_left"] = Sprite(f"Assets/character/piano/piano_left.png")
        sprites["piano_right"] = Sprite(f"Assets/character/piano/piano_right.png")
        sprites['still_left'] = Sprite(f"Assets/character/piano/parado/player_still_left.png",4)
        sprites['still_right'] = Sprite(f"Assets/character/piano/parado/player_still_right.png",4)
        del sprites["walk_attack_right"]
        del sprites["walk_attack_left"]
    # sprites usadas no backend:
    hitbox = Sprite("Assets/character/player_hitbox.png")  # sprite deve ser sempre atualizada
    sprite_atual = sprites["walk_right"]
    # cooldown tiros:  
    cooldown = 0
    gravity = 4500

    def __init__(self, janela, mapa):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.walkspeed = 200
        self.last_direction = 'right'
        self.delay = 0
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
        self.charge_piano = self.delay_piano = 1
        self.show_piano, self.playing_piano = False, False

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


        if self.is_playing:
            # Se for piano, o personagem carrega o piano na tela
            if self.instrumento == 'piano':
                self.can_move = False
                self.sprite_atual = self.sprites[f'charging_{self.last_direction}']
                self.charge_piano += 1
                if self.charge_piano >= 800 and not self.show_piano:
                    self.show_piano = True
                    self.sprites["piano_left"].set_position(self.hitbox.x - 110, self.hitbox.y)
                    self.sprites["piano_right"].set_position(self.hitbox.x + 70, self.hitbox.y)
                    self.charge_piano = 0
                    self.is_playing = False
            else:
                self.can_move = True
                self.sprite_atual = self.sprites[f'playing_{self.last_direction}']
        
        # Se o piano estiver na tela, terá um tempo de recarga para o personagem tocar
        if self.show_piano:
            self.delay_piano += 1
            if self.delay_piano >= 100:
                self.sprite_atual = self.sprites[f"playing_{self.last_direction}"]
                self.delay_piano = 0
                self.show_piano = False
                self.playing_piano = True

        # Enquanto estiver tocando piano, o player não poderá se mover
        if self.playing_piano:
            self.can_jump = False
            self.can_move = False
        else:
            self.can_move = True

        # O jogador sai do piano
        if self.teclado.key_pressed('x'):
            self.playing_piano = False

        # checar pulo 
        if self.teclado.key_pressed("UP"):
            if self.can_jump:
                self.jump()
        else:
            if self.can_jump is False and self.is_falling is False:
                self.vely *= 0.07
                self.is_falling = True
        # checar se está apertando pra direita
        if self.teclado.key_pressed("RIGHT") and self.can_move:
            self.last_direction = 'right'
            self.hitbox.x += self.walkspeed * self.janela.delta_time()
            if not self.is_playing:
                self.sprite_atual = self.sprites["walk_right"]
            else:
                if self.instrumento == 'violao':
                    self.sprite_atual = self.sprites[f'walk_attack_{self.last_direction}']

        # checar se está apertando pra esquerda
        elif self.teclado.key_pressed("LEFT") and self.can_move:
            self.last_direction = 'left'
            self.hitbox.x -= self.walkspeed * self.janela.delta_time()
            if not self.is_playing:
                self.sprite_atual = self.sprites["walk_left"]
            else:
                if self.instrumento == 'violao':
                    self.sprite_atual = self.sprites[f'walk_attack_{self.last_direction}']
        else:  # se nenhuma tecla de movimento estiver sendo apertada
            if not self.is_playing and not self.playing_piano:
                self.sprite_atual = self.sprites[f'still_{self.last_direction}']
            else:
                if self.instrumento == 'violao':
                    self.sprite_atual = self.sprites[f'playing_{self.last_direction}']


            


        # Atualiza o tempo de recarga
        self.delay += self.janela.delta_time()
        if self.delay >= self.cooldown:
            self.delay = 0
            # Atualiza os tiros
            # if self.is_playing:
            #     if self.teclado.key_pressed("up"):
            #         self.shoot(self.instrumento, (0, 1), self.hitbox)
            #     elif self.teclado.key_pressed("down"):
            #         self.shoot(self.instrumento, (0, -1), self.hitbox)
            #     elif self.last_direction == 'right':
            #         self.shoot(self.instrumento, (1, 0), self.hitbox)
            #     elif self.last_direction == 'left':
            #         self.shoot(self.instrumento, (-1, 0), self.hitbox)

    @staticmethod
    def update_frame(sprite, ms):
        sprite.set_total_duration(ms)
        sprite.draw()
        sprite.update()

    @staticmethod
    def shoot(tipo, direcao, player):
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
            self.sprites[f'piano_{self.last_direction}'].draw()
        if self.is_playing:
            self.update_frame(self.sprite_atual, 600)
        else:
            self.update_frame(self.sprite_atual, 800)


    def check_camera(self, lista_gameobjects: list):
        self.v_camera = 200
        if self.hitbox.x + self.hitbox.width >= self.janela.width/2:
            self.walkspeed = 0
            for gameobject in lista_gameobjects:
                if self.can_move:
                    if self.teclado.key_pressed("RIGHT"):
                        gameobject.x -= self.v_camera * self.janela.delta_time()
                    if self.teclado.key_pressed("LEFT"):
                        gameobject.x += self.v_camera * self.janela.delta_time()
        else:
            self.walkspeed = 200