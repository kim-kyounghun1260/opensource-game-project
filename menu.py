import pygame

class Menu():
    def __init__(self, gamer):
        self.gamer = gamer
        self.mid_w, self.mid_h = self.gamer.DISPLAY_W / 2, self.gamer.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.gamer.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.gamer.window.blit(self.gamer.display, (0, 0))
        pygame.display.update()
        self.gamer.reset_keys()

class MainMenu(Menu):
    def __init__(self, gamer):
        Menu.__init__(self, gamer)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.quitx, self.quity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.gamer.check_events()
            self.check_input()
            self.gamer.display.fill(self.gamer.BLACK)
            self.gamer.draw_text('Maze Gunner', 20, self.gamer.DISPLAY_W / 2, self.gamer.DISPLAY_H / 2 - 20)
            self.gamer.draw_text("Start", 20, self.startx, self.starty)
            self.gamer.draw_text("Quit", 20, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.gamer.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
        elif self.gamer.UP_KEY:
            if self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            

    def check_input(self):
        self.move_cursor()
        if self.gamer.START_KEY:
            if self.state == 'Start':
                self.gamer.playing = True
            elif self.state == 'Quit':
                self.gamer.quiting = True  
           
            self.run_display = False









