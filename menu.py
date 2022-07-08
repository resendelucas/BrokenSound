from PPlay.sprite import *
from PPlay.gameimage import *

class Menu:
    def __init__(self, janela) -> None:
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
        self.play_button.set_position(300,240)
        self.player_button = Sprite("Assets/menu/jogador.png", 2)
        self.player_button.set_position(300,340)
        self.options_button = Sprite("Assets/menu/opções.png", 2)
        self.options_button.set_position(300,440)
        self.leave_button = Sprite("Assets/menu/sair.png", 2)
        self.leave_button.set_position(320,540)
        self.background = GameImage("Assets/menu/menu_bg.png")

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
                self.play_button.set_curr_frame(1)
                if self.check_click():
                    self.playing = True
            else:
                self.play_button.set_curr_frame(0)

            if self.mouse.is_over_object(self.player_button):
                self.player_button.set_curr_frame(1)
                if self.check_click():
                    self.player_selection = True
                    self.main_menu = False
            else:
                self.player_button.set_curr_frame(0)

            if self.mouse.is_over_object(self.options_button):
                self.options_button.set_curr_frame(1)
                if self.check_click():
                    self.options_menu = True
                    self.main_menu = False
            else:
                self.options_button.set_curr_frame(0)

            if self.mouse.is_over_object(self.leave_button):
                self.leave_button.set_curr_frame(1)
                if self.check_click():
                    self.janela.close()
            else:
                self.leave_button.set_curr_frame(0)
                
        if self.keyboard.key_pressed("ESC"):
            self.playing = False
            self.options_menu = False
            self.player_selection = False
            self.main_menu = True

    def draw_menu(self):
        if self.main_menu:
            self.background.draw()
            self.play_button.draw()
            self.player_button.draw()
            self.options_button.draw()
            self.leave_button.draw()