import pygame as pg
from settings import *
from timer import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.colon_image = self.get_texture('resources/textures/colon.png', (8, 20))
        self.kill_image = self.get_texture('resources/textures/kill.png', (80, 20))
        self.time_image = self.get_texture('resources/textures/time.png', (100, 70))
        self.timer_size = 30
        self.timer_image = [self.get_texture(f'resources/textures/digits/{i}.png', [self.timer_size] * 2)
                              for i in range(11)]
        self.timers = dict(zip(map(str, range(11)), self.timer_image))
        self.counter_size = 25
        self.counter_image = [self.get_texture(f'resources/textures/digits/{i}.png', [self.counter_size] * 2)
                              for i in range(11)]
        self.counters = dict(zip(map(str, range(11)), self.counter_image))
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 75
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        self.game_over_menu_image1 = self.get_texture('resources/textures/game_over_menu1.png', RES)
        self.game_over_menu_image2 = self.get_texture('resources/textures/game_over_menu2.png', RES)
        self.state = "Start"
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_kill_count()
        self.timer_object()

    def win(self):
        self.screen.blit(self.win_image, (-10, 0))
        
    def win_menu(self):
        self.screen.blit(self.game_over_menu_image1, (-5, 20))
        pg.display.flip()
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            self.START_KEY = True
                        if event.key == pg.K_s:
                            self.DOWN_KEY = True
                        if event.key == pg.K_w:
                            self.UP_KEY = True
            if self.DOWN_KEY:
                if self.state == 'Start':
                    pause = False
                    self.screen.blit(self.game_over_menu_image2, (-5, 20))
                    pg.display.flip()
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                    pause = True
                    self.state = 'Quit'
            elif self.UP_KEY:
                if self.state == 'Quit':
                    pause = False
                    self.screen.blit(self.game_over_menu_image1, (-5, 20))
                    self.state = 'Start'
                    pg.display.flip()
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                    pause = True
                    self.state = 'Start'
                    
            if self.START_KEY:
                if self.state == 'Start':
                    pause = False
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                elif self.state == 'Quit':
                    self.game.main_running = False
                    pause = False
                


    def game_over(self):
        self.screen.blit(self.game_over_image, (-15, 0))

    def game_over_menu(self):
        self.screen.blit(self.game_over_menu_image1, (-5, 20))
        pg.display.flip()
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            self.START_KEY = True
                        if event.key == pg.K_s:
                            self.DOWN_KEY = True
                        if event.key == pg.K_w:
                            self.UP_KEY = True
            if self.DOWN_KEY:
                if self.state == 'Start':
                    pause = False
                    self.screen.blit(self.game_over_menu_image2, (-5, 20))
                    pg.display.flip()
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                    pause = True
                    self.state = 'Quit'
            elif self.UP_KEY:
                if self.state == 'Quit':
                    pause = False
                    self.screen.blit(self.game_over_menu_image1, (-5, 20))
                    self.state = 'Start'
                    pg.display.flip()
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                    pause = True
                    self.state = 'Start'
                    
            if self.START_KEY:
                if self.state == 'Start':
                    pause = False
                    self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                elif self.state == 'Quit':
                    self.game.main_running = False
                    pause = False
                    
                
                
        

    def timer_object(self):
        self.screen.blit(self.time_image, (5, 573))
        self.screen.blit(self.colon_image, (175, 594))
        self.screen.blit(self.colon_image, (265, 594))
        time_seconds = str(self.game.timer.seconds)
        for i, char in enumerate(time_seconds):
            self.screen.blit(self.timers[char], (i * self.timer_size+275, 587))
        time_minutes = str(self.game.timer.minutes)
        for i, char in enumerate(time_minutes):
            self.screen.blit(self.timers[char], (i * self.timer_size+200, 587))
        time_hours = str(self.game.timer.hours)
        for i, char in enumerate(time_hours):
            self.screen.blit(self.timers[char], (i * self.timer_size+115, 587))
            

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 625))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 625))

    def draw_kill_count(self):
        self.screen.blit(self.kill_image, (7, 560))
        counter = str(self.game.object_handler.NPC_kill_count)
        for i, char in enumerate(counter):
            self.screen.blit(self.counters[char], (i * self.counter_size+95, 555))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
