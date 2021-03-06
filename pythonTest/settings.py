

"""设置类"""
class Settiongs:
    """存储游戏中所有的设置"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        #飞船数量
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullet_allowed = 30
        # 外星人设置
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        #加快游戏节奏的速度
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # 设置星星间距最大值
        self.max_x_space = 100
        self.max_y_space = 100

    
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        # 飞船、子弹、外星人速度设置
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1
        #记分
        self.alien_points = 50
    
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale 
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)

