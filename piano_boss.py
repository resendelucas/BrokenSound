from PPlay.sprite import Sprite
from boss_mae import BossClasseMae


class BossPiano(BossClasseMae):
    sprites = {
        # Skeletons

        "idle_right": Sprite('Assets/boss_piano/skeletons/idle_left.png', 4),
        "idle_left": Sprite('Assets/boss_piano/skeletons/idle_right.png', 4),
        # aparecendo
        "spawning_right": Sprite("Assets/boss_piano/skeletons/spawning_right.png", 8),
        "spawning_left": Sprite("Assets/boss_piano/skeletons/spawning_left.png", 8),
        # andando
        "walking_left": Sprite("Assets/boss_piano/skeletons/walking_left.png", 8),
        "walking_right": Sprite("Assets/boss_piano/skeletons/walking_right.png", 8),
        # atacando
        "attacking_right": Sprite("Assets/boss_piano/skeletons/attacking_right.png", 8),
        "attacking_left": Sprite("Assets/boss_piano/skeletons/attacking_left.png", 8),
        # morrendo
        "dying_right": Sprite("Assets/boss_piano/skeletons/dying_right.png", 14),
        "dying_left": Sprite("Assets/boss_piano/skeletons/dying_left.png", 14),
        # Boss
        "summoner_playing": Sprite("Assets/boss_piano/boss_summoner.png", 41),
        "basic_playing": Sprite("Assets/boss_piano/boss_basic.png", 41),
        "summoner_arriving": Sprite("Assets/boss_piano/summoner_arriving.png", 2)
    }
    sprite_atual = sprites["summoner_arriving"]
    hitbox = Sprite("Assets/boss_piano/hitbox.png")
    sprites['summoner_arriving'].set_total_duration(0.2)
    
    
    def __init__(self, janela):
        super().__init__(janela, 10000, 10000)
        self.is_started = False
        self.is_falling = False
        self.lista_tiros = []
        
    def spawn(self):
        self.is_started = True
        self.hitbox.x = self.janela.width/2 - self.hitbox.width/2
        self.hitbox.y = self.janela.height
        self.is_arriving = True
        
    def update(self):
        self.last_position = self.hitbox.x, self.hitbox.y
        if self.is_arriving:
            print("alou")
            self.hitbox.y -= 50 * self.janela.delta_time()
            return
        self.feel_gravity()
        self.apply_motion()
        
    def calibrar_posicao_sprite(self):
        self.sprite_atual.x = self.hitbox.x
        self.sprite_atual.y = self.hitbox.y
        
        
        
    