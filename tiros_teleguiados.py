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
        soma_x_y = abs(deslocamento_y) + abs(deslocamento_x)
        ratio_x = deslocamento_x / soma_x_y
        ratio_y = deslocamento_y / soma_x_y
        if abs(ratio_x) + abs(ratio_y) > 1.1:
            print(f'ratios x y:{ratio_x:.2f}, {ratio_y:.2f}')
            print(f'meio do player: {self.player.hitbox.x + self.player.hitbox.width / 2:.2f},{self.player.hitbox.y + self.player.hitbox.height / 2} ')
            print(f'meio do tiro: {self.x + self.width / 2:.2f}, {self.y + self.height / 2}')


        self.velx += self.aceleracao * ratio_x * self.player.janela.delta_time()
        # print("somando ao vel x:",self.aceleracao * ratio_x * self.player.janela.delta_time())
        self.vely += self.aceleracao * ratio_y * self.player.janela.delta_time()
        # print("somando ao vely:", self.aceleracao * ratio_y * self.player.janela.delta_time())
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
