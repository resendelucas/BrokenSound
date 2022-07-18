from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window


class Menu:
    fases = ('tutorial', 'esqueleto', 'bruxa vermelha')

    def __init__(self, janela: Window):
        self.janela = janela
        self.mouse = janela.get_mouse()
        self.keyboard = janela.get_keyboard()
        self.click = False
        self.click_cooldown = 0.4
        self.main_menu = True
        self.playing = False
        self.player_selection = False
        self.options_menu = False
        self.play_button = Sprite("Assets/menu/jogar.png", 2)
        self.play_button.set_position(650, 370)
        self.fase_button = Sprite("Assets/menu/fase_inicial.png", 2)
        self.fase_button.set_position(self.play_button.x - 50, self.play_button.y + 50)
        self.leave_button = Sprite("Assets/menu/sair.png", 2)
        self.leave_button.set_position(self.play_button.x + 15, self.play_button.y + 125)
        self.background = GameImage("Assets/menu/metal.png")

        self.fase_inicial = "tutorial"

    def check_click(self):
        if self.click_cooldown < 0.2:
            self.click_cooldown += self.janela.delta_time()
        if self.mouse.is_button_pressed(1) and self.click_cooldown >= 0.2:
            self.click_cooldown = 0
            return True
        return False

    def check_events(self):
        if self.main_menu:
            if self.mouse.is_over_object(self.play_button):
                self.play_button.set_curr_frame(0)
                if self.check_click():
                    self.playing = True
            else:
                self.play_button.set_curr_frame(1)

            if self.mouse.is_over_object(self.leave_button):
                self.leave_button.set_curr_frame(0)
                if self.check_click():
                    self.janela.close()
            else:
                self.leave_button.set_curr_frame(1)

            if self.mouse.is_over_object(self.fase_button):
                self.fase_button.set_curr_frame(1)
                if self.check_click():
                    self.fase_inicial = self.fases[(self.fases.index(self.fase_inicial)+1) % 3]
            else:
                self.fase_button.set_curr_frame(0)

        if self.keyboard.key_pressed("ESC"):
            self.playing = False
            self.options_menu = False
            self.player_selection = False
            self.main_menu = True

    def draw_menu(self):
        if self.main_menu:
            self.background.draw()
            self.play_button.draw()
            self.fase_button.draw()
            self.janela.draw_text(self.fase_inicial, self.fase_button.x + 70, self.fase_button.y + 23, 25,
                                  (255, 255, 255))
            self.leave_button.draw()

    def you_died_screen(self):
        from os import getcwd
        self.janela.draw_text("A música está se esvaindo...", self.janela.width / 2, self.janela.height / 2, 40,
                              (255, 0, 0),
                              font_name=f"{getcwd()}Assets/FreePixel.ttf")
