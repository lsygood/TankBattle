from lib.Const import *


class Base(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, image_name, frame_image=None, speed=1):
        # 调用父类初始化方法
        super().__init__()
        # 定义图像属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

        if frame_image:
            self.image = self.image.subsurface(frame_image)

    def update(self):
        # 垂直方向移动
        self.rect.y += self.speed


class Menu(Base):
    def __init__(self):
        super().__init__(MENU_IMAGE, speed=5)
        self.playerNum = 1
        self.rect.left = 107
        self.rect.y = -SCREEN_HEIGHT
        self.select_tank = SelectTank()
        self.select_tank_group = pygame.sprite.Group()
        self.ys = [250+91, 281+91]

    def select(self):
        # 选择坦克
        self.select_tank.rect.x = 140+107
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
        super().__init__('./assets/images/others/select_tank.png', frame_image=POS['selectTank'],
                         speed=0)