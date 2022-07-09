from PPlay.sprite import Sprite


class TiroTeleguiado(Sprite):
    caminho_sprite = f'Assets/projeteis/esfera_teleguiada_pequena.png'
    velocidade_max_pequena = 700
    maxlifetime_pequena = 16
    aceleracao = 1
    lista_pequenas = []

    def __init__(self, sprite_boss, player):
        super().__init__(self.caminho_sprite)
        self.x = sprite_boss.x + 115
        self.y = sprite_boss.y + 280

        self.player = player
        self.lista_pequenas.append(self)
        self.lifetime = 0
        self.velx = self.vely = 0
        self.last_speed = (0, 0)

    def seguir_player(self):
        deslocamento_x = (self.player.hitbox.x + self.player.hitbox.width / 2) - (self.x + self.width / 2)
        deslocamento_y = (self.player.hitbox.y + self.player.hitbox.height / 2) - (self.y + self.height / 2)
        soma_x_y = abs(deslocamento_y + deslocamento_x)
        ratio_x = deslocamento_x / soma_x_y
        ratio_y = deslocamento_y / soma_x_y
        if abs(self.velx) + abs(self.vely) > self.velocidade_max_pequena:
            self.velx = self.last_speed[0]
            self.vely = self.last_speed[1]
        self.velx += self.aceleracao * ratio_x * self.player.janela.delta_time()
        self.vely += self.aceleracao * ratio_y * self.player.janela.delta_time()

        self.last_speed = (self.velx, self.vely)

    def apply_motion(self):
        self.x += self.velx
        self.y += self.vely

    @classmethod
    def draw_tiros_teleguiados(cls):
        for tiro in cls.lista_pequenas:
            tiro.draw()

    @classmethod
    def update_tiros(cls):
        for i, tiro in enumerate(cls.lista_pequenas):
            if tiro.lifetime >= 6:
                cls.lista_pequenas.pop(i)
            else:
                tiro.seguir_player()
                tiro.apply_motion()
            tiro.lifetime += tiro.player.janela.delta_time()
