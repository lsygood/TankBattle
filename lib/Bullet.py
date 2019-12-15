from lib.Map import *


class Bullet(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, speed=3):
        super().__init__()
        # 子弹图片
        self.bullets_image = ['./assets/images/bullet/bullet_up.png',
                              './assets/images/bullet/bullet_down.png',
                              './assets/images/bullet/bullet_left.png',
                              './assets/images/bullet/bullet_right.png']
        # 加载图片
        self.dir = UP  # 方向
        self.image = pygame.image.load(self.bullets_image[self.dir])
        self.rect = self.image.get_rect()
        self.size = 12  # 大小
        self.speed = speed  # 速度
        self.stronger = False  # 是否加强
        self.isDestroyed = False  # 是否摧毁
        self.hit = False  # 是否碰撞

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

        # 子弹碰撞后销毁
        if self.hit:
            self.destroy()
            self.hit = False

    def destroy(self):
        self.isDestroyed = True

    def isHit(self):
        if not self.isDestroyed:
            if not self.hit:
                # 边缘检测
                if self.rect.x >= 612 or self.rect.y >= 612 or self.rect.x < 0 or self.rect.y < 0:
                    self.hit = True
                # 子弹碰撞子弹
                bullet_group.remove(self)
                if pygame.sprite.spritecollide(self,bullet_group,False):
                    self.hit = True
                bullet_group.add(self)
                # 地图检测
                for map in map_Group:
                    if pygame.sprite.collide_rect(self, map):
                        if isinstance(map, (WALL, HOME)):
                            map.kill()
                            map_Group.remove(map)
                        # 子弹增强
                        if self.stronger:
                            if isinstance(map, IRON):
                                map.kill()
                                map_Group.remove(map)
                        # 销毁
                        if not isinstance(map, (GRASS, WATER, ICE)):
                            self.hit = True
                            bullet_group.remove(self)
                            break

    def update(self):
        self.move()
        # 销毁
        if self.isDestroyed:
            self.kill()
