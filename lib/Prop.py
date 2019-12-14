import random

from lib.Const import *


# 食物类, 用于提升坦克能力


class Prop(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 消灭当前所有敌人
        self.boom = './assets/images/prop/boom.png'
        # 当前所有敌人静止一段时间
        self.clock = './assets/images/prop/clock.png'
        # 使得坦克子弹可碎钢板
        self.gun = './assets/images/prop/gun.png'
        # 使得大本营的墙变为钢板
        self.iron = './assets/images/prop/iron.png'
        # 坦克获得一段时间的保护罩
        self.protect = './assets/images/prop/protect.png'
        # 坦克升级
        self.star = './assets/images/prop/star.png'
        # 坦克生命+1
        self.tank = './assets/images/prop/tank.png'
        # 所有食物
        self.props = [self.boom, self.clock, self.gun,
                      self.iron, self.protect, self.star, self.tank]
        # 是否存在
        self.isDestroyed = False
        self.hit = False
        # 存在时间
        self.times = 1000
        self.kind = random.randint(0, 6)
        # 加载图片
        self.image = pygame.image.load(self.props[self.kind])
        self.rect =  self.rect = self.image.get_rect()
        # 随机坐标
        self.rect.x, self.rect.y = random.randint(100, 500), random.randint(100, 500)

    # 生成道具
    def draw(self):
        if self.times > 0 and not self.isDestroyed:
            self.isDestroyed = False
            self.isHit()
        else:
            self.isDestroyed = True
        # 定时
        self.times -= 1

    def isHit(self):
        if self.hit:
            self.destroy()

    def destroy(self):
        self.isDestroyed = True

    def update(self):
        self.draw()
        if self.isDestroyed:
            self.kill()
