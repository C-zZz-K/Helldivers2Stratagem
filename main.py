# main.py
import pygame
import random
import os
import sys  # 导入 sys 模块
import time

# --- 资源路径处理函数 (重要) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
gray = (128, 128, 128)  # 用于按钮的灰色

# 字体
try:
    font = pygame.font.Font(resource_path("fonts/fz.ttf"), 36)  # 使用 resource_path
    stratagem_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 24) # 使用 resource_path
    all_stratagems_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 20)  # 所有战略装备列表字体, 使用 resource_path
    input_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 30)  # 输入框字体, 使用 resource_path

except pygame.error:
    print("Error: Could not load font. Make sure ./fonts/fz.ttf exists.")
    pygame.quit()
    exit()
try:
    icon = pygame.image.load(resource_path("icons/icon.png")) # 使用 resource_path
    pygame.display.set_icon(icon)
except pygame.error:
    print("Error: Could not load icon image. Make sure ./icons/icon.png exists.")

# 加载图片 (使用 resource_path)
def load_image(path, alpha=255):
    try:
        image = pygame.image.load(resource_path(path)) # 使用 resource_path
        image.set_alpha(alpha)  # 设置整体透明度
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
favorite_icon = load_image("./icons/favorite.png")  # 收藏夹图标
back_arrow_image = load_image("./arrow/left.png") # 返回按钮的图片
# add_stratagem_set_icon = load_image("./icons/like.png")  # 不再使用图标

# 加载声音 (使用 resource_path)
try:
    correct_sound = pygame.mixer.Sound(resource_path("./sounds/right.mp3")) # 使用 resource_path
    wrong_sound = pygame.mixer.Sound(resource_path("./sounds/wrong.mp3"))  # 使用 resource_path
    confirm_sound = pygame.mixer.Sound(resource_path("./sounds/confirm.mp3"))  # 使用 resource_path
    main_theme = pygame.mixer.Sound(resource_path("./music/main_theme1.mp3"))  # 使用 resource_path
except pygame.error:
    print("Error: Could not load sound files. Check paths.")
    pygame.quit()
    exit()

# 创建 Channel (用于 correct_sound 重叠播放)
num_channels = 8
correct_channels = [pygame.mixer.Channel(i) for i in range(num_channels)]


# 题目数据 (图片路径不需要改，因为load_image函数里已经用了resource_path)
stratagems_sets = {
    "yellow": [
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
    "red": [
        {"directions": ["right", "right", "up"],
         "image_path": "./stratagem/orbital_precision_strike.png",
         "text": "轨道精准攻击"},
        {"directions": ["right", "down", "right", "down", "right", "down"],
         "image_path": "./stratagem/orbital_walking_barrage.png",
         "text": "轨道游走火力网"},
        {"directions": ["right", "right", "right"],
         "image_path": "./stratagem/orbital_airburst_strike.png",
         "text": "轨道空爆攻击"},
        {"directions": ["right", "down", "up", "right", "down"],
         "image_path": "./stratagem/orbital_laser.png",
         "text": "轨道激光炮"},
        {"directions": ["right", "right", "down", "left", "right", "down"],
         "image_path": "./stratagem/orbital_120mm_he_barrage.png",
         "text": "轨道120MM高爆弹火力网"},
        {"directions": ["right", "down", "up", "up", "left", "down", "down"],
         "image_path": "./stratagem/orbital_380mm_he_barrage.png",
         "text": "轨道380MM高爆弹火力网"},
        {"directions": ["right", "up", "down", "down", "right"],
         "image_path": "./stratagem/orbital_railcannon_strike.png",
         "text": "轨道炮攻击"},
        {"directions": ["right", "down", "left", "up", "up"],
         "image_path": "./stratagem/orbital_gatling_barrage.png",
         "text": "轨道加特林空袭"},
        {"directions": ["right", "right", "down", "right"],
         "image_path": "./stratagem/orbital_gas_strike.png",
         "text": "轨道毒气攻击"},
        {"directions": ["right", "right", "left", "down"],
         "image_path": "./stratagem/orbital_ems_strike.png",
         "text": "轨道电磁冲击波攻击"},
        {"directions": ["right", "right", "down", "up"],
         "image_path": "./stratagem/orbital_smoke_strike.png",
         "text": "轨道烟雾攻击"},
        {"directions": ["right", "right", "down", "left", "right", "up"],
         "image_path": "./stratagem/orbital_napalm_barrage.png",
         "text": "轨道凝固汽油火力网"},
        {"directions": ["up", "right", "down", "down", "down"],
         "image_path": "./stratagem/eagle_500kg_bomb.png",
         "text": "“飞鹰”500KG炸弹"},
        {"directions": ["up", "right", "down", "right"],
         "image_path": "./stratagem/eagle_airstrike.png",
         "text": "“飞鹰”空袭"},
        {"directions": ["up", "right", "right"],
         "image_path": "./stratagem/eagle_strafing_run.png",
         "text": "“飞鹰”机枪扫射"},
        {"directions": ["up", "right", "down", "down", "right"],
         "image_path": "./stratagem/eagle_cluster_bomb.png",
         "text": "“飞鹰”集束炸弹"},
        {"directions": ["up", "right", "down", "up"],
         "image_path": "./stratagem/eagle_napalm_strike.png",
         "text": "“飞鹰”凝固汽油弹空袭"},
        {"directions": ["up", "right", "up", "down"],
         "image_path": "./stratagem/eagle_smoke_strike.png",
         "text": "“飞鹰”烟雾攻击"},
        {"directions": ["up", "right", "up", "left"],
         "image_path": "./stratagem/eagle_110mm_rocket_pods.png",
         "text": "“飞鹰”110MM火箭巢"},
    ],
    "green": [
        {"directions": ["down", "up", "right", "right", "up"],
         "image_path": "./stratagem/a_mg-43_machine_gun_sentry.png",
         "text": "哨戒机枪"},
        {"directions": ["down", "up", "left", "right", "right", "left"],
         "image_path": "./stratagem/e_mg-101_hmg_emplacement.png",
         "text": "重机枪部署支架"},
    ],
    "blue": [
        {"directions": ["down", "left", "down", "up", "right"],
         "image_path": "./stratagem/mg-43_machine_gun.png",
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
        self.current_stratagem_set_key = "red"  # 初始题库
        self.last_stratagem = None  # 上一道题目
        self.current_index = 0
        # self.reset_arrows()
        self.fade_alpha = 255
        self.fading_in = True
        self.menu_text_alpha = 255
        self.menu_text_alpha_dir = -1
        self.all_stratagems_scroll_y = 0
        self.show_all_stratagems = False
        self.custom_stratagem_set_name = ""  # 修改初始值为空字符串
        self.creating_stratagem_set = False
        self.editing_stratagem_set = False
        self.custom_stratagems = {}
        self.new_stratagem()
        self.reset_arrows()
        self.custom_set_edit_state = {} # 新增：记录自定义题库编辑状态


        # 按钮信息
        self.buttons = []
        button_images = {
            "yellow": load_image("./stratagem/reinforce.png"),
            "red": load_image("./stratagem/eagle_airstrike.png"),
            "green": load_image("./stratagem/a_mg-43_machine_gun_sentry.png"),
            "blue": load_image("./stratagem/mg-43_machine_gun.png"),
        }
        button_height = 80
        button_spacing = 10
        start_y = 0

        button_total_height = 0
        for i, (key, image) in enumerate(button_images.items()):
            button_rect = image.get_rect(topleft=(20, 0))
            self.buttons.append({"rect": button_rect, "image": image, "key": key})
            button_total_height += button_rect.height + button_spacing

        button_total_height -= button_spacing
        start_y = (screen_height - button_total_height) // 2 + 40

        current_y = start_y
        for button in self.buttons:
            button["rect"].topleft = (20, current_y)
            current_y += button["rect"].height + button_spacing

        self.favorite_button_rect = favorite_icon.get_rect(topleft=(20, 80)) # 调整收藏夹图标位置
        # 返回按钮
        self.back_button_rect = back_arrow_image.get_rect(topleft=(20, 20))
        # self.add_stratagem_set_button_rect = add_stratagem_set_icon.get_rect(topleft=(20,140))  # 不再使用图标
        # 改为文字按钮
        self.add_stratagem_set_text = "新建题库"
        self.add_stratagem_set_button_rect = all_stratagems_font.render(self.add_stratagem_set_text, True, white).get_rect(topleft=(20, 140))

        self.custom_sets_buttons = []
        self.update_custom_sets_buttons()


    def start_game(self):
        self.fading_in = False
        pygame.mixer.fadeout(1000)
        self.fade_alpha = 0
        self.state = "game"

    def new_stratagem(self):
        #优先自定义题库
        if self.current_stratagem_set_key in self.custom_stratagems:
            available_stratagems = self.custom_stratagems[self.current_stratagem_set_key]
        else:
            available_stratagems = stratagems_sets[self.current_stratagem_set_key]

        if not available_stratagems:  # 如果自定义题库为空，则显示空
            self.current_stratagem = None
            self.reset_arrows()  # 确保箭头也被重置
            return

        if len(available_stratagems) > 1:
            while True:
                new_stratagem = random.choice(available_stratagems)
                if new_stratagem != self.last_stratagem:
                    break
        else:
            new_stratagem = random.choice(available_stratagems)

        self.current_stratagem = new_stratagem
        self.last_stratagem = new_stratagem
        self.current_index = 0
        self.reset_arrows()


    def reset_arrows(self):
        if self.current_stratagem:  # 确保有当前战略装备
            self.arrow_alphas = [50] * len(self.current_stratagem["directions"])
        else:
            self.arrow_alphas = []  # 如果没有战略装备，则箭头为空

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
        # 优先检查返回按钮
        if self.back_button_rect.collidepoint(pos):
            if self.state == "all_stratagems":
                 # 如果在自定义题库编辑状态，先退出编辑
                if self.editing_stratagem_set:
                    self.editing_stratagem_set = False
                    # 重置所有自定义题库编辑状态
                    for key in self.custom_set_edit_state:
                        self.custom_set_edit_state[key] = False

                self.state = "game"
                self.show_all_stratagems = False

                confirm_sound.play()
                return
            elif self.state == "game":  # game状态下也可返回
                self.state = "menu"
                main_theme.play(-1)
                confirm_sound.play()
                return
            elif self.state == "create_stratagem_set":
                self.state = "all_stratagems"
                self.creating_stratagem_set = False
                confirm_sound.play()
                return

        if self.state == "game":
            for button in self.buttons:
                if button["rect"].collidepoint(pos):
                    self.current_stratagem_set_key = button["key"]
                    self.new_stratagem()
                    confirm_sound.play()
                    return

            for button in self.custom_sets_buttons:  # 检查自定义题库按钮
                if button["rect"].collidepoint(pos):
                    self.current_stratagem_set_key = button["key"]
                    self.new_stratagem()
                    confirm_sound.play()
                    return

            if self.favorite_button_rect.collidepoint(pos):
                self.show_all_stratagems = True
                self.state = "all_stratagems"
                confirm_sound.play()
                return

        # 题库按钮点击
        if self.state == "all_stratagems" and self.add_stratagem_set_button_rect.collidepoint(pos):
            self.state = "create_stratagem_set"
            self.creating_stratagem_set = True
            self.custom_stratagem_set_name = ""  # 重置名称为空字符串
            confirm_sound.play()
            return

       # 自定义题库按钮点击事件（进入/退出编辑模式）
        if self.state == "all_stratagems":
            for button in self.custom_sets_buttons:
                if button["rect"].collidepoint(pos):
                    # 如果已经在编辑另一个题库，先退出那个题库的编辑模式
                    if self.editing_stratagem_set and self.current_stratagem_set_key != button["key"]:
                         self.custom_set_edit_state[self.current_stratagem_set_key] = False

                    # 切换编辑状态
                    self.custom_set_edit_state[button["key"]] = not self.custom_set_edit_state.get(button["key"], False)
                    self.editing_stratagem_set = self.custom_set_edit_state[button["key"]]
                    self.current_stratagem_set_key = button["key"]  # 记录当前编辑的题库
                    confirm_sound.play()
                    return

        #创建题库界面，取消和确定的按钮
        if self.state == "create_stratagem_set":
            if self.confirm_button_rect.collidepoint(pos): #确定按钮
                self.create_new_stratagem_set(self.custom_stratagem_set_name)
            elif self.cancel_button_rect.collidepoint(pos): #取消按钮
                self.state = "all_stratagems"
                self.creating_stratagem_set = False
                confirm_sound.play()

    def create_new_stratagem_set(self, name):
            if name and name not in self.custom_stratagems :  # 确保名称不为空且不重复
                self.custom_stratagems[name] = []
                self.current_stratagem_set_key = name  # 切换到新题库
                self.update_custom_sets_buttons()  # 更新按钮列表
                 # 初始化新题库的编辑状态
                self.custom_set_edit_state[name] = False
                self.state = "all_stratagems"
                self.creating_stratagem_set = False
                confirm_sound.play()

    def update_custom_sets_buttons(self):
        self.custom_sets_buttons = []
        button_spacing = 10
        current_y = 200 # 自定义题库按钮起始位置

        for key in self.custom_stratagems:
            text_surface = all_stratagems_font.render(key, True, white)
            button_rect = text_surface.get_rect(topleft=(20, current_y))
             # 默认设为不透明
            text_surface.set_alpha(255)
            self.custom_sets_buttons.append({"rect": button_rect, "key": key, "text_surface": text_surface})
            current_y += text_surface.get_height() + button_spacing

    def draw_all_stratagems_list(self):
        screen.fill(black)
        # 绘制返回按钮
        screen.blit(back_arrow_image, self.back_button_rect)
        # screen.blit(add_stratagem_set_icon, self.add_stratagem_set_button_rect) # 不再使用图标
        add_stratagem_set_surface = all_stratagems_font.render(self.add_stratagem_set_text, True, white)
        screen.blit(add_stratagem_set_surface, self.add_stratagem_set_button_rect)


        # 绘制自定义题库按钮, 根据编辑状态改变透明度
        for button in self.custom_sets_buttons:
            if self.custom_set_edit_state.get(button["key"], False):  # 如果处于编辑状态
                button["text_surface"].set_alpha(255)  # 设置为不透明
            else:
                button["text_surface"].set_alpha(128)  # 否则半透明  # 注释掉这行，改为不透明
            screen.blit(button["text_surface"], button["rect"])

        # 计算列表总高度
        total_height = 0
        for key in stratagems_sets:
            for stratagem in stratagems_sets[key]:
                image = load_image(stratagem["image_path"])
                text_surface = all_stratagems_font.render(stratagem["text"], True, white)
                total_height += max(image.get_height(), text_surface.get_height()) + 10

        # 计算垂直居中的起始 y 坐标
        start_y = (screen_height - total_height) // 2 + self.all_stratagems_scroll_y
        y_offset = start_y

        for key in stratagems_sets:
            for stratagem in stratagems_sets[key]:
                image = load_image(stratagem["image_path"], alpha=50 if self.editing_stratagem_set else 255)  # 编辑模式下调暗
                image_rect = image.get_rect(center=(screen_width // 2 -  all_stratagems_font.render(stratagem["text"], True, white).get_width() //2 -10, 50 + y_offset))

                text_surface = all_stratagems_font.render(stratagem["text"], True, white)
                #文本居中, 亮度调整
                text_rect = text_surface.get_rect(center=(screen_width // 2 + image.get_width()//2 + 10 , image_rect.centery))
                if self.editing_stratagem_set:
                   text_surface.set_alpha(50)
                else:
                   text_surface.set_alpha(255)


                # 如果在编辑模式, 且当前战略在自定义题库中，不高亮显示
                if (self.editing_stratagem_set and
                    self.current_stratagem_set_key in self.custom_stratagems and
                    stratagem in self.custom_stratagems[self.current_stratagem_set_key]):
                        image.set_alpha(255)
                        text_surface.set_alpha(255)


                screen.blit(image, image_rect)
                screen.blit(text_surface, text_rect)

                # 添加到/移出 自定义题库
                if self.editing_stratagem_set and image_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:  # 检测鼠标左键
                        if stratagem in self.custom_stratagems[self.current_stratagem_set_key]:
                            self.custom_stratagems[self.current_stratagem_set_key].remove(stratagem)
                            confirm_sound.play()
                            time.sleep(0.1) # 避免连续点击
                        elif stratagem not in self.custom_stratagems[self.current_stratagem_set_key]:
                            self.custom_stratagems[self.current_stratagem_set_key].append(stratagem)
                            confirm_sound.play()
                            time.sleep(0.1)

                y_offset += max(image_rect.height, text_rect.height) + 10


    def draw_create_stratagem_set_input(self):
        # 创建模糊背景 (在绘制输入框前绘制)
        screen.blit(pygame.Surface((screen_width, screen_height), pygame.SRCALPHA).convert_alpha(), (0, 0))
        background_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA) # 使用SRCALPHA创建带alpha通道的surface
        background_surface.fill((0, 0, 0, 128))  # 填充半透明黑色
        screen.blit(background_surface, (0, 0))


        # 输入框背景
        input_box_bg = pygame.Surface((600, 200))
        input_box_bg.fill(black)
        input_box_bg_rect = input_box_bg.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(input_box_bg, input_box_bg_rect)


        # 提示文字
        prompt_text = input_font.render("请输入新题库的名称:", True, white)
        prompt_rect = prompt_text.get_rect(midtop=(screen_width // 2, input_box_bg_rect.top + 20))
        screen.blit(prompt_text, prompt_rect)

        # 输入框
        input_rect = pygame.Rect(0, 0, 400, 50)
        input_rect.midtop = (screen_width // 2, prompt_rect.bottom + 20)
        pygame.draw.rect(screen, white, input_rect, 2)  # 绘制边框
        text_surface = input_font.render(self.custom_stratagem_set_name, True, white)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))


        # 确认和取消按钮
        button_width = 100
        button_height = 40
        button_spacing = 50

        # 确认按钮居左
        self.confirm_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.confirm_button_rect.topright = (input_rect.centerx - button_spacing // 2, input_rect.bottom + 20)
        pygame.draw.rect(screen, gray, self.confirm_button_rect)
        confirm_text = input_font.render("确认", True, white)
        confirm_text_rect = confirm_text.get_rect(center=self.confirm_button_rect.center)
        screen.blit(confirm_text, confirm_text_rect)

        # 取消按钮居右
        self.cancel_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.cancel_button_rect.topleft = (input_rect.centerx + button_spacing // 2, input_rect.bottom + 20)
        pygame.draw.rect(screen, gray, self.cancel_button_rect)
        cancel_text = input_font.render("取消", True, white)
        cancel_text_rect = cancel_text.get_rect(center=self.cancel_button_rect.center)
        screen.blit(cancel_text, cancel_text_rect)

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
    text_surface.set_alpha(game_state.menu_text_alpha)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(text_surface, text_rect)

def draw_game():
    screen.fill(black)  # 在draw_game里添加背景填充
    if game_state.current_stratagem:
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
    # 如果当前战略为空（自定义题库为空时）
    elif game_state.current_stratagem is None:
        empty_text = stratagem_font.render("题库为空", True, white)
        empty_rect = empty_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(empty_text, empty_rect)


    for button in game_state.buttons:
        screen.blit(button["image"], button["rect"])
    for button in game_state.custom_sets_buttons:  # 绘制自定义题库按钮
        screen.blit(button["text_surface"], button["rect"])
    screen.blit(favorite_icon, game_state.favorite_button_rect)
    screen.blit(back_arrow_image, game_state.back_button_rect)  # 绘制返回按钮


# 主循环
running = True
main_theme.play(-1)
last_blink_time = time.time()
pygame.key.start_text_input() # 开启文本输入

while running:
    for event in pygame.event.get():
        if game_state.state != "create_stratagem_set":
            # 原来事件处理代码
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
                game_state.check_button_click(event.pos)

            elif event.type == pygame.MOUSEWHEEL:
                if game_state.state == "all_stratagems":
                    game_state.all_stratagems_scroll_y += event.y * 20
        elif game_state.state == "create_stratagem_set":  # 创建界面时的事件处理
            if event.type == pygame.KEYDOWN:
                if game_state.creating_stratagem_set:  # 仅在创建状态下响应
                    if event.key == pygame.K_BACKSPACE:
                        game_state.custom_stratagem_set_name = game_state.custom_stratagem_set_name[:-1]
                    # 允许输入中文、字母、数字、下划线和空格
                    elif event.unicode.isalnum() or event.unicode == "_" or event.unicode == " " or '\u4e00' <= event.unicode <= '\u9fff':  # 添加中文范围
                        if len(game_state.custom_stratagem_set_name) < 20:  # 限制名称长度
                            game_state.custom_stratagem_set_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 增加鼠标点击事件
                game_state.check_button_click(event.pos)  # 复用check_button_click函数
        elif event.type == pygame.QUIT:
            running = False

    if game_state.state == "menu":
        if game_state.fading_in:
            game_state.fade_alpha -= 2
            if game_state.fade_alpha <= 0:
                game_state.fading_in = False
                game_state.fade_alpha = 0
            fade_in(screen, game_state.fade_alpha)

        current_time = time.time()
        if current_time - last_blink_time >= 0.016:
            game_state.menu_text_alpha += game_state.menu_text_alpha_dir * 10
            if game_state.menu_text_alpha <= 0:
                game_state.menu_text_alpha_dir = 1
                game_state.menu_text_alpha = 0
            elif game_state.menu_text_alpha >= 255:
                game_state.menu_text_alpha_dir = -1
                game_state.menu_text_alpha = 255
            last_blink_time = current_time

        draw_menu()

    elif game_state.state == "game":
        if game_state.fade_alpha < 255:
            game_state.fade_alpha += 5
            fade_out(screen, game_state.fade_alpha)
        else:
            draw_game()

    elif game_state.state == "all_stratagems":
        game_state.draw_all_stratagems_list()

    elif game_state.state == "create_stratagem_set":
        game_state.draw_create_stratagem_set_input()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
