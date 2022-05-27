

"""设置类"""
class Settiongs:
    """存储游戏中所有的设置"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        # self.bg_color = (230,230,230)
        # 飞船速度设置
        self.ship_speed = 1.5
        #飞船数量
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullet_allowed = 30
        # 外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1