from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window


class Menu:
    def __init__(self, janela: Window) -> None:
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
        self.leave_button = Sprite("Assets/menu/sair.png", 2)
        self.leave_button.set_position(650, 470)
        self.background = GameImage("Assets/menu/metal.png")

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

        if self.keyboard.key_pressed("ESC"):
            self.playing = False
            self.options_menu = False
            self.player_selection = False
            self.main_menu = True

    def draw_menu(self):
        if self.main_menu:
            self.background.draw()
            self.play_button.draw()
            self.leave_button.draw()

    def you_died_screen(self):
        from os import getcwd
        self.janela.draw_text("A música está se esvaindo...", self.janela.width / 2, self.janela.height / 2, 40,
                              (255, 0, 0),
                              font_name=f"{getcwd()}Assets/FreePixel.ttf")
