import imp
import sys
from time import sleep
import pygame
from pygame.constants import FULLSCREEN
from settings import Settings
from game_stats import game_stat
from button import Button
from ship import Ship
from bullet import Bullet
from Alien import Alien
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.sett = Settings()
        self.screen = pygame.display.set_mode((1200, 800))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.sett.screen_width = self.screen.get_rect().width
        self.sett.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        self.play_button = Button(self, "Play")
        pygame.display.set_caption("Alien Invasion")
        self.stats = game_stat(self)
        self.sb = Scoreboard(self)

    def run_game(self):
        while True:
            self._check_event()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullet()
                self.Update_aliens()
            self._update_screen()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._event_keydown(event)
            elif event.type == pygame.KEYUP:
                self._event_keyup(event)

    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.game_active = True
            self.stats.reset_stat()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.centre_ship()
            pygame.mouse.set_visible(False)
            self.sett.initialize_dynamic_settings()

    def _event_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _event_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def fire_bullet(self):
        if len(self.bullets) <= self.sett.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets))
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self.check_alien_hit()

        self.check_bullet_alien_collision()

    def check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alins in collisions.values():
                self.stats.score += self.sett.alien_points * len(alins)
                # self.stats.score += self.sett.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.sett.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.centre_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_alien_hit(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.sett.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.image_rect.height
        available_space_y = self.sett.screen_height - (3 * alien_height) - ship_height
        number_row = available_space_y // (2 * alien_height)
        for number_row in range(number_row):
            for alien_number in range(number_aliens_x + 1):
                self.create_alien(alien_number, number_row)

    def create_alien(self, alien_number, number_row):
        alien = Alien(self)

        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien_width, alien_height = alien.rect.size
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * number_row)
        self.aliens.add(alien)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.sett.fleet_drop_speed
        self.sett.fleet_direction *= -1

    def _update_screen(self):
        self.screen.blit(self.sett.bg, self.screen.get_rect())
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def Update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
            # print("ship hit")
        self.check_alien_hit()


if __name__ == "__main__":
    a = AlienInvasion()
    a.run_game()
