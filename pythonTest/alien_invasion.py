import sys
from time import sleep
import pygame
from random import randint

from button import Button
from alien import Alien
from settings import Settiongs
from ship import Ship
from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
from star import Star

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
        self.scb = Scoreboard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        

        self._create_fleet()
        self.stars = pygame.sprite.Group()
        self.create_stars(self.settings.screen_width, self.settings.screen_height, self.settings.max_x_space, self.settings.max_y_space)
        self.play_button = Button(self, "Play")


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
        self.screen.fill(self.settings.bg_color)
        # background = pygame.image.load(r'pythonTest\universe.jpg').convert()
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            # self._update_screen(background)


    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #记录最高分,在退出之前
                    self.stats.save_high_score()
                    sys.exit()
                # elif event.type == pygame.VIDEORESIZE:
                #     SCREEN_SIZE = event.size
                #     self.screen = pygame.display.set_mode(SCREEN_SIZE,pygame.RESIZABLE)
                #     pygame.display.update()
                #左右移动 
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮的时候开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scb.prep_score()
            self.scb.prep_level()
            self.scb.prep_ships()
            #清空游戏屏幕
            self.aliens.empty()
            self.bullets.empty()
            #重新创建
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

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
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scb.prep_score()
            self.scb.check_high_score() 
        if not self.aliens:
            #清空屏幕并重新创建
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level += 1
            self.scb.prep_level()
        
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
            self.stats.save_high_score()
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
    
    

               #           , background
    def _update_screen(self):
            self.screen.fill(self.settings.bg_color)
            # 在屏幕上绘制飞船
            # self.screen.blit(background,(0,0))
            #绘制星星背景
            self.stars.draw(self.screen)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.scb.show_score()
            if not self.stats.game_active:
                self.play_button.draw_button()
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
        # self._show_false()
        if self.stats.ships_left > 0:
            self._show_false()
            # 将ships_left减一并更新记分牌
            self.stats.ships_left -= 1
            self.scb.prep_ships()
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人，并将飞船放置底部
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _show_false(self):
        font_name = pygame.font.match_font('fangsong')
        font = pygame.font.Font(font_name, 100)
        font_surface = font.render('闯关失败', True, (255,0,0), (255,255,255))
        self.screen.blit(font_surface, (600,400))
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

    def create_star(self, star_right_coordinate, random_x_space,
                    star_bottom_coordinate, random_y_space):
        # 创建一个星星
        star = Star(self)
        # 新增星星左坐标为前一个星星右坐标加随机横间距
        star.rect.x = star_right_coordinate + random_x_space
        # 每行星星上方留出适当空间
        star.rect.y = star_bottom_coordinate + random_y_space
        # 将星星增添到星星群
        self.stars.add(star)
    
    def create_stars(self, screen_width, screen_height, max_x_space,
                     max_y_space):
        star = Star(self)
        # 记录前一个星星右坐标
        star_right_coordinate = 0
        # 记录前行星星底坐标
        star_bottom_coordinate = 0
        # 增加随机列间距
        random_x_space = randint(1, max_x_space)
        # 增加随机行间距
        random_y_space = randint(1, max_y_space)
        # 屏幕纵向空间足够时循环创建整行星星
        while star_bottom_coordinate + star.rect.height + random_y_space < screen_height:
            # 屏幕横向空间足够时循环创建单个星星
            while star_right_coordinate + star.rect.width + random_x_space < screen_width:
                self.create_star(star_right_coordinate, random_x_space,
                                 star_bottom_coordinate, random_y_space)
                # 重置前一个星星右坐标和随机横间距
                star_right_coordinate = star_right_coordinate + star.rect.width + random_x_space
                random_x_space = randint(1, max_x_space)
            # 重置前一个星星右坐标、前行星星底坐标和随机纵间距
            star_right_coordinate = 0
            star_bottom_coordinate = star_bottom_coordinate + star.rect.height + random_y_space
            random_y_space = randint(1, max_y_space)



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
