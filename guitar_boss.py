from os import getcwd
from PPlay.sprite import Sprite
class BossGuitarra:
    sprites = {
                # parada
                "idle_right": Sprite('Assets/boss_guitar/still_right.png'),
                "idle_left" : Sprite('Assets/boss_guitar/still_left.png'),
                # invocando microfone
                "swing_summon_right" : Sprite("Assets/boss_guitar/summon_right.png",6),
                "swing_summon_left" : Sprite("Assets/boss_guitar/summon_right.png",6),
                # girando microfone
                "swinging_right" : Sprite("Assets/boss_guitar/swinging_right.png",10),
                "swinging_left" : Sprite("Assets/boss_guitar/swinging_left.png",10),
                # tocando pra cima (ataque meteoro)
                "meteoro_right" : Sprite("Assets/boss_guitar/meteoro_right.png",4),
                "meteoro_left" : Sprite("Assets/boss_guitar/meteoro_left.png",4),
                # tocando agachada
                "playing_right" : Sprite("Assets/boss_guitar/playing_right.png",6),
                "playing_left" : Sprite("Assets/boss_guitar/playing_left.png",6),
                # arriving
                "arriving_left": Sprite("Assets/boss_guitar/falling.png",2),
                # morte
                "dying_right": Sprite("Assets/boss_guitar/dying_right.png",2),
                "dying_left": Sprite("Assets/boss_guitar/dying_left.png",2),
                }