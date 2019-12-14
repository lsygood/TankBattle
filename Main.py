from lib.Map import *
from lib.Menu import *
from lib.Tanks import *

pygame.init()


class TankGame(object):
    """主程序"""

    def __init__(self):
        pygame.display.set_caption('坦克大战')  # 设置窗口标题
        self.clock = pygame.time.Clock()  # 创建时钟
        self.maxEnemy = 20  # 最大敌人数
        self.appearEnemy = 0  # 出现敌人数
        self.maxAppearEnemy = 5  # 最大出现敌人数
        self.level = 0  # 关卡数
        self.mapNum = 21  # 地图总数
        self.overY = 640
        self.isGameOver = False  # 游戏结束标志
        self.__init_sprites()  # 精灵组
        self.gameState = 0  # 游戏状态
        # 创建敌人事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 2000)

    def __init_sprites(self):
        # 游戏开始界面
        self.menu = Menu()
        self.menu_group = pygame.sprite.Group()
        # 地图
        self.map = Map()
        # 敌人坦克
        self.enemyTank_group = pygame.sprite.Group()
        # 玩家坦克
        self.player1_tank = PlayerTank(1)
        self.player1_tank.map = self.map
        self.player2_tank = PlayerTank(2)
        self.player2_tank.map = self.map
        self.player_tank_group = pygame.sprite.Group()
        # 道具
        self.props_group = pygame.sprite.Group()
        # 所有子弹组
        self.bullet_group = pygame.sprite.Group()

    def __startMenu(self):
        # 初始化
        screen.fill((0, 0, 0))
        self.isGameOver = False
        self.level = 0
        # 游戏开始界面
        self.menu_group.add(self.menu)
        self.menu_group.add(self.menu.select_tank_group)
        self.menu_group.update()
        self.menu_group.draw(screen)

    def __drawAll(self):
        # 设置游戏背景
        screen.fill((0, 0, 0), (0, 0, 624, 624))
        screen.fill((127, 127, 127), (624, 0, 688 - 624, 624))
        # 玩家
        if self.player1_tank.lives > 0:
            self.player_tank_group.add(self.player1_tank)
            tanks_group.add(self.player1_tank)
            self.bullet_group.add(self.player1_tank.bullet)
        if self.player2_tank.lives > 0:
            self.player_tank_group.add(self.player2_tank)
            tanks_group.add(self.player2_tank)
            self.bullet_group.add(self.player2_tank.bullet)

        # 添加敌人子弹
        for enemyTank in self.enemyTank_group:
            self.bullet_group.add(enemyTank.bullet)

        # 画地图
        self.map.mapGroup.update()
        self.map.mapGroup.draw(screen)
        self.map.drawRight(self.menu.playerNum, self.player1_tank.lives,
                           self.player2_tank.lives, self.maxEnemy)
        # 画所有坦克
        tanks_group.update()
        tanks_group.draw(screen)
        # 画所有子弹
        self.bullet_group.update()
        self.bullet_group.draw(screen)
        # 画所有道具
        self.props_group.update()
        self.props_group.draw(screen)

    def __check_collision(self):
        # 地图检测
        for map in self.map.mapGroup:
            for bullet in self.bullet_group:
                if pygame.sprite.collide_rect(bullet, map):
                    # 石头
                    if map in self.map.wallGroup:
                        self.map.wallGroup.remove(map)
                        map.kill()
                    # 子弹增强
                    if bullet.stronger:
                        if map in self.map.ironGroup:
                            self.map.ironGroup.remove(map)
                            map.kill()
                    # home
                    if map in self.map.homeGroup:
                        map.kill()
                        self.isGameOver = True
                    # 销毁
                    if (map not in self.map.grassGroup) and (map not in self.map.waterGroup) and \
                            (map not in self.map.iceGroup):
                        bullet.hit = True
                        self.bullet_group.remove(bullet)
                        break

        # 碰撞
        for enemyTank in self.enemyTank_group:
            for playerTank in self.player_tank_group:
                # 子弹碰撞子弹
                if pygame.sprite.collide_rect(playerTank.bullet, enemyTank.bullet):
                    playerTank.bullet.hit = True
                    enemyTank.bullet.hit = True

                # 玩家攻击敌人
                if enemyTank.isAppear:
                    if not enemyTank.isDestroyed:
                        if pygame.sprite.collide_rect(playerTank.bullet, enemyTank):
                            # 携带道具
                            if enemyTank.is_red:
                                self.props_group.add(enemyTank.prop)
                                enemyTank.is_red = False
                            # 攻击
                            if not playerTank.bullet.isDestroyed:
                                enemyTank.lives -= 1
                                playerTank.bullet.hit = True
                                self.bullet_group.remove(playerTank.bullet)

                            # 摧毁敌人坦克
                            if enemyTank.lives < 0:
                                enemyTank.destroy()
                                self.enemyTank_group.remove(enemyTank)
                                self.appearEnemy -= 1

                # 敌人攻击玩家
                if pygame.sprite.collide_rect(enemyTank.bullet, playerTank):

                    if playerTank.lives > 0 and not playerTank.isProtected:
                        # 摧毁玩家坦克
                        if not enemyTank.bullet.isDestroyed:
                            playerTank.destroy()
                            enemyTank.bullet.hit = True
                            self.bullet_group.remove(enemyTank.bullet)

                    # 游戏结束
                    if playerTank.lives < 0:
                        self.isGameOver = True

                # 道具
                if self.props_group:
                    for prop in self.props_group:
                        if pygame.sprite.collide_rect(playerTank, prop):
                            # 消灭当前所有敌人
                            if prop.kind == 0:
                                bang.play()
                                self.__killSprites(self.enemyTank_group)
                                self.maxEnemy -= self.appearEnemy
                                self.appearEnemy = 0
                            # 敌人静止
                            if prop.kind == 1:
                                for enemy in self.enemyTank_group:
                                    enemy.enemyStopTime = 500
                            # 子弹增强
                            if prop.kind == 2:
                                # 音效
                                add.play()
                                playerTank.bullet.stronger = True
                            # 使得大本营的墙变为钢板
                            if prop.kind == 3:
                                self.map.protect_time = 1000
                                self.map.protect_home()
                            # 坦克获得一段时间的保护罩
                            if prop.kind == 4:
                                # 音效
                                add.play()
                                playerTank.isProtected = True
                                playerTank.protectedTime = 500
                            # 坦克升级
                            if prop.kind == 5:
                                # 音效
                                add.play()
                                playerTank.level()
                            # 坦克生命+1
                            if prop.kind == 6:
                                # 音效
                                add.play()
                                playerTank.lives += 1
                            prop.hit = True
                            props.play()
                            self.props_group.remove(prop)
                            break

    def __killSprites(self, group):
        for sprite in group:
            sprite.kill()
        group.empty()

    def __level(self, l=1):
        self.level += l
        if self.level > self.mapNum:
            self.level = 1
        if self.level <= 0:
            self.level = self.mapNum

        # 只有一个玩家
        if self.menu.playerNum == 1:
            self.player2_tank.lives = 0

        # 切换地图清除所有精灵
        self.__killSprites(self.map.mapGroup)
        self.__killSprites(tanks_group)
        self.__killSprites(self.bullet_group)

        # 初始化数据
        self.map.init(self.level)
        self.player1_tank.init()
        self.maxEnemy = 20
        self.appearEnemy = 0
        if self.menu.playerNum == 2:
            self.player2_tank.init()

        # 初始化敌人(首先加载3个敌人)
        for i in range(0, 3):
            enemyTank = EnemyTank(i)
            enemyTank.map = self.map
            self.appearEnemy += 1
            self.maxEnemy -= 1
            self.enemyTank_group.add(enemyTank)
            tanks_group.add(enemyTank)

        self.gameState = GAME_STATE['GAME_INIT']

    def __game_over(self):
        screen.fill((0, 0, 0))
        # 图片
        image = pygame.image.load('./assets/images/others/game_over.png')
        screen.blit(image, (-130, self.overY))
        self.overY -= 2
        if self.overY < SCREEN_HEIGHT // 2 - 150:
            # 只有一个玩家
            if self.menu.playerNum == 1:
                self.player2_tank.lives = 0
            self.gameState = GAME_STATE['GAME_MENU']

    def _state_handler(self):
        if self.gameState == GAME_STATE['GAME_MENU']:
            # 开始界面
            self.__startMenu()
        elif self.gameState == GAME_STATE['GAME_INIT']:
            # 初始化
            if not self.map.isReady:
                # 初始化地图
                self.map.drawStage()
            else:
                self.gameState = GAME_STATE['GAME_START']
        elif self.gameState == GAME_STATE['GAME_START']:
            # 开始游戏
            self.__drawAll()
            # 游戏结束
            if self.isGameOver or (self.player1_tank.lives <= 0 and
                                   self.player2_tank.lives <= 0):
                self.gameState = GAME_STATE['GAME_OVER']
            # 消灭所有坦克 进入下一关
            if self.appearEnemy == self.maxEnemy and len(self.enemyTank_group) == 0:
                self.gameState = GAME_STATE['GAME_WIN']

        elif self.gameState == GAME_STATE['GAME_OVER']:
            # 游戏结束
            self.__game_over()
        elif self.gameState == GAME_STATE['GAME_WIN']:
            # 游戏胜利进入下一关
            self.__level()

    def __event_handler(self):
        for e in pygame.event.get():
            # 退出事件
            if e.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if self.gameState == GAME_STATE['GAME_START']:
                # 创建敌人事件
                if e.type == CREATE_ENEMY_EVENT:
                    # 创建敌人
                    if self.appearEnemy < self.maxAppearEnemy and self.maxEnemy > 0:
                        enemyTank = EnemyTank()
                        enemyTank.map = self.map
                        if not pygame.sprite.spritecollide(enemyTank, tanks_group, False):
                            self.appearEnemy += 1
                            self.maxEnemy -= 1
                            self.enemyTank_group.add(enemyTank)
                            tanks_group.add(enemyTank)

                # 松开方向键，坦克停止移动，修改坦克的开关状态
                if e.type == pygame.KEYUP:
                    # 判断松开的键停止坦克移动
                    if self.player1_tank.lives > 0:
                        if e.key == pygame.K_w or e.key == pygame.K_s or e.key == \
                                pygame.K_a or e.key == pygame.K_d:
                            self.player1_tank.isMoving = False
                    if self.player2_tank.lives > 0:
                        if e.key == pygame.K_UP or e.key == pygame.K_DOWN or e.key == \
                                pygame.K_LEFT or e.key == pygame.K_RIGHT:
                            self.player2_tank.isMoving = False

    def __KeyDown_handler(self):
        key = pygame.key.get_pressed()

        if self.gameState == GAME_STATE['GAME_MENU']:
            if key[pygame.K_RETURN]:
                # 进入游戏
                self.__level()
            else:
                # 选择
                if key[pygame.K_UP]:
                    self.menu.next(1)
                elif key[pygame.K_DOWN]:
                    self.menu.next(-1)
        elif self.gameState == GAME_STATE['GAME_START']:

            # 玩家按键检测
            if self.player1_tank.lives > 0:
                if key[pygame.K_w]:
                    self.player1_tank.dir = UP
                    self.player1_tank.isMoving = True
                elif key[pygame.K_s]:
                    self.player1_tank.dir = DOWN
                    self.player1_tank.isMoving = True
                elif key[pygame.K_a]:
                    self.player1_tank.dir = LEFT
                    self.player1_tank.isMoving = True
                elif key[pygame.K_d]:
                    self.player1_tank.dir = RIGHT
                    self.player1_tank.isMoving = True
                if key[pygame.K_SPACE]:
                    if not self.player1_tank.isShooting:
                        self.player1_tank.shoot()
                    if self.player1_tank.bullet.isDestroyed:
                        self.player1_tank.isShooting = False

            if self.player2_tank.lives > 0:
                if key[pygame.K_UP]:
                    self.player2_tank.dir = UP
                    self.player2_tank.isMoving = True
                elif key[pygame.K_DOWN]:
                    self.player2_tank.dir = DOWN
                    self.player2_tank.isMoving = True
                elif key[pygame.K_LEFT]:
                    self.player2_tank.dir = LEFT
                    self.player2_tank.isMoving = True
                elif key[pygame.K_RIGHT]:
                    self.player2_tank.dir = RIGHT
                    self.player2_tank.isMoving = True
                if key[pygame.K_RETURN]:
                    if not self.player2_tank.isShooting:
                        self.player2_tank.shoot()
                    if self.player2_tank.bullet.isDestroyed:
                        self.player2_tank.isShooting = False

            # 关卡切换
            if key[pygame.K_n]:
                self.__level()
            elif key[pygame.K_p]:
                self.__level(-1)

    def start_game(self):
        while True:
            # FPS
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 按键监听
            self.__KeyDown_handler()
            # 游戏状态监听
            self._state_handler()
            # 碰撞检测
            self.__check_collision()
            # 更新显示
            pygame.display.flip()


if __name__ == '__main__':
    Game = TankGame()
    Game.start_game()
