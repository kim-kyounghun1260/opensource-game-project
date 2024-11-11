import pygame as pg
from settings import *
from main import *
import time

class Timer:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
    
    def game_timer(self):
        elapsed_time = int(time.time() - self.start_time)  # 초 단위로 경과 시간 계산
        self.hours, remainder = divmod(elapsed_time, 3600)  # 시 계산
        self.minutes, self.seconds = divmod(remainder, 60)  # 분과 초 계산
        
    def update(self):
        self.game_timer()
        return self.hours, self.minutes, self.seconds
                    
