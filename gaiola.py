from PPlay.sprite import Sprite


class Gaiola(Sprite):
    caminho_sprite = 'Assets/boss_piano/gaiola/gaiola.png'
    cronometro_cair = 0
    cronometro_cair_value = 2.5
    gravidade = 900

    @classmethod
    def reset_class(cls):
        cls.caminho_sprite = 'Assets/boss_piano/gaiola/gaiola.png'
        cls.cronometro_cair = 0
        cls.cronometro_cair_value = 2.5
        cls.gravidade = 900

    def __init__(self, player):
        super().__init__(self.caminho_sprite)
        self.player = player
        self.janela = self.player.janela
        self.set_position(self.player.hitbox.x, self.player.hitbox.y - self.height * 2.5)
        self.is_flutuando = True
        self.vely = self.velx = 0
        self.mini_game = None
        self.is_player_preso = False

    def set_minigame(self, minigame):
        self.mini_game = minigame

    def update(self):
        self.cronometro_cair += self.janela.delta_time()
        if self.is_player_preso is True:
            if self.player.hitbox.x <= self.x:
                self.player.hitbox.x = self.x + 1
            elif self.player.hitbox.x + self.player.hitbox.width >= self.x + self.width:
                self.player.hitbox.x = self.x + self.width - 1 - self.player.hitbox.width

            if self.player.hitbox.y < self.y + 14:
                self.player.hitbox.y = self.y + 14
                self.player.vely = 0
        else:
            self.x = self.player.hitbox.x + self.player.hitbox.width/2 - self.width/2
        self.cronometro_cair += self.janela.delta_time()
        if self.cronometro_cair >= self.cronometro_cair_value:
            self.is_player_preso = True
            self.is_flutuando = False
            if self.y < 676 - self.height:
                self.vely -= self.gravidade * self.janela.delta_time()
                self.y -= self.vely * self.janela.delta_time()
            else:
                self.y = 676 - self.height
                # nesse caso, o minigame das teclas é executado
                self.mini_game.update_teclas()
                pass
