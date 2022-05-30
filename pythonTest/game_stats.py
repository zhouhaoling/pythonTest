


from tkinter import W


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.game_active = False
        self.settings = ai_game.settings
        self.reset_stats()
        #任何情况下都不应重置最高的分
        self.high_score = 0
        self.load_high_score()
    
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        # self.load_high_score()
    
    def save_high_score(self):
        """保存最高得分"""
        with open('pythonTest\high_score.txt', 'w') as file_object:
            file_object.write(str(self.high_score))
            file_object.close()
    
    def load_high_score(self):
        try:
            with open('pythonTest\high_score.txt') as file_object:
                h_s = file_object.read()
                try:
                    self.high_score = int(h_s)
                except ValueError:
                    self.high_score = 0
                file_object.close()
        except FileNotFoundError:
            with open('pythonTest\high_score.txt', 'w') as file_object:
                file_object.close()