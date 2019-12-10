from lib.Const import *

class Bullet(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, tank, speed=3):
        super().__init__()
        # 子弹相关
        self.bullets_image = ['./assets/images/bullet/bullet_up.png',
                              './assets/images/bullet/bullet_down.png',
                              './assets/images/bullet/bullet_left.png',
                              './assets/images/bullet/bullet_right.png']
        self.dir = UP
        self.image = pygame.image.load(self.bullets_image[self.dir])
        self.rect = self.image.get_rect()
        self.size = 12
        self.speed = speed
        self.stronger = False
        self.isDestroyed = False
        self.hit = False
        # 坦克
        self.tank = tank

    def move(self):
        self.image = pygame.image.load(self.bullets_image[self.dir])
        if self.dir == UP:
            self.rect.y -= self.speed
        if self.dir == DOWN:
            self.rect.y += self.speed
        if self.dir == LEFT:
            self.rect.x -= self.speed
        if self.dir == RIGHT:
            self.rect.x += self.speed

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
                # TODO 爆炸特效 和 音效
                if not self.tank.isAI:
                    enemyCrack.play()
            self.hit = False

    def update(self):
        self.move()
        # 销毁
        if self.isDestroyed:
            self.kill()
