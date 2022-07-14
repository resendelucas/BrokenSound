from os import getcwd

from PPlay.sprite import Sprite
from PPlay.window import Window


class Tiro(Sprite):
    path_tiros = f'{getcwd()}\\Assets\\projeteis'

    tiros = {"violao": [],
             "caixa_de_som": [],
             "flauta": [],
             "piano": []
             }
    velocidades = {"violao": 600,
                   "caixa_de_som": 300,
                   "flauta": 600,
                   "piano": 600
                   }
    max_lifetimes = {"violao": 1.5,
                     "caixa_de_som": 3,
                     "flauta": 1.5,
                     "piano": 1.5
                     }
    direcoes = {(1, 0): "right",
                (-1, 0): "left",
                (0, 1): "up",
                (0, -1): "down"
                }
    direcoes_string = {"right": (1, 0),
                       "left": (-1, 0),
                       "up": (0, 1),
                       "down": (0, -1)
                       }
    danos = {"violao": 50,
             "caixa_de_som": 35,
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
        for instrumento, lista_tiros in cls.tiros.items():
            for i, tiro in enumerate(lista_tiros):
                if tiro.time_lived >= cls.max_lifetimes[instrumento]:
                    cls.tiros[instrumento].pop(i)
                    break
                tiro.x += cls.velocidades[instrumento] * tiro.direcao[0] * janela.delta_time()
                tiro.y -= cls.velocidades[instrumento] * tiro.direcao[1] * janela.delta_time()
                tiro.time_lived += janela.delta_time()
                for inimigo in lista_inimigos:
                    if not inimigo.is_dying and not inimigo.is_imune:
                        if tiro.collided_perfect(inimigo.sprite_atual):
                            inimigo.levar_dano(cls.danos[instrumento])
                            cls.tiros[instrumento].pop(i)
                            break

    @classmethod
    def draw_tiros(cls, janela: Window):
        for lista_tiros in cls.tiros.values():
            for i, tiro in enumerate(lista_tiros):
                tiro.set_total_duration(400)
                tiro.draw()
                tiro.update()

    @classmethod
    def get_every_tiro(cls):
        lista = []
        for lista_tiros in cls.tiros.values():
            lista += lista_tiros
        return lista
