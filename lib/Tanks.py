from lib.Bullet import *
from lib.Prop import *


class Tank(pygame.sprite.Sprite):
    """坦克基类"""

    def __init__(self, resource_image, rect, speed=0):
        # 调用父类初始化方法
        super().__init__()
        # 定义图像属性
        self.resource_image = pygame.image.load(resource_image)
        self.image = self.resource_image.subsurface(rect)
        self.rect = self.image.get_rect()
        # 坦克相关
        self.lives = 0  # 生命
        self.isDestroyed = False  # 是否被摧毁
        self.enemyStopTime = 0  # 坦克停止时间
        # 移动相关
        self.dir = UP  # 方向：0:上 1:下 2:左 3:右
        self.speed = speed  # 坦克的速度
        self.frame = 0  # 控制敌方坦克切换方向的时间
        self.isMoving = False  # 是否可以移动
        self.isAI = False  # 是否自动
        # 动画效果
        self.time = 0
        self.moving = True
        # 射击相关
        self.shootRate = 0.6  # 射击的概率
        self.isShooting = False  # 子弹是否在运行中o
        self.bullet = Bullet()
        # 碰撞
        self.hit = False  # 是否碰到墙或者坦克
        self.map = None

    # 画图
    def drawImage(self, image, rect, left, top):
        resource_image = pygame.image.load(image)
        resource_rect = pygame.Rect(rect)
        resource_rect.left, resource_rect.top = left, top
        self.image = resource_image.subsurface(resource_rect)

    def draw(self):
        # 动画效果
        self.time += 1
        if self.time == 5:
            self.time = 0
            self.moving = not self.moving

        if self.isAI and self.enemyStopTime > 0:
            self.enemyStopTime -= 1
            self.moving = False

    # 移动
    def move(self):

        # 如果是AI坦克，在一定时间或者碰撞之后切换方法
        if self.isAI and self.enemyStopTime > 0:
            return

        # 记录坐标
        tempX = self.rect.x
        tempY = self.rect.y

        if self.isAI:
            self.frame += 1
            if self.frame % 100 == 0:
                self.dir = random.randint(0, 3)  # 随机一个方向
                self.frame = 0

        if self.dir == UP:
            self.rect.y -= self.speed
        elif self.dir == DOWN:
            self.rect.y += self.speed
        elif self.dir == RIGHT:
            self.rect.x += self.speed
        elif self.dir == LEFT:
            self.rect.x -= self.speed

        # 碰撞检测
        self.isHit()

        # 碰撞后还原坐标
        if self.hit:
            self.rect.x = tempX
            self.rect.y = tempY
            self.hit = False
            if self.isAI:
                self.dir = random.randint(0, 3)  # 随机方向

    def isHit(self):
        if not self.isDestroyed:
            if not self.hit:
                # 地图边缘检测
                if self.rect.y > 576 or self.rect.x > 576 or self.rect.x < 0 or self.rect.y < 0:
                    self.hit = True
                # 地图碰撞检测
                for map in self.map.mapGroup:
                    if (map not in self.map.grassGroup) and (map not in self.map.iceGroup):
                        if pygame.sprite.collide_rect(self, map):
                            self.hit = True
                            break

    # 射击
    def shoot(self):
        if self.isAI and self.enemyStopTime > 0:
            return
        if self.isShooting:
            return
        else:
            self.bullet.dir = self.dir
            self.bullet.isDestroyed = False
            self.bullet.hit = False
            if self.dir == UP:
                self.bullet.rect.x = self.rect.centerx - (self.bullet.size // 2)
                self.bullet.rect.y = self.rect.y - self.bullet.size
            elif self.dir == DOWN:
                self.bullet.rect.x = self.rect.centerx - (self.bullet.size // 2)
                self.bullet.rect.y = self.rect.y + 48
            elif self.dir == LEFT:
                self.bullet.rect.x = self.rect.x - self.bullet.size
                self.bullet.rect.y = self.rect.centery - (self.bullet.size // 2)
            elif self.dir == RIGHT:
                self.bullet.rect.x = self.rect.x + 48
                self.bullet.rect.y = self.rect.centery - (self.bullet.size // 2)
            # 音效
            if not self.isAI:
                attack.play()
            # 射击
            self.isShooting = True

    def destroy(self):
        self.isDestroyed = True
        tempDir = 1
        ts = 0
        # 爆炸效果
        flag = True
        # 爆炸效果
        if flag:
            temp = int(ts // 3)
            boom_image = pygame.image.load(BOOM_IMAGE)
            boom_rect = pygame.Rect(POS['boom'])
            boom_rect.left = 65 * temp
            boom = boom_image.subsurface(boom_rect)
            screen.blit(boom, (self.rect.x + (65 - 48) // 2, self.rect.y + (65 - 48) // 2))
            ts += tempDir
            if ts > 4 * 3 - 3:
                tempDir = -1
            if ts <= 0:
                flag = False

    def update(self):
        self.draw()
        if self.isDestroyed:
            self.kill()
        if self.isMoving:
            self.move()


class PlayerTank(Tank):
    """玩家坦克"""

    def __init__(self, player=1):
        super().__init__(
            './assets/images/myTank/tank_T1_0.png', POS['tank'], speed=3)
        self.color = 0
        self.lives = 3  # 生命值
        self.isProtected = True  # 是否受保护
        self.protectedTime = 500  # 保护时间
        self.player = player  # 玩家
        # 出生
        self.rect.x, self.rect.y = 195, 576
        self.tanks_image = ['./assets/images/myTank/tank_T1_0.png',
                            './assets/images/myTank/tank_T1_1.png',
                            './assets/images/myTank/tank_T1_2.png']
        if self.player == 2:
            self.rect.x, self.rect.y = 387, 576
            self.tanks_image = ['./assets/images/myTank/tank_T2_0.png',
                                './assets/images/myTank/tank_T2_1.png',
                                './assets/images/myTank/tank_T2_2.png']

    def init(self):
        self.dir = UP
        self.lives = 3  # 生命值
        self.color = 0  # 等级
        self.speed = 3  # 速度
        self.isMoving = False
        self.isProtected = True  # 是否受保护
        self.protectedTime = 500  # 保护时间
        self.bullet.stronger = False
        self.rect.x, self.rect.y = 195, 576
        if self.player == 2:
            self.rect.x, self.rect.y = 387, 576

    # 创建玩家坦克
    def draw(self):
        super().draw()
        if self.moving and self.isMoving:
            self.drawImage(self.tanks_image[self.color], POS['tank'], 0, self.dir * 48)
        else:
            self.drawImage(self.tanks_image[self.color], POS['tank'], 48, self.dir * 48)

        # 保护动画
        if self.isProtected:
            temp = int((500 - self.protectedTime) // 5) % 2

            protected_image = pygame.image.load('./assets/images/others/protect.png')
            protected_rect = pygame.Rect(POS['protected'])
            protected_rect.left = 48 * temp
            protected = protected_image.subsurface(protected_rect)
            screen.blit(protected, self.rect)

            self.protectedTime -= 1
            if self.protectedTime == 0:
                self.isProtected = False

    # 等级提升
    def level(self, l=1):
        if self.color < 3:
            self.color += l
        if self.color > 3:
            self.color = 3
        elif self.color <= 0:
            self.color = 0

        if self.color == 0:
            self.speed = 3
            self.bullet.speed = 3
            self.bullet.stronger = False
        elif self.color == 2:
            self.speed = 6
            self.bullet.speed = 6
            self.bullet.stronger = False
        elif self.color == 3:
            self.speed = 6
            self.bullet.speed = 9
            self.bullet.stronger = False

    def destroy(self):
        super().destroy()
        # 音效
        playerCrack.play()

    def reload(self):
        # 被摧毁后重新载入
        if self.isDestroyed and self.lives > 0:
            self.dir = UP
            self.rect.x, self.rect.y = 195, 576
            if self.player == 2:
                self.rect.x, self.rect.y = 387, 576
            self.lives -= 1
            self.level(-1) # 等级降低
            self.isProtected = True  # 是否受保护
            self.protectedTime = 500  # 保护时间
            self.isDestroyed = False

    def update(self):
        super().update()
        self.reload()


class EnemyTank(Tank):
    """敌人坦克"""

    def __init__(self, x=None):
        super().__init__(
            './assets/images/enemyTank/enemy_1_0.png', POS['tank'], speed=0)
        self.times = 0  # 定时
        self.isAI = True  # AI
        self.isMoving = True
        # 出生
        if x is None:
            self.x = random.randint(0, 2)
        else:
            self.x = x
        self.rect.x, self.rect.y = self.x * 12 * 24, 0
        self.dir = DOWN
        self.isAppear = False  # 显示出场动画
        self.appear_image = './assets/images/others/appear.png'
        # 坦克种类
        self.enemy1 = ['./assets/images/enemyTank/enemy_1_0.png',
                       './assets/images/enemyTank/enemy_1_1.png',
                       './assets/images/enemyTank/enemy_1_2.png',
                       './assets/images/enemyTank/enemy_1_3.png']
        self.enemy2 = ['./assets/images/enemyTank/enemy_2_0.png',
                       './assets/images/enemyTank/enemy_2_1.png',
                       './assets/images/enemyTank/enemy_2_2.png',
                       './assets/images/enemyTank/enemy_2_3.png']
        self.enemy3 = ['./assets/images/enemyTank/enemy_3_0.png',
                       './assets/images/enemyTank/enemy_3_1.png',
                       './assets/images/enemyTank/enemy_3_2.png',
                       './assets/images/enemyTank/enemy_3_3.png']
        self.enemy4 = ['./assets/images/enemyTank/enemy_4_0.png',
                       './assets/images/enemyTank/enemy_4_1.png',
                       './assets/images/enemyTank/enemy_4_2.png',
                       './assets/images/enemyTank/enemy_4_3.png']
        self.enemy_list = [self.enemy1, self.enemy2, self.enemy3, self.enemy4]
        # 种类
        self.kind = random.randint(0, 3)
        # 速度
        self.speed = max(3 - self.kind, 1)
        # 是否携带食物(红色的坦克携带食物)
        self.is_red = random.choice((True, False, False, False, False))
        # 同一种类的坦克具有不同的颜色
        if self.is_red:
            self.lives = 3
            # 道具
            self.prop = Prop()
        else:
            self.lives = random.randint(0, 2)

    def draw(self):
        self.times += 1
        # 出场动画
        if not self.isAppear:
            temp = int(self.times // 5) % 3
            self.drawImage(self.appear_image, POS['enemyBefore'], temp * 48, 0)
            if self.times == 34:
                self.isAppear = True
                self.times = 0
        else:
            super().draw()
            if self.moving and self.isMoving:
                self.drawImage(self.enemy_list[self.kind][self.lives],
                               POS['tank'], 0, self.dir * 48)
            else:
                self.drawImage(self.enemy_list[self.kind][self.lives],
                               POS['tank'], 48, self.dir * 48)

            if self.times % 50 == 0:
                r = random.random()
                # 以一定的概率射击
                if r < self.shootRate:
                    self.shoot()
                self.times = 0
                self.isShooting = False

    def destroy(self):
        super().destroy()
        # 音效
        enemyCrack.play()

    def update(self):
        super().update()
