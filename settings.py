import pygame


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (53, 23, 68)
        self.ship_speed = 1.5
        self.bg = pygame.image.load("images\\background.bmp")
        # self.bg = pygame.image.load("images\\bqFxu5.jpg")
        # self.bg = pygame.transform.scale(self.bg, (1920, 1080))
        self.bullet_speed = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 10
        self.alien_speed = 1
        self.fleet_drop_speed = 7
        self.fleet_direction = -1
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 4
        self.alien_speed = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed * -self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)