from os import getcwd

from PPlay.sprite import Sprite
from PPlay.window import Window


class Tiro(Sprite):
    path_tiros = f'{getcwd()}\\Assets\\projeteis'

    tipo_tiros = ("violao", "flauta", "piano")

    tiros = {"violao": [],
             "flauta": [],
             "piano": []
             }
    velocidades = {"violao": 600,
                   "flauta": 600,
                   "piano": 600
                   }
    max_lifetimes = {"violao": 1.5,
                     "flauta": 1.5,
                     "piano": 1.5
                     }
    direcoes = {(1, 0): "right",
                (-1, 0): "left",
                (0, 1): "up",
                (0, -1): "down"
                }
    danos = {"violao": 50,
             "piano": 25,
             "flauta": 50
             }

    def __init__(self, tipo_tiro: str, direcao: tuple, player: Sprite):
        """
        Direção: uma tupla que indica o sinal da velocidade X e velocidade Y que o tiro terá. Idealmente -1, 0 ou 1.
        
        Tipo_tiro: até agora implementado somente o tipo violao
        """
        super().__init__(f'{self.path_tiros}\\{tipo_tiro}_{self.direcoes[direcao]}.png', 5)
        self.direcao = direcao
        self.tiros[tipo_tiro].append(self)
        if self.direcao[0] > 0:  # se for pra direita
            self.x = player.x + player.width  # na direita do player  (x)
            self.y = player.y + player.height / 2 - self.height / 2  # no meio do player (y)
        elif self.direcao[0] < 0:  # se for pra esquerda
            self.x = player.x - self.width  # na esquerda do player (x)
            self.y = player.y + player.height / 2 - self.height / 2  # no meio do player (y)
        elif self.direcao[1] > 0:  # se for pra cima
            self.x = player.x + player.width / 2 - self.width / 2  # no meio do player (x)
            self.y = player.y - self.height  # acima do player (y)
        elif self.direcao[1] < 0:  # se for pra cima
            self.x = player.x + player.width / 2 - self.width / 2  # no meio do player (x)
            self.y = player.y + player.height  # acima do player (y)

        self.x0 = self.x
        self.y0 = self.y

        self.time_lived = 0

    @classmethod
    def update_tiros(cls, janela: Window, lista_inimigos=None, player=None):
        for instrumento in cls.tipo_tiros:
            for inimigo in lista_inimigos:
                for i, tiro in enumerate(cls.tiros[instrumento]):
                    tiro.x += cls.velocidades[instrumento] * tiro.direcao[0] * janela.delta_time()
                    tiro.y -= cls.velocidades[instrumento] * tiro.direcao[1] * janela.delta_time()
                    tiro.time_lived += janela.delta_time()
                    colisao = tiro.collided_perfect(inimigo.sprite_atual)
                    if colisao:
                        inimigo.levar_dano(cls.danos[instrumento])
                    if tiro.time_lived >= cls.max_lifetimes[instrumento] or colisao:
                        cls.tiros[instrumento].pop(i)

    @classmethod
    def draw_tiros(cls, janela: Window):
        for tipo_tiro in cls.tipo_tiros:
            for i, tiro in enumerate(cls.tiros[tipo_tiro]):
                tiro.set_total_duration(400)
                tiro.draw()
                tiro.update()
