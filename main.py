# main.py
import pygame
import random
import os
import sys
import time
import tkinter as tk
from tkinter import simpledialog, Toplevel


# --- 资源路径处理函数 ---
def resource_path(relative_path):
    try:
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
gray = (128, 128, 128)

# 字体
try:
    font = pygame.font.Font(resource_path("fonts/fz.ttf"), 36)
    stratagem_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 24)
    all_stratagems_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 20)
    input_font = pygame.font.Font(resource_path("fonts/fz.ttf"), 30)

except pygame.error:
    print("Error: Could not load font.")
    pygame.quit()
    exit()
try:
    icon = pygame.image.load(resource_path("icons/icon.png"))
    pygame.display.set_icon(icon)
except pygame.error:
    print("Error: Could not load icon image.")


# 加载图片
def load_image(path, alpha=255):
    try:
        image = pygame.image.load(resource_path(path))
        image.set_alpha(alpha)
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
favorite_icon = load_image("./icons/favorite.png")
back_arrow_image = load_image("./arrow/left.png")

# 加载声音
try:
    correct_sound = pygame.mixer.Sound(resource_path("./sounds/right.mp3"))
    wrong_sound = pygame.mixer.Sound(resource_path("./sounds/wrong.mp3"))
    confirm_sound = pygame.mixer.Sound(resource_path("./sounds/confirm.mp3"))
    main_theme = pygame.mixer.Sound(resource_path("./music/main_theme1.mp3"))
except pygame.error:
    print("Error: Could not load sound files.")
    pygame.quit()
    exit()

# 创建 Channel
num_channels = 8
correct_channels = [pygame.mixer.Channel(i) for i in range(num_channels)]

# 题目数据
stratagems_sets = {
    "yellow": [
        {"directions": ["up", "down", "right", "left", "up"],
         "image_path": "./stratagem/reinforce.png",
         "text": "增援"},
        {"directions": ["up", "down", "right", "up"],
         "image_path": "./stratagem/sos_beacon.png",
         "text": "SOS信标"},
        {"directions": ["down", "down", "up", "right"],
         "image_path": "./stratagem/resupply.png",
         "text": "重新补给"},
        {"directions": ["down", "up", "left", "down", "up", "right", "down", "up"],
         "image_path": "./stratagem/hellbomb.png",
         "text": "地狱火炸弹"},
        {"directions": ["up", "up", "left", "up", "right"],
         "image_path": "./stratagem/eagle_rearm.png",
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
         "text": "轨道120MM高爆弹"},
        {"directions": ["right", "down", "up", "up", "left", "down", "down"],
         "image_path": "./stratagem/orbital_380mm_he_barrage.png",
         "text": "轨道380MM高爆弹"},
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
         "text": "轨道电磁冲击波"},
        {"directions": ["right", "right", "down", "up"],
         "image_path": "./stratagem/orbital_smoke_strike.png",
         "text": "轨道烟雾攻击"},
        {"directions": ["right", "right", "down", "left", "right", "up"],
         "image_path": "./stratagem/orbital_napalm_barrage.png",
         "text": "轨道凝固汽油"},
        {"directions": ["up", "right", "down", "down", "down"],
         "image_path": "./stratagem/eagle_500kg_bomb.png",
         "text": "500KG炸弹"},
        {"directions": ["up", "right", "down", "right"],
         "image_path": "./stratagem/eagle_airstrike.png",
         "text": "飞鹰空袭"},
        {"directions": ["up", "right", "right"],
         "image_path": "./stratagem/eagle_strafing_run.png",
         "text": "飞鹰机枪扫射"},
        {"directions": ["up", "right", "down", "down", "right"],
         "image_path": "./stratagem/eagle_cluster_bomb.png",
         "text": "飞鹰集束炸弹"},
        {"directions": ["up", "right", "down", "up"],
         "image_path": "./stratagem/eagle_napalm_strike.png",
         "text": "飞鹰凝固汽油弹"},
        {"directions": ["up", "right", "up", "down"],
         "image_path": "./stratagem/eagle_smoke_strike.png",
         "text": "飞鹰烟雾攻击"},
        {"directions": ["up", "right", "up", "left"],
         "image_path": "./stratagem/eagle_110mm_rocket_pods.png",
         "text": "飞鹰110MM火箭巢"},
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


class GameState:
    def __init__(self):
        self.state = "menu"
        self.current_stratagem_set_key = "red"
        self.last_stratagem = None
        self.current_index = 0
        self.fade_alpha = 255
        self.fading_in = True
        self.menu_text_alpha = 255
        self.menu_text_alpha_dir = -1
        self.all_stratagems_scroll_y = 0
        self.show_all_stratagems = False
        self.custom_stratagem_set_name = ""
        self.creating_stratagem_set = False
        self.editing_stratagem_set = False
        self.custom_stratagems = {}
        self.new_stratagem()
        self.reset_arrows()
        self.custom_set_edit_state = {}

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

        self.favorite_button_rect = favorite_icon.get_rect(topleft=(20, 80))
        self.back_button_rect = back_arrow_image.get_rect(topleft=(20, 20))
        self.add_stratagem_set_text = "新建战略装备集合"
        self.add_stratagem_set_button_rect = all_stratagems_font.render(self.add_stratagem_set_text, True,
                                                                        white).get_rect(topleft=(20, 140))

        self.custom_sets_buttons = []
        self.update_custom_sets_buttons()

        # Tkinter 根窗口 (延迟创建)
        self.root = None

    def _get_tkinter_root(self):
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()  # 隐藏根窗口
        return self.root

    def start_game(self):
        self.fading_in = False
        pygame.mixer.fadeout(1000)
        self.fade_alpha = 0
        self.state = "game"

    def new_stratagem(self):
        if self.current_stratagem_set_key in self.custom_stratagems:
            available_stratagems = self.custom_stratagems[self.current_stratagem_set_key]
        else:
            available_stratagems = stratagems_sets[self.current_stratagem_set_key]

        if not available_stratagems:
            self.current_stratagem = None
            self.reset_arrows()
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
        if self.current_stratagem:
            self.arrow_alphas = [50] * len(self.current_stratagem["directions"])
        else:
            self.arrow_alphas = []

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

    def _create_tkinter_input(self):
        root = self._get_tkinter_root()  # 获取 Tkinter 根窗口
        root.overrideredirect(True) # 绕过窗口管理器

        # 创建一个顶层窗口
        top = Toplevel(root)
        top.title("新建战略装备集合")
        top.attributes('-topmost', True)  # 使其置顶
        top.geometry('300x100+200+200')
        top.lift()

        def on_confirm():
            nonlocal input_text
            input_text = entry.get()
            top.destroy()
            if input_text:  # 确保输入不为空
                self.custom_stratagem_set_name = input_text
                self.create_new_stratagem_set(self.custom_stratagem_set_name)
            else:
                self.state = "all_stratagems"
                self.creating_stratagem_set = False
                confirm_sound.play()

        def on_cancel():
            nonlocal input_text
            input_text = None
            top.destroy()
            self.state = "all_stratagems"
            self.creating_stratagem_set = False
            confirm_sound.play()

        # 绑定窗口关闭事件
        top.protocol("WM_DELETE_WINDOW", on_cancel)

        label = tk.Label(top, text="请输入新的战备集名称:")
        label.pack(pady=5)

        entry = tk.Entry(top)
        entry.pack(pady=5)
        entry.focus_set()  # 设置输入框为焦点

        input_text = None  # 初始化

        confirm_button = tk.Button(top, text="确定", command=on_confirm)
        confirm_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(top, text="取消", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        root.wait_window(top)  # 等待顶层窗口关闭

    def check_button_click(self, pos):
        if self.back_button_rect.collidepoint(pos):
            if self.state == "all_stratagems":
                if self.editing_stratagem_set:
                    self.editing_stratagem_set = False
                    for key in self.custom_set_edit_state:
                        self.custom_set_edit_state[key] = False

                self.state = "game"
                self.show_all_stratagems = False
                confirm_sound.play()
                return
            elif self.state == "game":
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

            for button in self.custom_sets_buttons:
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

        if self.state == "all_stratagems" and self.add_stratagem_set_button_rect.collidepoint(pos):
            self.state = "create_stratagem_set"
            self.creating_stratagem_set = True
            self.custom_stratagem_set_name = ""
            self._create_tkinter_input()
            return

        if self.state == "all_stratagems":
            for button in self.custom_sets_buttons:
                if button["rect"].collidepoint(pos):
                    if self.editing_stratagem_set and self.current_stratagem_set_key != button["key"]:
                        self.custom_set_edit_state[self.current_stratagem_set_key] = False

                    self.custom_set_edit_state[button["key"]] = not self.custom_set_edit_state.get(button["key"], False)
                    self.editing_stratagem_set = self.custom_set_edit_state[button["key"]]
                    self.current_stratagem_set_key = button["key"]
                    confirm_sound.play()
                    return

    def create_new_stratagem_set(self, name):
        if name and name not in self.custom_stratagems:
            self.custom_stratagems[name] = []
            self.current_stratagem_set_key = name
            self.update_custom_sets_buttons()
            self.custom_set_edit_state[name] = False
            self.state = "all_stratagems"
            self.creating_stratagem_set = False
            confirm_sound.play()

    def update_custom_sets_buttons(self):
        self.custom_sets_buttons = []
        button_spacing = 10
        current_y = 200

        for key in self.custom_stratagems:
            text_surface = all_stratagems_font.render(key, True, white)
            button_rect = text_surface.get_rect(topleft=(20, current_y))
            text_surface.set_alpha(255)
            self.custom_sets_buttons.append({"rect": button_rect, "key": key, "text_surface": text_surface})
            current_y += text_surface.get_height() + button_spacing

    def draw_all_stratagems_list(self):
        screen.fill(black)
        screen.blit(back_arrow_image, self.back_button_rect)
        add_stratagem_set_surface = all_stratagems_font.render(self.add_stratagem_set_text, True, white)
        screen.blit(add_stratagem_set_surface, self.add_stratagem_set_button_rect)

        for button in self.custom_sets_buttons:
            if self.custom_set_edit_state.get(button["key"], False):
                button["text_surface"].set_alpha(255)
            else:
                button["text_surface"].set_alpha(128)
            screen.blit(button["text_surface"], button["rect"])

        total_height = 0
        for key in stratagems_sets:
            for stratagem in stratagems_sets[key]:
                image = load_image(stratagem["image_path"])
                text_surface = all_stratagems_font.render(stratagem["text"], True, white)
                total_height += max(image.get_height(), text_surface.get_height()) + 10

        start_y = (screen_height - total_height) // 2 + self.all_stratagems_scroll_y
        y_offset = start_y

        for key in stratagems_sets:
            for stratagem in stratagems_sets[key]:
                image = load_image(stratagem["image_path"], alpha=50 if self.editing_stratagem_set else 255)
                image_rect = image.get_rect(center=(
                screen_width // 2 - all_stratagems_font.render(stratagem["text"], True, white).get_width() // 2 - 10,
                50 + y_offset))

                text_surface = all_stratagems_font.render(stratagem["text"], True, white)
                text_rect = text_surface.get_rect(
                    center=(screen_width // 2 + image.get_width() // 2 + 10, image_rect.centery))
                if self.editing_stratagem_set:
                    text_surface.set_alpha(50)
                else:
                    text_surface.set_alpha(255)

                if (self.editing_stratagem_set and
                        self.current_stratagem_set_key in self.custom_stratagems and
                        stratagem in self.custom_stratagems[self.current_stratagem_set_key]):
                    image.set_alpha(255)
                    text_surface.set_alpha(255)

                screen.blit(image, image_rect)
                screen.blit(text_surface, text_rect)

                if self.editing_stratagem_set and image_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        if stratagem in self.custom_stratagems[self.current_stratagem_set_key]:
                            self.custom_stratagems[self.current_stratagem_set_key].remove(stratagem)
                            confirm_sound.play()
                            time.sleep(0.1)
                        elif stratagem not in self.custom_stratagems[self.current_stratagem_set_key]:
                            self.custom_stratagems[self.current_stratagem_set_key].append(stratagem)
                            confirm_sound.play()
                            time.sleep(0.1)

                y_offset += max(image_rect.height, text_rect.height) + 10

    def draw_create_stratagem_set_input(self):
        pass


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
    text_surface = font.render("按任意键进行游戏", True, white)
    text_surface.set_alpha(game_state.menu_text_alpha)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(text_surface, text_rect)


def draw_game():
    screen.fill(black)
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

    elif game_state.current_stratagem is None:
        empty_text = stratagem_font.render("该战略集合为空", True, white)
        empty_rect = empty_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(empty_text, empty_rect)

    for button in game_state.buttons:
        screen.blit(button["image"], button["rect"])
    for button in game_state.custom_sets_buttons:
        screen.blit(button["text_surface"], button["rect"])
    screen.blit(favorite_icon, game_state.favorite_button_rect)
    screen.blit(back_arrow_image, game_state.back_button_rect)


# 主循环
running = True
main_theme.play(-1)
last_blink_time = time.time()

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
            game_state.check_button_click(event.pos)

        elif event.type == pygame.MOUSEWHEEL:
            if game_state.state == "all_stratagems":
                game_state.all_stratagems_scroll_y += event.y * 20

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
        pass

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()