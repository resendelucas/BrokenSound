from PPlayTeste.gameimage import *
from PPlayTeste.sound import *
from PPlayTeste.sprite import *

class Player:
    def __init__(self, janela, mapa):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.vPlayer = 200
        self.walking_right, self.walking_left, self.is_playing = False, False, False
        self.player_walk_right = Sprite("Assets/character/walking/walk_right.png",6)
        self.player_walk_left = Sprite("Assets/character/walking/walk_left.png",6)
        self.player_walk_attack_right = Sprite("Assets/character/walking/walk_attack_right.png",6)
        self.player_walk_attack_left = Sprite("Assets/character/walking/walk_attack_left.png",6)
        self.player_playing = Sprite("Assets/character/parado/attack_right.png",4)
        self.player_still = Sprite("Assets/character/parado/player_2.png")
        self.player_x, self.player_y = 688, 608

    def check_events(self) -> None:
        """Checa inputs do player e muda as variáveis de estado de acordo."""
        if self.teclado.key_pressed("RIGHT"):

            self.player_x += self.vPlayer * self.janela.delta_time()
            self.walking_right = True
            self.walking_left = False
            if self.teclado.key_pressed("z"):
                self.is_playing = True
            else:
                self.is_playing = False

        elif self.teclado.key_pressed("LEFT"):

            self.player_x -= self.vPlayer * self.janela.delta_time()
            self.walking_left = True
            self.walking_right = False
            if self.teclado.key_pressed("z"):
                self.is_playing = True
            else:
                self.is_playing = False

        elif self.teclado.key_pressed("z"):

            self.walking_left = False
            self.walking_right = False
            self.is_playing = True

        else:

            self.walking_left = False
            self.walking_right = False
            self.is_playing = False

        
        # Atualiza posição do jogador
        self.player_y = 608 - self.player_still.height
        
    def update_pos(self, sprite, x, y):
        sprite.x = x
        sprite.y = y

    def update_frame(self, sprite, ms):
        sprite.set_total_duration(ms)
        sprite.draw()
        sprite.update()

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
            self.update_pos(self.player_playing, self.player_x, self.player_y)
            self.update_frame(self.player_playing, 300)

        else:
            self.update_pos(self.player_still, self.player_x, self.player_y)
            self.player_still.draw()
