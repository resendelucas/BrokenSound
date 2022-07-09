from PPlay.sprite import *
from mini_songs import song1


class MiniGame:
    sprites = {
        'button-green': Sprite("Assets/mini-game/q-green.png"),
        'button-red': Sprite("Assets/mini-game/w-red.png"),
        'button-yellow': Sprite("Assets/mini-game/e-yellow.png"),
        'button-blue': Sprite("Assets/mini-game/r-blue.png")
    }
    notes = {
        'green': [],
        'red': [],
        'yellow': [],
        'blue': [],
    }
    background = Sprite("Assets/mini-game/linhas.png")

    def __init__(self, janela, player, boss):
        self.janela = janela
        self.player = player
        self.boss = boss
        self.teclado = janela.get_keyboard()
        self.vel_notes = 150
        self.background.set_position(self.janela.width / 2 - self.background.width / 2, 0)
        self.sprites['button-green'].set_position(511, 355)
        self.sprites['button-red'].set_position(556, 355)
        self.sprites['button-yellow'].set_position(602, 355)
        self.sprites['button-blue'].set_position(646, 355)
        self.get_notes()

    def config(self):
        # Falta mover o player e o boss para os cantos da tela
        self.player.can_move = False

    def check_events(self):
        for key, values in self.notes.items():
            for note in values:
                # Faz as bolinhas descerem
                note.y += self.vel_notes * self.janela.delta_time()

                # Verifica se colidiu e o player apertou a tecla certa
                if key == 'green':
                    if self.teclado.key_pressed("q") and note.collided(self.sprites['button-green']):
                        values.remove(note)
                if key == 'red':
                    if self.teclado.key_pressed("w") and note.collided(self.sprites['button-red']):
                        values.remove(note)
                if key == 'yellow':
                    if self.teclado.key_pressed("e") and note.collided(self.sprites['button-yellow']):
                        values.remove(note)
                if key == 'blue':
                    if self.teclado.key_pressed("r") and note.collided(self.sprites['button-blue']):
                        values.remove(note)

                # remove a bolinha se passar da tela
                if note.y > self.janela.height:
                    values.remove(note)

    def draw_elements(self):
        self.background.draw()
        self.sprites['button-green'].draw()
        self.sprites['button-red'].draw()
        self.sprites['button-yellow'].draw()
        self.sprites['button-blue'].draw()
        for key, values in self.notes.items():
            for note in values:
                note.draw()

    def get_notes(self):
        padding_y = -20
        for notes in song1:
            for col, note in enumerate(notes):
                if note != ' ':
                    if col == 0:
                        green = Sprite("Assets/mini-game/green.png")
                        green.set_position(516, padding_y)
                        self.notes['green'].append(green)
                    if col == 1:
                        red = Sprite("Assets/mini-game/red.png")
                        red.set_position(561, padding_y)
                        self.notes['red'].append(red)
                    if col == 2:
                        yellow = Sprite("Assets/mini-game/yellow.png")
                        yellow.set_position(607, padding_y)
                        self.notes['yellow'].append(yellow)
                    if col == 3:
                        blue = Sprite("Assets/mini-game/blue.png")
                        blue.set_position(651, padding_y)
                        self.notes['blue'].append(blue)
            padding_y -= 50
