from PPlay.sprite import Sprite
from boss_mae import BossClasseMae

class BossPiano(BossClasseMae):
    sprites = {
        # Skeletons

        "idle_right": Sprite('Assets/boss_piano/skeletons/idle_left.png', 4),
        "idle_left": Sprite('Assets/boss_piano/skeletons/idle_right.png', 4),
        # aparecendo
        "spawning_right": Sprite("Assets/boss_piano/skeletons/spawning_right.png", 8),
        "spawning_left": Sprite("Assets/boss_piano/skeletons/spawing_left.png", 8),
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
    }