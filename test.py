# 导入所需模块
import pygame
import random
import os
import sys
import configparser

# 获取主程序所在目录的路径
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# 初始化pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HELLDIVERS™2")

# 设置窗口图标
icon_path = os.path.join(BASE_DIR, "icons", "icon.png")
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 加载箭头图片
ARROW_DIR = os.path.join(BASE_DIR, "arrow")
arrow_images = {
    "up": pygame.image.load(os.path.join(ARROW_DIR, "up.png")),
    "down": pygame.image.load(os.path.join(ARROW_DIR, "down.png")),
    "left": pygame.image.load(os.path.join(ARROW_DIR, "left.png")),
    "right": pygame.image.load(os.path.join(ARROW_DIR, "right.png"))
}

# 加载开始界面背景图片
MENU_DIR = os.path.join(BASE_DIR, "menu")
menu_background = pygame.image.load(os.path.join(MENU_DIR, "helldivers.png"))

# 加载音效
RIGHT_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "right.mp3"))
WRONG_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "wrong.mp3"))
CONFIRM_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "confirm.mp3"))

# 定义箭头、图片和文字描述的起始位置的坐标
ARROW_START_X = 500
ARROW_START_Y = HEIGHT // 2 - 50
IMAGE_START_X = 425
IMAGE_START_Y = HEIGHT // 2 - 50
TEXT_START_X = 485
TEXT_START_Y = 2 + 355

# 加载字体
FONT_DIR = os.path.join(BASE_DIR, "fonts")
FONT_PATH = os.path.join(FONT_DIR, "msyh.ttc")
font = pygame.font.Font(FONT_PATH, 18)

# 定义游戏题库，包含每个题目及其对应的图片路径和文字描述
QUESTIONS = [
    {"directions": ["up", "down", "right", "left", "up"], "image_path": "./stratagem/reinforce.png",
     "text": "增援"},
    {"directions": ["up", "down", "right", "up"], "image_path": "./stratagem/sos_beacon.png",
     "text": "SOS信标"},
    {"directions": ["down", "down", "up", "right"], "image_path": "./stratagem/resupply.png",
     "text": "重新补给"},
]

QUESTIONS2 = [
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
]

QUESTIONS3 = [
    {"directions": ["down", "up", "right", "right", "up"],
     "image_path": "./stratagem/a_mg-43_machine_gun_sentry.png",
     "text": "哨戒机枪"},
    {"directions": ["down", "up", "left", "right", "right", "left"], "image_path": "./stratagem/e_mg-101_hmg_emplacement.png",
     "text": "重机枪部署支架"},

]

QUESTIONS4 = [
    {"directions": ["down", "left", "down", "up", "right"], "image_path": "./stratagem/mg-43_machine_gun.png",
     "text": "机枪"},
    {"directions": ["down", "left", "right", "up", "down"], "image_path": "./stratagem/apw-1_anti-materiel_rifle.png",
     "text": "反器材步枪"},
]

FAVORITE_QUESTIONS = []

last_question_index = None  # 用于存储上一个题目的索引

# 定义背景音乐的淡入淡出函数
def fade_music_in(music, volume_increment=0.01, max_volume=1.0):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(0.0)  # 初始化音量为0
    pygame.mixer.music.play(-1)  # 循环播放
    current_volume = 0.0
    while current_volume < max_volume:
        pygame.mixer.music.set_volume(current_volume)
        current_volume += volume_increment
        pygame.time.delay(10)

def fade_music_out(volume_decrement=0.01):
    current_volume = pygame.mixer.music.get_volume()
    while current_volume > 0.0:
        pygame.mixer.music.set_volume(current_volume)
        current_volume -= volume_decrement
        pygame.time.delay(10)
    pygame.mixer.music.stop()

def draw_arrow(arrow, x, y, alpha=128):
    """根据箭头类型绘制箭头"""
    arrow_image = arrow_images[arrow]
    arrow_image.set_alpha(alpha)  # 设置箭头图片的透明度
    WIN.blit(arrow_image, (x, y))

def display_message(message, font, x, y, alpha=255):
    """显示消息"""
    text = font.render(message, True, WHITE)
    text.set_alpha(alpha)  # 设置文本透明度
    WIN.blit(text, (x, y))

class Button:
    def __init__(self, image_path, text, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.alpha = 128  # 默认按钮透明度为50%
        self.text = text  # 按钮描述文字

    def draw(self, win):
        self.image.set_alpha(self.alpha)  # 设置按钮图片的透明度
        win.blit(self.image, self.rect)
        display_message(self.text, font, self.rect.right + 10, self.rect.centery - 10, self.alpha)  # 绘制按钮描述文字

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

def main_menu():
    """开始界面"""
    instruction_font = pygame.font.Font(FONT_PATH, 25)

    # 显示版本号
    version_font = pygame.font.Font(None, 20)
    version_text = version_font.render("ver 1.21", True, WHITE)

    # 随机选择背景音乐
    bg_music_list = ["./music/main_theme1.mp3"]
    selected_bg_music = random.choice(bg_music_list)

    # 播放背景音乐并淡入
    fade_music_in(selected_bg_music, volume_increment=0.01, max_volume=0.5)

    # 控制闪烁效果的变量
    alpha = 0
    increasing = True

    while alpha < 255:
        WIN.fill(BLACK)
        menu_background.set_alpha(alpha)
        WIN.blit(menu_background, (0, 0))
        display_message("按任意键开始游戏", instruction_font, WIDTH // 2 - 100, HEIGHT // 2 + 250, 255)
        WIN.blit(version_text, (WIDTH - 100, HEIGHT - 30))  # 绘制版本号
        pygame.display.update()

        if increasing:
            alpha += 3  # 透明度增加
            if alpha >= 255:
                increasing = False
        else:
            alpha -= 3  # 透明度减少
            if alpha <= 0:
                break

    while True:
        WIN.blit(menu_background, (0, 0))
        # 闪烁效果
        if increasing:
            alpha += 3  # 透明度增加
            if alpha >= 255:
                increasing = False
        else:
            alpha -= 3  # 透明度减少
            if alpha <= 128:
                increasing = True

        display_message("按任意键开始游戏", instruction_font, WIDTH // 2 - 100, HEIGHT // 2 + 250, alpha)
        WIN.blit(version_text, (WIDTH - 100, HEIGHT - 30))  # 绘制版本号
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # 播放确认音效
                CONFIRM_SOUND.play()
                # 淡出背景音乐
                fade_music_out(volume_decrement=0.01)
                # 淡出背景图片和文本
                alpha = 255
                while alpha > 0:
                    WIN.fill(BLACK)
                    menu_background.set_alpha(alpha)
                    WIN.blit(menu_background, (0, 0))
                    display_message("按任意键开始游戏", instruction_font, WIDTH // 2 - 100, HEIGHT // 2 + 250, alpha)
                    WIN.blit(version_text, (WIDTH - 100, HEIGHT - 30))  # 绘制版本号
                    pygame.display.update()
                    alpha -= 17  # 每次减少17，大约半秒完成淡出
                return

def write_to_config_file(questions):
    config = configparser.ConfigParser()
    config['Favorites'] = {}

    for i, question in enumerate(questions):
        section_name = f"Question_{i+1}"
        config['Favorites'][f"directions_{i+1}"] = ','.join(question['directions'])
        config['Favorites'][f"image_path_{i+1}"] = question['image_path']
        config['Favorites'][f"text_{i+1}"] = question['text']

    with open('favorites_config.ini', 'w') as configfile:
        config.write(configfile)

def stratagem_page():
    """显示stratagem页面"""
    global QUESTION5  # 引用全局变量 QUESTION5
    # 创建返回按钮
    return_button = Button("./arrow/left.png", "返回", 20, 20)
    running = True

    # 收藏界面的起始坐标
    collection_start_x = 450
    collection_start_y = 50
    pixel_spacing = 60  # 间隔像素
    scroll_speed = 10  # 滚动速度

    # 存储已收藏题目的索引
    favorite_indices = []

    # 跟踪左键状态
    left_mouse_down = False

    while running:
        WIN.fill(BLACK)
        return_button.draw(WIN)

        # 遍历所有题库，将题目内容陈列在收藏界面
        current_y = collection_start_y
        for index, question_set in enumerate([QUESTIONS, QUESTIONS2, QUESTIONS3, QUESTIONS4]):
            for question_index, question in enumerate(question_set):
                image_path = question["image_path"]
                question_image = pygame.image.load(image_path)
                # 计算题目图片的位置和范围
                question_rect = question_image.get_rect(topleft=(collection_start_x, current_y))
                WIN.blit(question_image, question_rect)
                # 绘制文字描述，放置在图片右侧居中显示
                display_message(question["text"], font, collection_start_x + 80, current_y)

                # 检查是否点击了题目图片
                if question_rect.collidepoint(pygame.mouse.get_pos()):
                    # 鼠标左键按下
                    if pygame.mouse.get_pressed()[0] and not left_mouse_down:
                        left_mouse_down = True
                        # 获取当前题目在列表中的索引
                        question_index_global = index * len(question_set) + question_index
                        # 如果未收藏，则收藏
                        if question_index_global not in favorite_indices:
                            favorite_indices.append(question_index_global)
                            FAVORITE_QUESTIONS.append(question)  # 将当前题目添加到收藏的题目列表中
                        else:
                            # 如果已收藏，则取消收藏
                            favorite_indices.remove(question_index_global)
                            if question in FAVORITE_QUESTIONS:
                                FAVORITE_QUESTIONS.remove(question)
                        # 调用写入配置文件的函数，将收藏的题目写入配置文件
                        write_to_config_file(FAVORITE_QUESTIONS)
                    # 鼠标左键松开
                    elif not pygame.mouse.get_pressed()[0] and left_mouse_down:
                        left_mouse_down = False

                # 绘制收藏图标
                if index * len(question_set) + question_index in favorite_indices:
                    like_image = pygame.image.load("./icons/like.png")
                    like_rect = like_image.get_rect(topleft=(collection_start_x - 35, current_y + 15))
                    WIN.blit(like_image, like_rect)

                current_y += pixel_spacing

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if return_button.is_over(pos):
                    # 播放确认音效
                    CONFIRM_SOUND.play()
                    return
            elif event.type == pygame.MOUSEWHEEL:  # 监听鼠标滚轮事件
                if event.y > 0:  # 鼠标滚轮向上滚动
                    collection_start_y += scroll_speed
                elif event.y < 0:  # 鼠标滚轮向下滚动
                    collection_start_y -= scroll_speed


def main():
    global current_question, current_input, alpha, switch_time, last_question_index, QUESTION5
    clock = pygame.time.Clock()
    running = True
    current_question = []
    current_input = []
    alpha = []
    switch_time = 0  # 记录切换题目的时间
    main_menu()  # 显示开始界面

    # 创建按钮
    buttons = [
        Button("./stratagem/reinforce.png", "任务", WIDTH - 1200, 60),
        Button("./stratagem/eagle_strafing_run.png", "进攻", WIDTH - 1200, 150),
        Button("./stratagem/a_mg-43_machine_gun_sentry.png", "防御", WIDTH - 1200, 240),
        Button("./stratagem/mg-43_machine_gun.png", "补给", WIDTH - 1200, 330),
        Button("./icons/favorite.png", "所有", WIDTH - 120, 60),
        Button("./icons/favorite.png", "收藏", WIDTH - 1200, 420)
    ]

    current_question_set = QUESTIONS  # 初始使用题库1
    last_question_index = None

    while running:
        WIN.fill(BLACK)  # 清空窗口

        # 绘制按钮
        for button in buttons:
            button.draw(WIN)

        # 处理事件
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if len(current_input) < len(current_question) and current_question[len(current_input)] == "up":
                        current_input.append("up")
                        alpha[len(current_input) - 1] = 255  # 恢复透明度为100%
                        RIGHT_SOUND.play()  # 播放正确音效
                    else:
                        current_input = []  # 如果按错，重置输入
                        alpha = [128] * len(current_question)  # 重置透明度列表为50%
                        WRONG_SOUND.play()  # 播放错误音效
                elif event.key == pygame.K_DOWN:
                    if len(current_input) < len(current_question) and current_question[len(current_input)] == "down":
                        current_input.append("down")
                        alpha[len(current_input) - 1] = 255
                        RIGHT_SOUND.play()
                    else:
                        current_input = []
                        alpha = [128] * len(current_question)
                        WRONG_SOUND.play()
                elif event.key == pygame.K_LEFT:
                    if len(current_input) < len(current_question) and current_question[len(current_input)] == "left":
                        current_input.append("left")
                        alpha[len(current_input) - 1] = 255
                        RIGHT_SOUND.play()
                    else:
                        current_input = []
                        alpha = [128] * len(current_question)
                        WRONG_SOUND.play()
                elif event.key == pygame.K_RIGHT:
                    if len(current_input) < len(current_question) and current_question[len(current_input)] == "right":
                        current_input.append("right")
                        alpha[len(current_input) - 1] = 255
                        RIGHT_SOUND.play()
                    else:
                        current_input = []
                        alpha = [128] * len(current_question)
                        WRONG_SOUND.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_over(pos):
                        # 播放确认音效
                        CONFIRM_SOUND.play()
                        if i == 4:  # 新按钮的索引
                            stratagem_page()  # 跳转到stratagem页面
                        else:
                            current_question_set = [QUESTIONS, QUESTIONS2, QUESTIONS3, QUESTIONS4][i]  # 更新当前题库
                            question_index = random.randint(0, len(current_question_set) - 1)  # 更新question_index
                            current_question = current_question_set[question_index]["directions"]
                            alpha.extend([128] * (len(current_question) - len(alpha)))  # 更新alpha列表长度
                            # 更新按钮透明度
                            for btn in buttons:
                                btn.alpha = 128  # 先将所有按钮透明度设置为50%
                            buttons[i].alpha = 255  # 再将当前按钮透明度设置为100%
                            break

        # 检查当前输入是否正确
        if current_input == current_question[:len(current_input)]:
            if len(current_input) == len(current_question):
                if switch_time == 0:
                    switch_time = pygame.time.get_ticks()  # 记录切换题目的时间
                elif pygame.time.get_ticks() - switch_time >= 250:
                    # 如果当前题目已经回答正确且延迟时间超过250ms，显示下一个题目
                    new_question_index = random.randint(0, len(current_question_set) - 1)
                    if new_question_index != last_question_index:
                        question_index = new_question_index
                    else:
                        while new_question_index == last_question_index:
                            new_question_index = random.randint(0, len(current_question_set) - 1)
                        question_index = new_question_index
                    current_question = current_question_set[question_index]["directions"]
                    current_input = []
                    alpha = [128] * len(current_question)  # 重置透明度列表为50%
                    switch_time = 0  # 重置切换时间
                    last_question_index = question_index
        else:
            # 输入错误，箭头变暗
            alpha[len(current_input):] = [128] * (len(current_question) - len(current_input))
            switch_time = 0  # 重置切换时间

        # 显示当前题目的图片、箭头和文字
        if current_question:
            image_path = current_question_set[question_index]["image_path"]
            question_image = pygame.image.load(image_path)
            WIN.blit(question_image, (IMAGE_START_X, IMAGE_START_Y))
            # 绘制文字描述，放置在图片右侧居中显示
            display_message(current_question_set[question_index]["text"], font, TEXT_START_X, TEXT_START_Y)
            for i, direction in enumerate(current_question):
                draw_arrow(direction, ARROW_START_X + 50 * i, ARROW_START_Y, alpha[i])

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()