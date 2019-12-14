import pygame

# 静态变量

SCREEN_WIDTH = 688  # 屏幕宽
SCREEN_HEIGHT = 624  # 屏幕高

# 定义屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RECT.size)

# 定义屏幕刷新频率
FRAME_PER_SEC = 60

# 敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
PROTECT_HOME_EVENT = pygame.USEREVENT+1

# **************图片资源*****************
MENU_IMAGE = "./assets/images/others/menu.gif"
NUM_IMAGE = "./assets/images/others/num.png"
FLAG_IMAGE = "./assets/images/others/flag.png"
BOOM_IMAGE = "./assets/images/others/boom.png"
# **************各个图块在图片中的位置*****************
POS = {
    'selectTank': (0, 0, 27, 27),
    'stageLevel': (140, 0, 78, 14),
    'num': (0, 0, 14, 14),
    'score': (0, 0, 30, 32),
    'tank': (0, 0, 48, 48),
    'protected': (0, 0, 48, 48),
    'enemyBefore': (0, 0, 48, 48),
    'boom': (0, 0, 66, 66),
}
# **************地图块类型*****************
MAPTYPE = {'WALL': 1,
           'IRON': 2,
           'GRASS': 3,
           'WATER': 4,
           'ICE': 5,
           'HOME': 9,
           'ANOTHREHOME': 8}
# **************声音资源*****************
pygame.mixer.init()
bulletCrack = pygame.mixer.Sound("./assets/audio/bulletCrack.ogg")
enemyCrack = pygame.mixer.Sound("./assets/audio/enemyCrack.ogg")
playerCrack = pygame.mixer.Sound("./assets/audio/playerCrack.ogg")
hit = pygame.mixer.Sound("./assets/audio/hit.ogg")
attack = pygame.mixer.Sound("./assets/audio/attack.ogg")
props = pygame.mixer.Sound("./assets/audio/prop.ogg")
bang = pygame.mixer.Sound("./assets/audio/bang.ogg")
add = pygame.mixer.Sound("./assets/audio/add.ogg")
# 定义游戏状态
GAME_STATE = {'GAME_MENU': 0,  # 菜单
              'GAME_INIT': 1,  # 初始化
              'GAME_START': 2,  # 开始
              'GAME_OVER': 3,  # 结束
              'GAME_WIN': 4}  # win

# 坦克及子弹的四个方向
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
# 所有坦克组
tanks_group = pygame.sprite.Group()