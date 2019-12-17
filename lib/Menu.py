from lib.Const import *


class Base(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类初始化方法
        super().__init__()
        # 定义图像属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 垂直方向移动
        self.rect.y += self.speed


class Menu(Base):
    def __init__(self):
        super().__init__(MENU_IMAGE, speed=5)
        self.playerNum = 1
        self.rect.x = 107
        self.rect.y = -SCREEN_HEIGHT
        self.select_tank = SelectTank()
        self.select_tank_group = pygame.sprite.Group()
        self.ys = [250 + 91, 281 + 91]

    def select(self):
        # 选择坦克
        self.select_tank.rect.y = self.ys[self.playerNum - 1]
        self.select_tank_group.add(self.select_tank)

    def next(self, n):
        # 菜单选择
        self.playerNum += n
        if self.playerNum > 2:
            self.playerNum = 1
        elif self.playerNum < 1:
            self.playerNum = 2

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.y + 91:
            self.rect.y = SCREEN_RECT.y + 91
            self.select()


class SelectTank(Base):
    def __init__(self):
        super().__init__('./assets/images/others/select_tank.png', speed=0)
        self.select_tank_rect = pygame.Rect(POS['selectTank'])
        self.select_tank_image = pygame.image.load('./assets/images/others/select_tank.png')
        self.rect.x = 140 + 107
        self.times = 0

    def draw(self):
        self.times += 1
        # 动画
        if int(self.times // 6) % 2 == 0:
            self.select_tank_rect.top = 27
        else:
            self.select_tank_rect.top = 0
            self.times = 0
        self.image = self.select_tank_image.subsurface(self.select_tank_rect)

    def update(self):
        self.draw()
