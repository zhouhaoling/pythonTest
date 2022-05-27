import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """"表示单个外星人"""
    def __init__(self, ai_game):
        # 初始化并设置起始位置
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load(r'pythonTest\alien.bmp')
        self.rect = self.image.get_rect()

        # 最初位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    
    def update(self):
        #移动外星人
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        #判断外星人是否在屏幕边界
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        


