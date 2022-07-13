from PPlay.sprite import Sprite


class Gaiola(Sprite):
    caminho_sprite = 'Assets/boss_piano/gaiola.png'
    cronometro_cair = 0
    cronometro_cair_value = 2.5
    gravidade = 4500

    def __init__(self, player):
        super().__init__(self.caminho_sprite)
        self.player = player
        self.janela = self.player.janela
        self.set_position(self.player.hitbox.x, self.player.hitobx.y)
        self.is_flutuando = True
        self.vely = self.velx = 0

    def update(self):
        if not self.is_flutuando:
            if self.player.hitbox.x <= self.x:
                self.player.hitbox.x = self.x + 1
            elif self.player.hitbox.x + self.player.hitbox.width >= self.x + self.width:
                self.player.hitbox.x = self.x + self.width - 1
            return
        self.x = self.player.hitbox.x + self.player.hitbox.width/2 - self.width/2
        self.y -= self.vely
        self.cronometro_cair += self.janela.delta_time()
        if self.cronometro_cair >= self.cronometro_cair_value:
            if self.y < 676 - self.height:
                self.vely -= self.gravidade
            else:
                # nesse caso, o minigame das teclas é executado
                pass
