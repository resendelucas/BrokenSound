from PPlay.gameimage import *
from PPlay.sound import *
from PPlay.sprite import *
from tiros import Tiro

class Player:
    def __init__(self, janela, mapa):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.vPlayer = 200
        self.walking_right, self.walking_left, self.is_playing = False, False, False
        self.instrumento = 'violao'
        self.last_direction = 'right'
        self.cooldown, self.delay = 0.7, 0
        self.ready = True
        self.player_hitbox = Sprite("Assets/character/player_hitbox.png")
        self.player_walk_right = Sprite("Assets/character/walking/walk_right.png",6)
        self.player_walk_left = Sprite("Assets/character/walking/walk_left.png",6)
        self.player_walk_attack_right = Sprite("Assets/character/walking/walk_attack_right.png",6)
        self.player_walk_attack_left = Sprite("Assets/character/walking/walk_attack_left.png",6)
        self.player_playing_right = Sprite("Assets/character/parado/attack_right.png",4)
        self.player_playing_left = Sprite("Assets/character/parado/attack_left.png",4)
        self.player_still_right = Sprite("Assets/character/walking/big_walk0.png")
        self.player_still_left = Sprite("Assets/character/walking/big_walk_back0.png")
        self.player_x, self.player_y = 688, 608
        
    def check_events(self) -> None:
        """Checa inputs do player e muda as variáveis de estado de acordo."""
        # checar se está tocando música
        if self.teclado.key_pressed("z"):
            self.is_playing = True
        else:
            self.is_playing = False
        
        # checar se está apertando pra direita
        if self.teclado.key_pressed("RIGHT"):

            self.player_x += self.vPlayer * self.janela.delta_time()
            self.walking_right = True
            self.walking_left = False
            self.last_direction = 'right'
            
        # checar se está apertando pra esquerda
        elif self.teclado.key_pressed("LEFT"):

            self.player_x -= self.vPlayer * self.janela.delta_time()
            self.walking_left = True
            self.walking_right = False
            self.last_direction = 'left'
            

        elif self.teclado.key_pressed("z"):

            self.walking_left = False
            self.walking_right = False
            self.is_playing = True
            
        else:

            self.walking_left = False
            self.walking_right = False
            self.is_playing = False

        
        # Atualiza posição do jogador
        self.player_y = 608 - self.player_still_right.height
        self.update_pos(self.player_hitbox, self.player_x, self.player_y)

        # Atualiza o tempo de recarga
        self.delay += self.janela.delta_time()
        if self.delay >= self.cooldown:
            self.ready = True
            self.delay = 0
        else:
            self.ready = False
        
        # Atualiza os tiros

        if self.is_playing and self.ready:
            if self.teclado.key_pressed("up"):
                self.shoot(self.instrumento,(0,1),self.player_hitbox)
            elif self.teclado.key_pressed("down"):
                self.shoot(self.instrumento,(0,-1),self.player_hitbox)
            elif self.last_direction == 'right':
                self.shoot(self.instrumento,(1,0),self.player_hitbox)
            elif self.last_direction == 'left':
                self.shoot(self.instrumento,(-1,0),self.player_hitbox)
                
        
    def update_pos(self, sprite, x, y):
        sprite.x = x
        sprite.y = y

    def update_frame(self, sprite, ms):
        sprite.set_total_duration(ms)
        sprite.draw()
        sprite.update()

    def shoot(self, tipo, direcao, player):
        Tiro(tipo, direcao, player)

    def draw_player(self):
        if self.walking_left:

            if self.is_playing:
                self.update_pos(self.player_walk_attack_left, self.player_x, self.player_y)
                self.update_frame(self.player_walk_attack_left, 800)
            else:
                self.update_pos(self.player_walk_left, self.player_x, self.player_y)
                self.update_frame(self.player_walk_left, 800)
        
        elif self.walking_right:
            if self.is_playing:
                self.update_pos(self.player_walk_attack_right, self.player_x, self.player_y)
                self.update_frame(self.player_walk_attack_right, 800)
            else:
                self.update_pos(self.player_walk_right, self.player_x, self.player_y)
                self.update_frame(self.player_walk_right, 800)


        elif self.is_playing:
            if self.last_direction == 'right':
                self.update_pos(self.player_playing_right, self.player_x, self.player_y)
                self.update_frame(self.player_playing_right, 300)
            if self.last_direction == 'left':
                self.update_pos(self.player_playing_left, self.player_x, self.player_y)
                self.update_frame(self.player_playing_left, 300)

        else:
            if self.last_direction == 'right':
                self.update_pos(self.player_still_right, self.player_x, self.player_y)
                self.player_still_right.draw()
            if self.last_direction == 'left':
                self.update_pos(self.player_still_left, self.player_x, self.player_y)
                self.player_still_left.draw()
