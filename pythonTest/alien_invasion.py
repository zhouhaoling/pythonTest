import sys
import pygame
class AlienInvasion:
    """管理有限资源合行为"""

    def _init_(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Alien Invasion")
    
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
            pygame.display.flip()


if __name__ == '_main_':
    ai = AlienInvasion()
    ai.run_game()
