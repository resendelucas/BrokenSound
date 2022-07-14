def check_camera(self, lista_gameobjects: list, mapa):
    self.v_camera = 200
    if self.hitbox.x + self.hitbox.width >= self.janela.width / 2 \
            and mapa.floor.x > mapa.boss_x_start:
        self.walkspeed = 0
        for gameobject in lista_gameobjects:
            if self.can_move:
                if self.teclado.key_pressed("RIGHT"):
                    gameobject.x -= self.v_camera * self.janela.delta_time()
                elif self.teclado.key_pressed("LEFT"):
                    if not mapa.floor.x > 0:
                        gameobject.x += self.v_camera * self.janela.delta_time()
                    else:
                        self.walkspeed = 200
    else:
        self.walkspeed = 200
        if mapa.floor.x < mapa.boss_x_start:
            mapa.floor.x = mapa.boss_x_start
            mapa.boss.spawn()