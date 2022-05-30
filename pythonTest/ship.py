import imp
import pygame
from pygame.sprite import Sprite

"""飞船管理类"""
class Ship(Sprite):

    def __init__(self,ai_game):
        """初始化飞船及其位置"""
        super().__init__()
        self.setShip(ai_game)
        # self.image = pygame.image.load('pythonTest\picture\ship.bmp')
        # # 将飞船图片缩小,当图片过大时
        # self.image = pygame.transform.scale(self.image,(40,60))
        self.image = pygame.image.load(r'pythonTest\ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        #在飞船属性x中存储小数值
        self.x = float(self.rect.x)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        
    def setShip(self,ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        # 调整飞船位置
        # 更新飞船
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 更新rect对象
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
   