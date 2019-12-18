from lib.Const import *


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 定义图像属性
        self.image = pygame.image.load(MENU_IMAGE)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.playerNum = 1
        self.rect.y = -SCREEN_HEIGHT
        # 选择坦克
        self.select_tank_image = pygame.image.load('./assets/images/others/select_tank.png')
        self.select_tank_rect = pygame.Rect(POS['selectTank'])
        self.times = 0
        self.ys = [250 + 60, 281 + 60]

    def select(self):
        # 选择坦克
        self.times += 1
        if int(self.times // 6) % 2 == 0:
            temp = 0
        else:
            temp = 27
        self.select_tank_rect.top = temp
        select_tank = self.select_tank_image.subsurface(self.select_tank_rect)
        screen.blit(select_tank, (140 + 85, self.ys[self.playerNum - 1]))

    def next(self, n):
        # 菜单选择
        self.playerNum += n
        if self.playerNum >= 2:
            self.playerNum = 1
        elif self.playerNum <= 1:
            self.playerNum = 2

    def update(self):
        # 垂直方向移动
        self.rect.y += self.speed
        if self.rect.y > SCREEN_RECT.y:
            self.rect.y = SCREEN_RECT.y
