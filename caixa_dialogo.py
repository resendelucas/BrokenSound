from pygame.draw import rect as drawrect
from pygame.font import Font


class CaixaDialogo:
    black = (0, 0, 0)
    white = (255, 255, 255)
    fonte = Font('Assets/FreePixel.ttf', 20)
    intervalo_entre_letras = 0.05
    dialogos_ativos = []
    janela = None
    player = None
    width_letra = 9
    height_letra = 17

    def __init__(self, lista_linhas, sprite_falando, pos_vida: float=0, direcao: str = 'right'):
        self.pos_vida = pos_vida
        self.sprite_falando = sprite_falando
        self.direcao = direcao
        self.cronometro = 0
        self.lista_linhas_atual = []
        self.lista_linhas = lista_linhas
        self.total_caracteres = 0
        self.is_desativado = False
        self.is_finished = False
        self.cronometro_finished = 0
        for linha in lista_linhas:
            self.total_caracteres += len(linha)
        self.string_atual = ''
        self.x_base = self.sprite_falando.x + self.sprite_falando.width if direcao == 'right' else self.sprite_falando.x
        self.y_base = self.sprite_falando.y - self.sprite_falando.height * 8 / 10 - len(lista_linhas) * 1.2 * 4

    @classmethod
    def update_dialogos(cls):
        for dialogo in cls.dialogos_ativos:
            dialogo.update()

    @classmethod
    def draw_dialogos(cls):
        for dialogo in cls.dialogos_ativos:
            dialogo.draw()

    def desaparecer(self):
        if self in self.dialogos_ativos:
            self.dialogos_ativos.remove(self)
            self.is_desativado = True

    def aparecer(self, pos_vida=999999):
        self.pos_vida = pos_vida
        if self not in self.dialogos_ativos and not self.is_desativado:
            self.dialogos_ativos.append(self)

    def update(self):
        self.cronometro += self.janela.delta_time()
        self.x_base = self.sprite_falando.x + self.sprite_falando.width if self.direcao == 'right' \
            else self.sprite_falando.x
        self.y_base = self.sprite_falando.y - self.sprite_falando.height * 8 / 10 - len(self.lista_linhas) * 1.2 * 4
        i = int(self.cronometro // self.intervalo_entre_letras)
        self.lista_linhas_atual = []
        for j, linha in enumerate(self.lista_linhas):
            self.lista_linhas_atual.append('')
            if i > len(linha):
                self.lista_linhas_atual[j] = linha
                i -= len(linha)
            else:
                self.lista_linhas_atual[j] = linha[:i]
                i = 0
                break
        if self.lista_linhas == self.lista_linhas_atual:
            self.is_finished = True
            self.cronometro_finished += self.janela.delta_time()
            if self.cronometro_finished >= self.pos_vida:
                self.desaparecer()

    def draw(self):
        self.draw_fundo()
        for i, linha in enumerate(self.lista_linhas_atual):
            for j, char in enumerate(linha):
                self.janela.draw_text(char, self.x_base + 2 + self.width_letra * j,
                                      self.y_base + 2 + (1 * self.height_letra * i),
                                      color=self.black, font=self.fonte)

    def draw_fundo(self):
        from math import log, e
        if self.max_chars() <= 1:
            return
        variavel_logx5 = log(self.max_chars() * 5, e) / 3 + 0.6 * 1 / self.max_chars()
        variavel_logx3 = log(self.max_chars() * 3, e) + + 0.6 * 1 / self.max_chars()
        # retangulo preto mais largo horizontalmente
        drawrect(self.janela.screen, self.black, (self.x_base - 9, self.y_base - 3,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 18,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 6))
        # retangulo preto mais alto verticalmente
        drawrect(self.janela.screen, self.black, (self.x_base - 3, self.y_base - 9,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 6,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 18))
        # retangulo preto meio termo, das pontas
        drawrect(self.janela.screen, self.black, (self.x_base - 7, self.y_base - 7,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 14,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 14))
        # quadrado preto do rabinho 1
        drawrect(self.janela.screen, self.black, (self.x_base + variavel_logx5 * self.width_letra,
                                                  self.y_base + 9 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  variavel_logx3 * self.width_letra * 3 / 10,
                                                  variavel_logx3 * self.width_letra * 3 / 10))
        # quadrado preto do rabinho 2
        drawrect(self.janela.screen, self.black, (self.x_base + variavel_logx5 * self.width_letra - 5,
                                                  self.y_base + 15 + len(
                                                      self.lista_linhas) * self.height_letra * 1.2 + 5,
                                                  variavel_logx3 * self.width_letra * 3 / 10,
                                                  variavel_logx3 * self.width_letra * 2.5 / 10))
        # quadrado preto do rabinho 3
        drawrect(self.janela.screen, self.black, (self.x_base + variavel_logx5 * self.width_letra - 1.5,
                                                  self.y_base + 15 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  variavel_logx3 * self.width_letra * 3 / 10,
                                                  variavel_logx3 * self.width_letra * 3 / 10))

        # quadrado branco do rabinho 1
        drawrect(self.janela.screen, self.white, (self.x_base + variavel_logx5 * self.width_letra + 2,
                                                  self.y_base + 9 + len(
                                                      self.lista_linhas) * self.height_letra * 1.2 - 2,
                                                  variavel_logx3 * self.width_letra * 3 / 10 - 4,
                                                  variavel_logx3 * self.width_letra * 3 / 10))
        # quadrado branco do rabinho 2
        drawrect(self.janela.screen, self.white, (self.x_base + variavel_logx5 * self.width_letra - 3,
                                                  self.y_base + 15 + len(
                                                      self.lista_linhas) * self.height_letra * 1.2 + 5,
                                                  variavel_logx3 * self.width_letra * 3 / 10 - 4,
                                                  variavel_logx3 * self.width_letra * 3 / 10 - 4))
        # quadrado branco do rabinho 3
        drawrect(self.janela.screen, self.white, (self.x_base + variavel_logx5 * self.width_letra,
                                                  self.y_base + 14 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  variavel_logx3 * self.width_letra * 2.3 / 10 - 2,
                                                  variavel_logx3 * self.width_letra * 3 / 10 - 2))
        # retangulo branco mais largo horizontalmente
        drawrect(self.janela.screen, self.white, (self.x_base - 7, self.y_base - 3,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 14,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 6))
        # retangulo branco mais alto verticalmente
        drawrect(self.janela.screen, self.white, (self.x_base - 3, self.y_base - 7,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 6,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 14))
        # retangulo branco meio termo, das pontas
        drawrect(self.janela.screen, self.white, (self.x_base - 5, self.y_base - 5,
                                                  (self.max_chars() + 1) * self.width_letra * 1.00 + 10,
                                                  len(self.lista_linhas) * self.height_letra * 1.2 + 10))
        # retangulo do texto
        drawrect(self.janela.screen, self.white,
                 (self.x_base, self.y_base,
                  (self.max_chars() + 1) * self.width_letra * 1.00,
                  len(self.lista_linhas) * self.height_letra * 1.2))

    def max_chars(self):
        maior = 0
        for linha in self.lista_linhas_atual:
            if len(linha) > maior:
                maior = len(linha)
        return maior

    @classmethod
    def set_player(cls, player):
        cls.player = player
        cls.janela = player.janela
