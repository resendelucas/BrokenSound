from PPlay.sprite import *
from PPlay.window import *
from tiros import Tiro


class Player:
    # sprites visuais:
    Window(800,700)
    sprites = {
            "walk_right": Sprite("Assets/character/walking/walk_right.png", 6),
            'walk_left' : Sprite("Assets/character/walking/walk_left.png", 6),
            'walk_attack_right' : Sprite("Assets/character/walking/walk_attack_right.png", 6),
            'walk_attack_left' : Sprite("Assets/character/walking/walk_attack_left.png", 6),
            'playing_right' : Sprite("Assets/character/parado/attack_right.png", 4),
            'playing_left' : Sprite("Assets/character/parado/attack_left.png", 4),
            'still_right' : Sprite("Assets/character/parado/player_still_right.png"),
            'still_left' : Sprite("Assets/character/parado/player_still_left.png")
    }
    # sprites usadas no backend:
    hitbox = Sprite("Assets/character/player_hitbox.png")  # sprite deve ser sempre atualizada
    sprite_atual = sprites["walk_right"]
    # cooldown tiros:  
    cooldown = 0

    def __init__(self, janela, mapa):
        self.janela = janela
        self.mapa = mapa
        self.teclado = janela.get_keyboard()
        self.walkspeed = 200
        self.instrumento = 'violao'
        self.last_direction = 'right'
        self.delay = 0
        self.ready = True  # se pode atirar (não está em cooldown)
        self.hitbox.set_position(688, 608)
        self.is_playing = False
        self.gravity_on = False
        self.last_position = [0, 0]
    def check_events(self) -> None:
        """Checa inputs do player e muda as variáveis de estado de acordo."""
        # checar se está tocando música
        self.last_position[0], self.last_position[1] = self.hitbox.x, self.hitbox.y
        self.is_playing = self.teclado.key_pressed("z")
        if self.is_playing:
            self.sprite_atual = self.sprites[f'playing_{self.last_direction}']
        # checar se está apertando pra direita
        if self.teclado.key_pressed("RIGHT"):
            self.last_direction = 'right'
            self.hitbox.x += self.walkspeed * self.janela.delta_time()
            if not self.is_playing:
                self.sprite_atual = self.sprites["walk_right"]
            else:
                self.sprite_atual = self.sprites[f'walk_attack_{self.last_direction}']

        # checar se está apertando pra esquerda
        elif self.teclado.key_pressed("LEFT"):
            self.last_direction = 'left'
            self.hitbox.x -= self.walkspeed * self.janela.delta_time()
            if not self.is_playing:
                self.sprite_atual = self.sprites["walk_left"]
            else:
                self.sprite_atual = self.sprites[f'walk_attack_{self.last_direction}']
        else:  # se nenhuma tecla de movimento estiver sendo apertada
            self.sprite_atual = self.sprites[f'still_{self.last_direction}']
            
        # Atualiza posição do jogador
        # self.hitbox.y = 608 - self.hitbox.height

        # Atualiza o tempo de recarga
        self.delay += self.janela.delta_time()
        if self.delay >= self.cooldown:
            self.delay = 0
            # Atualiza os tiros
            if self.is_playing:
                if self.teclado.key_pressed("up"):
                    self.shoot(self.instrumento, (0, 1), self.hitbox)
                elif self.teclado.key_pressed("down"):
                    self.shoot(self.instrumento, (0, -1), self.hitbox)
                elif self.last_direction == 'right':
                    self.shoot(self.instrumento, (1, 0), self.hitbox)
                elif self.last_direction == 'left':
                    self.shoot(self.instrumento, (-1, 0), self.hitbox)

    @staticmethod
    def update_frame(sprite, ms):
        sprite.set_total_duration(ms)
        sprite.draw()
        sprite.update()

    @staticmethod
    def shoot(tipo, direcao, player):
        Tiro(tipo, direcao, player)

    def draw_player(self):
        self.sprite_atual.set_position(self.hitbox.x, self.hitbox.y)
        if not self.is_playing:
            self.update_frame(self.sprite_atual, 800)
        else:
            self.update_frame(self.sprite_atual, 300)
