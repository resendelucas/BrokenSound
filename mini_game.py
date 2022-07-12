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
        self.tam = 84
        self.total = 0
        self.key_missed = 0
        self.background.set_position(self.janela.width / 2 - self.background.width / 2, 0)
        self.sprites['button-green'].set_position(511+self.tam, 355)
        self.sprites['button-red'].set_position(556+self.tam, 355)
        self.sprites['button-yellow'].set_position(602+self.tam, 355)
        self.sprites['button-blue'].set_position(646+self.tam, 355)
        self.get_notes(song1)

    def config(self):
        # Falta mover o player e o boss para os cantos da tela
        self.player.can_move = False

    def check_events(self):
        for key, values in self.notes.items():
            if values:
                note = values[0]
            # Faz as bolinhas descerem
                note.y += self.vel_notes * self.janela.delta_time()

                # Verifica se colidiu e o player apertou a tecla certa
                if key == 'green':
                    if self.teclado.key_pressed("q") and not self.player.key_pressed_past["q"]:
                        if note.collided(self.sprites['button-green']):
                            values.remove(note)
                            self.boss.levar_dano(self.boss.max_health * 0.2 / self.total)
                        else:
                            values.remove(note)
                            self.player.levar_dano(0.25)
                if key == 'red':
                    if self.teclado.key_pressed("w") and not self.player.key_pressed_past["w"]:
                        if note.collided(self.sprites['button-red']):
                            values.remove(note)
                            self.boss.levar_dano(self.boss.max_health * 0.2 / self.total)
                        else:
                            values.remove(note)
                            self.player.levar_dano(0.25)
                if key == 'yellow':
                    if self.teclado.key_pressed("e") and not self.player.key_pressed_past["e"]:
                        if note.collided(self.sprites['button-yellow']):
                            values.remove(note)
                            self.boss.levar_dano(self.boss.max_health * 0.2 / self.total)
                        else:
                            values.remove(note)
                            self.player.levar_dano(0.25)
                if key == 'blue':
                    if self.teclado.key_pressed("r") and not self.player.key_pressed_past["r"]:
                        if note.collided(self.sprites['button-blue']):
                            values.remove(note)
                            self.boss.levar_dano(self.boss.max_health * 0.2 / self.total)
                        else:
                            values.remove(note)
                            self.player.levar_dano(0.25)
                
                if note.y > self.sprites['button-green'].y + self.sprites['button-green'].height + 5:
                    self.player.levar_dano(0.5)
                    self.key_missed += 1
                    values.remove(note)

        if (len(self.notes['green']) + len(self.notes['yellow']) + \
            len(self.notes['blue']) + len(self.notes['red'])) == 0:
            self.boss.is_mini_game_on = False
            self.boss.is_mini_game_done = True
            
        self.player.key_pressed_past["q"] = self.teclado.key_pressed("q")
        self.player.key_pressed_past["w"] = self.teclado.key_pressed("w")
        self.player.key_pressed_past["e"] = self.teclado.key_pressed("e")
        self.player.key_pressed_past["r"] = self.teclado.key_pressed("r")

    def draw_elements(self):
        self.background.draw()
        self.sprites['button-green'].draw()
        self.sprites['button-red'].draw()
        self.sprites['button-yellow'].draw()
        self.sprites['button-blue'].draw()
        for key, values in self.notes.items():
            for note in values:
                note.draw()

    def get_notes(self, song):
        padding_y = -20
        for notes in song:
            for col, note in enumerate(notes):
                if note != ' ':
                    if col == 0:
                        green = Sprite("Assets/mini-game/green.png")
                        green.set_position(516+self.tam, padding_y)
                        self.notes['green'].append(green)
                    if col == 1:
                        red = Sprite("Assets/mini-game/red.png")
                        red.set_position(561+self.tam, padding_y)
                        self.notes['red'].append(red)
                    if col == 2:
                        yellow = Sprite("Assets/mini-game/yellow.png")
                        yellow.set_position(607+self.tam, padding_y)
                        self.notes['yellow'].append(yellow)
                    if col == 3:
                        blue = Sprite("Assets/mini-game/blue.png")
                        blue.set_position(651+self.tam, padding_y)
                        self.notes['blue'].append(blue)
            padding_y -= 50
        self.total = len(self.notes['green']) + len(self.notes['yellow']) + \
            len(self.notes['blue']) + len(self.notes['red'])
