import pygame


class game_stat:
    def __init__(self, ai_game):
        self.settings = ai_game.sett
        self.reset_stat()
        self.game_active = False
        self.high_score = 0

    def reset_stat(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level=1
