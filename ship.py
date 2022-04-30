import pygame
from pygame import image
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.sett
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("images\\heroship.bmp")
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect()
        self.image_rect = self.image.get_rect()
        self.image_rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.image_rect.x)
        self.y = float(self.image_rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.image_rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.image_rect.left > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_up and self.image_rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.image_rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.image_rect.x = self.x
        self.image_rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)

    def centre_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.image_rect.x)
