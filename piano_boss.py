from PPlay.sprite import Sprite
from boss_mae import BossClasseMae


class BossPiano(BossClasseMae):
    sprites = {
        "summoner_playing": Sprite("Assets/boss_piano/boss_basic.png", 25),
        "basic_playing": Sprite("Assets/boss_piano/boss_aprendiz_playing.png", 25),
        "summoner_arriving": Sprite("Assets/boss_piano/summoner_arriving.png", 2),
        "basic_arriving": Sprite("Assets/boss_piano/skeleton_aprendiz_arriving.png", 2)
    }
    sprite_atual = sprites["basic_arriving"]
    hitbox = Sprite("Assets/boss_piano/hitbox.png")
    sprites['summoner_arriving'].set_total_duration(0.2)
    sprites['summoner_playing'].set_total_duration(1.3)
    sprites['basic_arriving'].set_total_duration(0.2)
    sprites['basic_playing'].set_total_duration(1.3)
    
    
    def __init__(self, janela):
        super().__init__(janela, 10000, 10000)
        self.is_started = False
        self.is_falling = False
        self.lista_tiros = []
        self.cronometro_still = 0
        self.is_playing = False

    def spawn(self):
        self.is_started = True
        self.hitbox.x = self.janela.width/2 - self.hitbox.width/2
        self.hitbox.y = self.janela.height
        self.is_arriving = True
        self.is_underground = True
        
    def update(self):
        self.last_position = self.hitbox.x, self.hitbox.y
        if self.is_arriving:
            self.hitbox.y -= 50 * self.janela.delta_time()
            if not self.is_underground:
                self.cronometro_still += self.janela.delta_time()
                if self.cronometro_still > 2:
                    self.cronometro_still = 0
                    self.is_playing = True
                    self.sprite_atual = self.sprites['basic_playing']
                    self.is_arriving = False
            return

        if self.is_playing:
            pass
        self.feel_gravity()
        self.apply_motion()
        
    def calibrar_posicao_sprite(self):
        self.sprite_atual.x = self.hitbox.x
        self.sprite_atual.y = self.hitbox.y
        
        
        
    