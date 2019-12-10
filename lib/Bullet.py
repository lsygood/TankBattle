from lib.Const import *

class Bullet(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, tank, speed=3):
        super().__init__()
        # 子弹图片
        self.bullets_image = ['./assets/images/bullet/bullet_up.png',
                              './assets/images/bullet/bullet_down.png',
                              './assets/images/bullet/bullet_left.png',
                              './assets/images/bullet/bullet_right.png']
        # 加载图片
        self.dir = UP # 方向
        self.image = pygame.image.load(self.bullets_image[self.dir])
        self.rect = self.image.get_rect()
        self.size = 12 # 大小
        self.speed = speed # 速度
        self.stronger = False # 是否加强
        self.isDestroyed = False # 是否摧毁
        self.hit = False # 是否碰撞
        # 坦克对象
        self.tank = tank

    def move(self):
        # 改变图片
        self.image = pygame.image.load(self.bullets_image[self.dir])
        if self.dir == UP:
            self.rect.y -= self.speed
        if self.dir == DOWN:
            self.rect.y += self.speed
        if self.dir == LEFT:
            self.rect.x -= self.speed
        if self.dir == RIGHT:
            self.rect.x += self.speed

        # 碰撞检测
        self.isHit()

    def destroy(self):
        self.isDestroyed = True

    def isHit(self):
        # 子弹被坠毁
        if self.isDestroyed:
            return
        # 碰撞检测
        if not self.isDestroyed:
            if not self.hit:
                # 边缘检测
                if self.rect.x >= 612 or self.rect.y >= 612 or self.rect.x < 0 or self.rect.y < 0:
                    self.isDestroyed = True
            # 子弹碰撞后销毁
            else:
                self.destroy()
                # 音效
                if not self.tank.isAI:
                    enemyCrack.play()
            self.hit = False

    def update(self):
        self.move()
        # 销毁
        if self.isDestroyed:
            self.kill()
