import pygame
import random
import os
import time  # 导入 time 模块

# 初始化 Pygame
pygame.init()

# 窗口设置
screen_width = 1280
screen_height = 760
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("HELLDIVERS™Ⅱ 战略装备模拟器")

# 颜色
white = (255, 255, 255)
black = (0, 0, 0)

# 字体
try:
    font = pygame.font.Font("./fonts/fz.ttf", 36)
    stratagem_font = pygame.font.Font("./fonts/fz.ttf", 24)
except pygame.error:
    print("Error: Could not load font. Make sure ./fonts/fz.ttf exists.")
    pygame.quit()
    exit()
try:
    icon = pygame.image.load("./icons/icon.png")
    pygame.display.set_icon(icon)
except pygame.error:
    print("Error: Could not load icon image. Make sure ./icons/icon.png exists.")

# 加载图片
def load_image(path):
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error:
        print(f"Error: Could not load image at {path}")
        pygame.quit()
        exit()

menu_image = load_image("./menu/helldivers.png")
menu_image = pygame.transform.scale(menu_image, (screen_width, screen_height))
arrow_images = {
    "up": load_image("./arrow/up.png"),
    "down": load_image("./arrow/down.png"),
    "left": load_image("./arrow/left.png"),
    "right": load_image("./arrow/right.png"),
}

# 加载声音
try:
    correct_sound = pygame.mixer.Sound("./sounds/right.mp3")
    wrong_sound = pygame.mixer.Sound("./sounds/wrong.mp3")
    confirm_sound = pygame.mixer.Sound("./sounds/confirm.mp3")
    main_theme = pygame.mixer.Sound("./music/main_theme1.mp3")
except pygame.error:
    print("Error: Could not load sound files. Check paths.")
    pygame.quit()
    exit()

# 创建 Channel (用于 correct_sound 重叠播放)
num_channels = 8
correct_channels = [pygame.mixer.Channel(i) for i in range(num_channels)]


# 题目数据
stratagems_sets = {
    "reinforce": [
        {"directions": ["up", "down", "right", "left", "up"], "image_path": "./stratagem/reinforce.png",
         "text": "增援"},
        {"directions": ["up", "down", "right", "up"], "image_path": "./stratagem/sos_beacon.png",
         "text": "SOS信标"},
        {"directions": ["down", "down", "up", "right"], "image_path": "./stratagem/resupply.png",
         "text": "重新补给"},
        {"directions": ["down", "up", "left", "down", "up", "right", "down", "up"], "image_path": "./stratagem/hellbomb.png",
         "text": "NUX-223“地狱火”炸弹"},
        {"directions": ["up", "up", "left", "up", "right"], "image_path": "./stratagem/eagle_rearm.png",
         "text": "重新武装飞鹰"},
    ],
    "eagle_airstrike": [
        {"directions": ["right", "down", "right", "down", "right", "down"],
         "image_path": "./stratagem/orbital_walking_barrage.png", "text": "轨道游走火力网"},
        {"directions": ["right", "down", "up", "right", "down"],
         "image_path": "./stratagem/orbital_laser.png", "text": "轨道激光炮"},
        {"directions": ["right", "right", "down", "left", "right", "down"],
         "image_path": "./stratagem/orbital_120mm_he_barrage.png", "text": "轨道120MM高爆弹火力网"},
        {"directions": ["right", "down", "up", "up", "left", "down", "down"],
         "image_path": "./stratagem/orbital_380mm_he_barrage.png", "text": "轨道380MM高爆弹火力网"},
        {"directions": ["right", "up", "down", "down", "right"],
         "image_path": "./stratagem/orbital_railcannon_strike.png", "text": "轨道炮攻击"},
        {"directions": ["right", "down", "left", "up", "up"],
         "image_path": "./stratagem/orbital_gatling_barrage.png", "text": "轨道加特林空袭"},
        {"directions": ["up", "right", "down", "down", "down"], "image_path": "./stratagem/eagle_500kg_bomb.png",
         "text": "“飞鹰”500KG炸弹"},
        {"directions": ["up", "right", "down", "right"], "image_path": "./stratagem/eagle_airstrike.png",
         "text": "“飞鹰”空袭"},
        {"directions": ["up", "right", "right"], "image_path": "./stratagem/eagle_strafing_run.png",
         "text": "“飞鹰”机枪扫射"},
        {"directions": ["up", "right", "down", "down", "right"], "image_path": "./stratagem/eagle_cluster_bomb.png",
         "text": "“飞鹰”集束炸弹"},
        {"directions": ["up", "right", "down", "up"], "image_path": "./stratagem/eagle_napalm_strike.png",
         "text": "“飞鹰”凝固汽油弹空袭"},
        {"directions": ["up", "right", "down", "up"], "image_path": "./stratagem/eagle_smoke_strike.png",
         "text": "“飞鹰”烟雾攻击"},
    ],
    "a_mg-43_machine_gun_sentry": [
        {"directions": ["down", "up", "right", "right", "up"],
         "image_path": "./stratagem/a_mg-43_machine_gun_sentry.png",
         "text": "哨戒机枪"},
        {"directions": ["down", "up", "left", "right", "right", "left"],
         "image_path": "./stratagem/e_mg-101_hmg_emplacement.png",
         "text": "重机枪部署支架"},
    ],
    "mg-43_machine_gun": [
        {"directions": ["down", "left", "down", "up", "right"], "image_path": "./stratagem/mg-43_machine_gun.png",
         "text": "机枪"},
        {"directions": ["down", "left", "right", "up", "down"],
         "image_path": "./stratagem/apw-1_anti-materiel_rifle.png",
         "text": "反器材步枪"},
    ]
}


# 游戏状态
class GameState:
    def __init__(self):
        self.state = "menu"
        self.current_stratagem_set_key = "reinforce"  # 初始题库
        self.last_stratagem = None  # 上一道题目
        self.new_stratagem()
        self.current_index = 0
        self.reset_arrows()
        self.fade_alpha = 255
        self.fading_in = True
        self.menu_text_alpha = 255  # 新增：菜单文字透明度
        self.menu_text_alpha_dir = -1  # 新增：透明度变化方向


        # 按钮信息
        self.buttons = []
        button_images = {
            "reinforce": load_image("./stratagem/reinforce.png"),
            "eagle_airstrike": load_image("./stratagem/eagle_airstrike.png"),
            "a_mg-43_machine_gun_sentry": load_image("./stratagem/a_mg-43_machine_gun_sentry.png"),
            "mg-43_machine_gun": load_image("./stratagem/mg-43_machine_gun.png"),
        }
        button_height = 80  # 假设按钮高度, 后续会根据实际图片大小调整
        button_spacing = 10
        start_y = 0

        button_total_height = 0
        for i, (key, image) in enumerate(button_images.items()):
            button_rect = image.get_rect(topleft=(20, 0))  # 临时设置 topleft, 稍后计算
            self.buttons.append({"rect": button_rect, "image": image, "key": key})
            button_total_height += button_rect.height + button_spacing

        button_total_height -= button_spacing
        start_y = (screen_height - button_total_height) // 2

        # 重新计算按钮位置
        current_y = start_y
        for button in self.buttons:
            button["rect"].topleft = (20, current_y)
            current_y += button["rect"].height + button_spacing



    def start_game(self):

        self.fading_in = False
        pygame.mixer.fadeout(1000)
        self.fade_alpha = 0
        self.state = "game"

    def new_stratagem(self):
        # 从当前选定的题库中选择题目，并确保与上一题不同
        available_stratagems = stratagems_sets[self.current_stratagem_set_key]

        # 如果题库中只有一道题, 就不用检查重复了.
        if len(available_stratagems) > 1:
             # 使用循环，直到选到与上一题不同的题目
            while True:
                new_stratagem = random.choice(available_stratagems)
                if new_stratagem != self.last_stratagem:
                    break
        else:
            new_stratagem = random.choice(available_stratagems)

        self.current_stratagem = new_stratagem
        self.last_stratagem = new_stratagem  # 更新上一道题目
        self.current_index = 0
        self.reset_arrows()

    def reset_arrows(self):
        self.arrow_alphas = [50] * len(self.current_stratagem["directions"])

    def check_input(self, direction):
        if (not self.current_stratagem or
                not self.current_stratagem["directions"] or
                self.current_index < 0 or
                self.current_index >= len(self.current_stratagem["directions"])):
            return

        if self.current_stratagem["directions"][self.current_index] == direction:
            self.arrow_alphas[self.current_index] = 255
            self.current_index += 1

            for channel in correct_channels:
                if not channel.get_busy():
                    channel.play(correct_sound)
                    break

            if self.current_index == len(self.current_stratagem["directions"]):
                confirm_sound.play()
                self.new_stratagem()
        else:
            wrong_sound.play()
            self.current_index = 0
            self.reset_arrows()

    def check_button_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                self.current_stratagem_set_key = button["key"]
                self.new_stratagem()  #切换题库后，也要防止新题目和上一题相同
                confirm_sound.play()
                return


# 渐入效果
def fade_in(screen, alpha):
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(black)
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))

# 渐出效果
def fade_out(screen, alpha):
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(black)
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))


game_state = GameState()

def draw_menu():
    screen.blit(menu_image, (0, 0))
    text_surface = font.render("按任意键启动游戏", True, white)
     # 设置文字透明度
    text_surface.set_alpha(game_state.menu_text_alpha)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(text_surface, text_rect)

def draw_game():
    if game_state.current_stratagem:
        #  垂直偏移量，用于调整题目图片的位置
        vertical_offset = 150

        stratagem_image = load_image(game_state.current_stratagem["image_path"])
        stratagem_rect = stratagem_image.get_rect(center=(screen_width // 2, 150 + vertical_offset))
        screen.blit(stratagem_image, stratagem_rect)

        name_surface = stratagem_font.render(game_state.current_stratagem["text"], True, white)
        name_rect = name_surface.get_rect(center=(screen_width // 2, stratagem_rect.bottom + 30))
        screen.blit(name_surface, name_rect)

        arrow_x = stratagem_rect.right + 20
        arrow_y = stratagem_rect.centery - arrow_images["up"].get_height() // 2

        for i, direction in enumerate(game_state.current_stratagem["directions"]):
            arrow_image = arrow_images[direction].copy()
            arrow_image.set_alpha(game_state.arrow_alphas[i])
            screen.blit(arrow_image, (arrow_x, arrow_y))
            arrow_x += arrow_image.get_width() + 10

     # 绘制按钮
    for button in game_state.buttons:
        screen.blit(button["image"], button["rect"])

# 主循环
running = True
main_theme.play(-1)
last_blink_time = time.time()  # 记录上次闪烁的时间

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state.state == "menu":
                game_state.start_game()
            elif game_state.state == "game":
                if event.key == pygame.K_UP:
                    game_state.check_input("up")
                elif event.key == pygame.K_DOWN:
                    game_state.check_input("down")
                elif event.key == pygame.K_LEFT:
                    game_state.check_input("left")
                elif event.key == pygame.K_RIGHT:
                    game_state.check_input("right")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.state == "game":
                game_state.check_button_click(event.pos)

    if game_state.state == "menu":
        if game_state.fading_in:
            game_state.fade_alpha -= 2
            if game_state.fade_alpha <= 0:
                game_state.fading_in = False
                game_state.fade_alpha = 0
            fade_in(screen, game_state.fade_alpha)

        # 菜单文字闪烁逻辑
        current_time = time.time()
        if current_time - last_blink_time >= 0.016:  # 每帧都更新，控制速度
            game_state.menu_text_alpha += game_state.menu_text_alpha_dir * 10 #可以调整闪烁速度
            if game_state.menu_text_alpha <= 0:
                game_state.menu_text_alpha_dir = 1  # 改变方向
                game_state.menu_text_alpha = 0

            elif game_state.menu_text_alpha >= 255:
                game_state.menu_text_alpha_dir = -1 #改变方向
                game_state.menu_text_alpha = 255
            last_blink_time = current_time

        draw_menu()


    elif game_state.state == "game":
      #渐出效果
        if game_state.fade_alpha < 255:
          game_state.fade_alpha += 5
          fade_out(screen,game_state.fade_alpha)
        else:
          screen.fill(black)
          draw_game()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()