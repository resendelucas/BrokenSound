from PPlay.sprite import *
from PPlay.window import *

class Skeleton(Sprite):
    Window(1365, 768)
    sprites = {
        "sidle_right": Sprite('Assets/boss_piano/skeletons/idle_left.png', 4),
        "sidle_left": Sprite('Assets/boss_piano/skeletons/idle_right.png', 4),
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
    }

    lista_inimigos = []

    def __init__(self, ):, p