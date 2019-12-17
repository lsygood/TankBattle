from lib.Const import *
from lib.MapLevel import *


class Base(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, image_name):
        # 调用父类初始化方法
        super().__init__()
        # 定义图像属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()


class WALL(Base):
    def __init__(self):
        super().__init__('./assets/images/scene/brick.png')


class IRON(Base):
    def __init__(self):
        super().__init__('./assets/images/scene/iron.png')


class GRASS(Base):
    def __init__(self):
        super().__init__('./assets/images/scene/tree.png')


class WATER(Base):
    def __init__(self):
        super().__init__('./assets/images/scene/river1.png')


class ICE(Base):
    def __init__(self):
        super().__init__('./assets/images/scene/ice.png')


class HOME(Base):
    def __init__(self):
        super().__init__('./assets/images/home/home1.png')


class Map:

    def __init__(self):
        self.level = 1
        self.mapWidth = 630
        self.mapHeight = 630
        self.temp = 0
        self.dir = 1  # 中间切换的方向，1：合上，2：展开
        self.isReady = False  # 标识地图是否已经画好
        self.protect_time = 0  # 保护时间
        # 地图数组
        self.mapLevel = []
        # 家
        self.home = HOME()

    # 画一帧的图片
    def drawImage(self, resource_image, frame_image, left, top, x, y):
        resource_image = pygame.image.load(resource_image)
        frame_image = pygame.Rect(frame_image)
        frame_image.left = left
        frame_image.top = top
        sub_image = resource_image.subsurface(frame_image)
        screen.blit(sub_image, (x, y))

    def drawNum(self, x, y):
        num = self.level

        if num <= 9:
            self.drawImage(NUM_IMAGE,
                           POS["num"],
                           POS["num"][0] + num * 14, POS["num"][1],
                           x, y)
        else:
            g = num % 10
            s = num // 10 % 10
            self.drawImage(NUM_IMAGE,
                           POS["num"],
                           POS["num"][0] + s * 14, POS["num"][1],
                           x, y)
            self.drawImage(NUM_IMAGE,
                           POS["num"],
                           POS["num"][0] + g * 14, POS["num"][1],
                           x + 14, y)

    def playAudio(self, audio):
        pygame.mixer.music.load(audio)
        # 设置音量
        pygame.mixer.music.set_volume(0.5)
        # 播放
        pygame.mixer.music.play()

    # 初始化地图参数
    def init(self, level):
        self.dir = 1
        self.isReady = False
        self.level = level
        self.protect_time = 0
        self.temp = 0

    # 画切换地图的动画
    def drawStage(self):
        if self.dir == 1:
            # temp = 18*18 灰色屏幕已经画完
            if self.temp == 324:
                # 初始化地图
                self.initMap()
                # 显示关卡数
                self.drawImage(NUM_IMAGE, POS["stageLevel"],
                               POS["stageLevel"][0], POS["stageLevel"][1], 266, 315)
                self.drawNum(380, 315)

            elif self.temp == 324 + 720:
                # 720即调用了720/15次，主要用来停顿
                self.temp = 324
                self.dir = -1
                self.playAudio('./assets/audio/start.ogg')
            else:
                # 灰屏效果(设置屏幕背景为灰色)
                screen.fill((127, 127, 127), (0, self.temp, 688, 18))
                screen.fill((127, 127, 127), (0, 624 - self.temp - 18, 688, 18))
        else:
            self.isReady = True
        self.temp += 18 * self.dir

    # 初始化地图
    def initMap(self):
        self.setLevel(self.level)
        self.drawMap()

    # 设置关卡
    def setLevel(self, level):
        self.level = level
        # 加载地图数组
        self.mapLevel = eval("map" + str(self.level))

    # 绘制地图
    def drawMap(self):
        # 遍历地图数组并添加到各自的组和地图组
        for i in range(0, 26):
            for j in range(0, 26):
                if self.mapLevel[i][j] == MAPTYPE['WALL']:
                    wall = WALL()
                    wall.rect.x, wall.rect.y = j * 24, i * 24
                    map_Group.add(wall)
                elif self.mapLevel[i][j] == MAPTYPE['IRON']:
                    iron = IRON()
                    iron.rect.x, iron.rect.y = j * 24, i * 24
                    map_Group.add(iron)
                elif self.mapLevel[i][j] == MAPTYPE['WATER']:
                    water = WATER()
                    water.rect.x, water.rect.y = j * 24, i * 24
                    map_Group.add(water)
                elif self.mapLevel[i][j] == MAPTYPE['ICE']:
                    ice = ICE()
                    ice.rect.x, ice.rect.y = j * 24, i * 24
                    map_Group.add(ice)
                elif self.mapLevel[i][j] == MAPTYPE['GRASS']:
                    grass = GRASS()
                    grass.rect.x, grass.rect.y = j * 24, i * 24
                    map_Group.add(grass)
                elif self.mapLevel[i][j] == MAPTYPE['HOME']:
                    self.home = HOME()
                    self.home.rect.x, self.home.rect.y = j * 24, i * 24
                    map_Group.add(self.home)

    # 保护家
    def protect_home(self):
        if self.protect_time > 0:
            for i, j in [(23, 11), (23, 12), (23, 13), (23, 14), (24, 11), (24, 14), (25, 11),
                         (25, 14)]:
                iron = IRON()
                iron.rect.x, iron.rect.y = j * 24, i * 24
                map_Group.add(iron)
        else:
            for i, j in [(23, 11), (23, 12), (23, 13), (23, 14), (24, 11), (24, 14), (25, 11),
                         (25, 14)]:
                wall = WALL()
                wall.rect.x, wall.rect.y = j * 24, i * 24
                map_Group.add(wall)

    # 画地图右侧数据 玩家数据 剩余敌人数
    def drawRight(self, playerNum, player1, player2, enemyNum):
        # 敌人数
        x = 640
        y = 17
        for i in range(1, enemyNum):
            tempX = x
            tempY = y + int((i + 1) / 2) * 16
            if i % 2 == 0:
                tempX = x + 16
            self.drawImage(FLAG_IMAGE, (0, 0, 14, 14), 92, 0, tempX, tempY)

        # 旗帜和关卡数字
        self.drawImage(FLAG_IMAGE,
                       POS["score"],
                       60 + POS["score"][0], POS["score"][1],
                       640, 528)

        self.drawNum(640, 560)

        # 1P
        self.drawImage(FLAG_IMAGE,
                       POS["score"],
                       POS["score"][0], POS["score"][1],
                       640, 336)

        self.drawImage(NUM_IMAGE,
                       POS["num"],
                       POS["num"][0] + player1 * 14, POS["num"][1],
                       658, 352)
        # 2P
        self.drawImage(FLAG_IMAGE,
                       POS["score"],
                       POS["score"][0] + 30, POS["score"][1],
                       640, 416)

        if playerNum == 2:
            self.drawImage(NUM_IMAGE,
                           POS["num"],
                           POS["num"][0] + player2 * 14, POS["num"][1],
                           658, 433)
