import pygame as pg
import sys
import ctypes
from settings import *
from map import *
from menu import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from timer import *
from gamer import Gamer

class Game:
    def __init__(self):
        pg.init()
        self.main_running = True
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(screensize,pygame.FULLSCREEN)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()
        self.state = "Start"
        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
        self.game_paused_image1 = self.object_renderer.get_texture('resources/textures/game_paused1.png', RES)
        self.game_paused_image2 = self.object_renderer.get_texture('resources/textures/game_paused2.png', RES)

        
    def new_game(self):
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.player = Player(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.timer = Timer(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.timer.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def paused_menu(self):
        self.screen.blit(self.game_paused_image1, (-30, 20))
        pg.display.flip()
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.START_KEY = True
                    if event.key == pg.K_s:
                        self.DOWN_KEY = True
                    if event.key == pg.K_w:
                        self.UP_KEY = True
                if self.DOWN_KEY:
                    if self.state == 'Start':
                        pause = False
                        self.screen.blit(self.game_paused_image2, (-30, 20))
                        pg.display.flip()
                        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                        pause = True
                        self.state = 'Quit'
                elif self.UP_KEY:
                    if self.state == 'Quit':
                        pause = False
                        self.screen.blit(self.game_paused_image1, (-30, 20))
                        pg.display.flip()
                        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                        pause = True
                        self.state = 'Start'
                            
                if self.START_KEY:
                    if self.state == 'Start':
                        pause = False
                        self.UP_KEY, self.DOWN_KEY, self.START_KEY = False, False, False
                    elif self.state == 'Quit':
                        self.main_running = False
                        pause = False
                                      

            
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                #pg.quit()
                #sys.exit()
                self.paused_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.START_KEY = True
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while self.main_running:
            self.check_events()
            self.update()
            self.draw()
                    

if __name__ == '__main__':
    favicon = pygame.image.load("resources/0.png")    #favicon 설정
    pygame.display.set_icon(favicon)
    pygame.display.set_caption('Maze Gunner')
    while True:
        g = Gamer()
        while g.running:
            pygame.mixer.music.pause()
            g.curr_menu.display_menu()
            g.game_loop()
            g.game_quit()
        game = Game()
        while game.main_running:
            game.run() 
            
    
