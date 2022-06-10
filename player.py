from PPlayTeste.gameimage import *
from PPlayTeste.window import *


class Player():
    def __init__(self, janela, mapa):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.vPlayer = 200
        self.walk_right, self.walk_left, self.is_playing = False, False, False
        self.walk_count, self.playing_count = 0, 0
        self.player_x, self.player_y = 688, 608
        self.player_walk_right = []
        self.player_walk_left = []
        self.player_playing = []
        self.get_player()

    def get_player(self):
        self.player_still = GameImage("Assets/character/parado/player_0.png")
        
        walk_right = 'Assets/character/walking/big_walk'
        walk_left = 'Assets/character/walking/big_walk_back'
        playing = 'Assets/character/parado/player_'

        for i in range(6):
            self.player_walk_right.append(GameImage(f"{walk_right}{i}.png"))
            self.player_walk_left.append(GameImage(f"{walk_left}{i}.png"))
            if i < 4:
                self.player_playing.append(GameImage(f"{playing}{i}.png"))

    def check_events(self):

        if self.teclado.key_pressed("RIGHT"):

            self.player_x +=self.vPlayer * self.janela.delta_time()
            self.walk_right = True
            self.walk_left = False
            self.is_playing = False

        elif self.teclado.key_pressed("LEFT"):

            self.player_x -=self.vPlayer * self.janela.delta_time()
            self.walk_left = True
            self.walk_right = False
            self.is_playing = False

        elif self.teclado.key_pressed("z"):
            self.playing_count += 1
            self.walk_left = False
            self.walk_right = False
            self.is_playing = True
            self.walk_count = 0
        
        else:
            self.walk_left = False
            self.walk_right = False
            self.is_playing = False
            self.walk_count = 0
            self.playing_count = 0

        if self.walk_left:
            self.walk_count += 1

        if self.walk_right:
            self.walk_count += 1

        if self.walk_count >= 45*6:
            self.walk_count = 0

        if self.playing_count >= 36*4:
            self.playing_count = 0

        self.player_y = 608 - self.player_still.height
        # Atualiza posição do jogador
        for player_left in self.player_walk_left:
            player_left.x = self.player_x
            player_left.y = self.player_y

        for player_right in self.player_walk_right:
            player_right.x = self.player_x
            player_right.y = self.player_y

        for playing in self.player_playing:
            playing.x = self.player_x
            playing.y = self.player_y

        self.player_still.x = self.player_x
        self.player_still.y = self.player_y

    def draw_player(self):

        if self.walk_left:
            self.player_walk_left[self.walk_count//45].draw()
            
        elif self.walk_right:
            self.player_walk_right[self.walk_count//45].draw()

        elif self.is_playing:
            self.player_playing[self.playing_count//36].draw()
        
        else:
            self.player_still.draw()
    
