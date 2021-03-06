import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.setti = ai_game.sett
        self.screen = ai_game.screen
        self.color = ai_game.sett.bullet_color

        self.rect = pygame.Rect(0, 0, self.setti.bullet_width, self.setti.bullet_height)

        self.rect.midtop = ai_game.ship.image_rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.setti.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
