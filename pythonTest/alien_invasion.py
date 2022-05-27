from cmath import inf
import imp
import sys
from time import sleep
import pygame

from alien import Alien
from settings import Settiongs
from ship import Ship
from bullet import Bullet
from game_stats import GameStats

SCREEN_SIZE = (1200,800)

class AlienInvasion:
    """管理有限资源合行为"""

    def __init__(self):
        """初始化pyagem"""
        pygame.init()
        self.settings = Settiongs()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height),pygame.RESIZABLE
        # )
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """创建外星人"""
        alien = Alien(self)
        # 计算一行可以容纳多少个外星人，其间距为外星人宽度
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)


    def run_game(self):
        #设置背景图片
        background = pygame.image.load(r'pythonTest\universe.jpg').convert()
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen(background)


    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    SCREEN_SIZE = event.size
                    self.screen = pygame.display.set_mode(SCREEN_SIZE,pygame.RESIZABLE)
                    pygame.display.update()
                #左右移动 
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _update_bullets(self):
        """更新子弹位置"""
        self.bullets.update()
        """删除消失的子弹"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_colisions()
        

    def _check_bullet_alien_colisions(self):
        #删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        
    def _update_aliens(self):
        #更新外星人位置
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()



    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
                
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """创建一颗子弹，并加入编组bullets中"""
        # 限制子弹数量
        # if len(self.bullets)<self.settings.bullet_allowed:
        #     new_bullet = Bullet(self)
        #     self.bullets.add(new_bullet)
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    
    

    def _update_screen(self,background):
            # self.screen.fill(self.settings.bg_color)
            # 在屏幕上绘制飞船
            self.screen.blit(background,(0,0))
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            pygame.display.update()    

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 
    
    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        self._show_false()
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人，并将飞船放置底部
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False

    def _show_false(self):
        font_name = pygame.font.match_font('fangsong')
        font = pygame.font.Font(font_name, 100)
        font_surface = font.render('闯关失败,重新开始', True, (255,0,0))
        self.screen.blit(font_surface, (500,500))
        pygame.display.flip()
        sleep(1)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #闯关失败
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
