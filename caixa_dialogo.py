from pygame.draw import rect as drawrect
from pygame.font import Font


class CaixaDialogo:
    black = (0, 0, 0)
    white = (255, 255, 255)
    fonte = Font('Assets/FreePixel.ttf', 20)
    intervalo_entre_letras = 0.05
    janela = None
    player = None
    width_letra = 9
    height_letra = 17

    def __init__(self, lista_linhas, sprite_falando, direcao: str = 'right'):
        self.sprite_falando = sprite_falando
        self.cronometro = 0
        self.lista_linhas_atual = []
        self.lista_linhas = lista_linhas
        self.total_caracteres = 0
        for linha in lista_linhas:
            self.total_caracteres += len(linha)
        self.string_atual = ''
        self.x_base = self.sprite_falando.x + self.sprite_falando.width if direcao == 'right' else self.sprite_falando.x
        self.y_base = self.sprite_falando.y - self.sprite_falando.height * 8 / 10 - len(lista_linhas) * 1.2 * 4

    def update(self):
        self.cronometro += self.janela.delta_time()
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
        drawrect(self.janela.screen, self.black, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra,
                                                  self.y_base + 9 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  log(self.max_chars(), e) * self.width_letra * 3/10,
                                                  log(self.max_chars(), e) * self.width_letra * 3/10))
        # quadrado preto do rabinho 2
        drawrect(self.janela.screen, self.black, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra - 5,
                                                  self.y_base + 15 + len(self.lista_linhas) * self.height_letra * 1.2 + 5,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10,
                                                  log(self.max_chars(), e) * self.width_letra * 2.5 / 10))
        # quadrado preto do rabinho 3
        drawrect(self.janela.screen, self.black, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra - 1.5,
                                                  self.y_base + 15 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10))

        # quadrado branco do rabinho 1
        drawrect(self.janela.screen, self.white, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra + 2,
                                                  self.y_base + 9 + len(self.lista_linhas) * self.height_letra * 1.2 - 2,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10 - 4,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10))
        # quadrado branco do rabinho 2
        drawrect(self.janela.screen, self.white, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra - 3,
                                                  self.y_base + 15 + len(
                                                      self.lista_linhas) * self.height_letra * 1.2 + 5,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10 - 4,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10 - 4))
        # quadrado branco do rabinho 3
        drawrect(self.janela.screen, self.white, (self.x_base + log(self.max_chars()*5, e)/5 * self.width_letra,
                                                  self.y_base + 14 + len(self.lista_linhas) * self.height_letra * 1.2,
                                                  log(self.max_chars(), e) * self.width_letra * 2.3 / 10 - 2,
                                                  log(self.max_chars(), e) * self.width_letra * 3 / 10 - 2))
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
