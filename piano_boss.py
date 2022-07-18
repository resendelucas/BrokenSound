from PPlay.sprite import Sprite
from boss_mae import BossClasseMae
from skeletons import Skeleton
from gaiola import Gaiola
from minigame_teclas import MiniGameTeclas
from obeliscos import Obelisco
from PPlay.sound import *
class BossPiano(BossClasseMae):
    sprites = {
        "summoner_playing": Sprite("Assets/boss_piano/boss_basic.png", 25),
        "basic_playing": Sprite("Assets/boss_piano/boss_aprendiz_playing.png", 25),
        "summoner_arriving": Sprite("Assets/boss_piano/summoner_arriving.png", 2),
        "basic_arriving": Sprite("Assets/boss_piano/skeleton_aprendiz_arriving.png", 2),
        "explosion": Sprite("Assets/boss_piano/explosion.png", 19)
    }
    sprite_atual = sprites["basic_arriving"]
    hitbox = Sprite("Assets/boss_piano/hitbox.png")
    sprites['summoner_arriving'].set_total_duration(0.2)
    sprites['summoner_playing'].set_total_duration(1.3)
    sprites['basic_arriving'].set_total_duration(0.2)
    sprites['basic_playing'].set_total_duration(1.3)
    sprites['explosion'].set_total_duration(600)

    cooldown_value = 2
    cooldown_atual = 0
    musica1 = Sound("Assets/boss_piano/spooky.ogg")
    musica1.loop = True
    musica2 = Sound("Assets/boss_piano/musica-boss-equeleto2.ogg")
    musica2.loop = True

    @classmethod
    def reset_class(cls):
        cls.sprites = {
            "summoner_playing": Sprite("Assets/boss_piano/boss_basic.png", 25),
            "basic_playing": Sprite("Assets/boss_piano/boss_aprendiz_playing.png", 25),
            "summoner_arriving": Sprite("Assets/boss_piano/summoner_arriving.png", 2),
            "basic_arriving": Sprite("Assets/boss_piano/skeleton_aprendiz_arriving.png", 2),
            "explosion": Sprite("Assets/boss_piano/explosion.png", 19)
        }
        cls.sprite_atual = cls.sprites["basic_arriving"]
        cls.hitbox = Sprite("Assets/boss_piano/hitbox.png")
        cls.sprites['summoner_arriving'].set_total_duration(0.2)
        cls.sprites['summoner_playing'].set_total_duration(1.3)
        cls.sprites['basic_arriving'].set_total_duration(0.2)
        cls.sprites['basic_playing'].set_total_duration(1.3)
        cls.sprites['explosion'].set_total_duration(600)

        cls.cooldown_value = 2
        cls.cooldown_atual = 0
        cls.musica1 = Sound("Assets/boss_piano/spooky.ogg")
        cls.musica1.loop = True
        cls.musica2 = Sound("Assets/boss_piano/musica-boss-equeleto2.ogg")
        cls.musica2.loop = True

    def __init__(self, janela):
        super().__init__(janela)
        self.is_started = False
        self.is_falling = False
        self.lista_tiros = []
        self.cronometro_still = 0
        self.is_playing = False
        self.gaiola = None
        self.mini_game = None
        self.obeliscos = []
        self.plataformas_obeliscos = None
        self.boss_final = False

        self.boss_name = 'piano'

    def spawn(self):
        self.is_started = True
        self.hitbox.x = self.janela.width / 2 - self.hitbox.width / 2
        self.hitbox.y = self.janela.height
        self.is_arriving = True
        self.is_underground = True

    def update(self):
        self.health_color = (255, 0, 255) if self.is_imune else (255, 0, 0)
        self.cooldown_atual += self.janela.delta_time()
        Skeleton.set_player_e_janela(self.player, self.janela)
        Skeleton.update_esqueletos()
        self.last_position = self.hitbox.x, self.hitbox.y
        if not self.is_finished and not self.is_dying:
            if self.is_arriving:
                self.hitbox.y -= 50 * self.janela.delta_time()
                if not self.is_underground:
                    self.cronometro_still += self.janela.delta_time()
                    if self.cronometro_still > 2:
                        self.cronometro_still = 0
                        self.is_playing = True
                        self.musica1.play()
                        self.musica1.set_volume(25)
                        self.sprite_atual = self.sprites['basic_playing']
                        self.is_arriving = False
                return

            if self.is_playing and self.sprite_atual is self.sprites['basic_playing']:
                if self.cooldown_atual >= self.cooldown_value and len(Skeleton.lista_inimigos) < 8:
                    self.spawn_esqueletos()

                if self.health_ratio <= 0.66 and not self.is_mini_game_on and not self.is_mini_game_done:
                    Skeleton.kill_all()
                    self.hitbox.y = -9999
                    self.sprite_atual = self.sprites['summoner_playing']
                    self.is_mini_game_on = True
                    self.musica1.fadeout(600)
                    self.musica2.play()
                    self.musica2.set_volume(25)
                    self.gaiola = Gaiola(self.player)
                    self.mini_game = MiniGameTeclas(self.gaiola)

            elif self.is_playing and self.is_mini_game_on and not self.is_mini_game_done:
                self.gaiola.cronometro_cair = 4
                self.engaiolar_player()
                self.mini_game.colisao_player_teclas()
                self.is_mini_game_done = self.health_ratio <= 0.33
                self.is_mini_game_on = not self.is_mini_game_done
                if self.is_mini_game_done and not self.is_mini_game_on:
                    self.spawn_obeliscos()

            elif self.is_playing and not self.is_mini_game_on and self.is_mini_game_done:
                self.obeliscos = Obelisco.lista
                self.is_imune = len(self.obeliscos) > 0
                if self.cooldown_atual >= self.cooldown_value and len(Skeleton.lista_inimigos) < 8:
                    self.spawn_esqueletos()
                if self.is_imune and not self.is_dying:
                    self.levar_dano(-50 * self.janela.delta_time())
                    if self.health_ratio > 0.5:
                        self.health_ratio = 0.5
                        self.health_atual = self.max_health * 0.5
                    self.health_color = (255, 0, 255)
                Obelisco.update()
                if self.health_ratio <= 0:
                    self.is_dying = True
                    self.musica2.fadeout(2000)
                    self.is_mini_game_done = True
                    Skeleton.kill_all()
                    self.cronometro_animacao = 0

            if self.player.healthbar.health_atual <= 0:
                if self.musica1.is_playing():
                    self.musica1.fadeout(800)
                if self.musica2.is_playing:
                    self.musica2.fadeout(800)

        self.feel_gravity()
        self.apply_motion()

    def spawn_obeliscos(self):
        for plataforma in self.plataformas_obeliscos:
            self.obeliscos.append(Obelisco(plataforma, self.janela))

    def spawn_esqueletos(self):
        if self.cooldown_atual >= self.cooldown_value and len(Skeleton.lista_inimigos) < 8:
            esqueleto = Skeleton()
            esqueleto.hitbox.x = 0
            esqueleto = Skeleton()
            esqueleto.hitbox.x = self.janela.width - esqueleto.hitbox.width
            Skeleton()
            self.cooldown_atual = 0

    def calibrar_posicao_sprite(self):
        self.sprite_atual.x = self.hitbox.x
        self.sprite_atual.y = self.hitbox.y

    def engaiolar_player(self):
        self.gaiola.set_minigame(self.mini_game)
        self.mini_game.update()
