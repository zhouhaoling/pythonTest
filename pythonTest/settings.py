

"""设置类"""
class Settiongs:
    """存储游戏中所有的设置"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        # self.bg_color = (230,230,230)
        # 飞船速度设置
        self.ship_speed = 1.5
        # 子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullet_allowed = 30