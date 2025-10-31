import pygame
import sys
import time
import random
import os
from pygame.locals import *
import sys

# 处理打包后的路径问题
def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发和打包后"""
    try:
        # PyInstaller创建临时文件夹，并将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 图标路径设置（相对于脚本的位置）
ICON_PATH = resource_path("image.png")

# 严格检查图标文件是否存在
if not os.path.exists(ICON_PATH):
    print(f"错误：图标文件 '{ICON_PATH}' 不存在！")
    print("请将图标文件放在与脚本相同的目录后再运行程序")
    sys.exit(1)

# 尝试加载图标并验证
try:
    icon = pygame.image.load(ICON_PATH)
    # 验证图像是否有效
    if icon.get_width() == 0 or icon.get_height() == 0:
        raise Exception("图标文件无效")
except Exception as e:
    print(f"错误：无法加载图标 - {str(e)}")
    print("请检查图标文件是否损坏或格式正确（推荐PNG格式）")
    sys.exit(1)

pygame.init()
pygame.display.set_caption("HeiKe007")
pygame.display.set_icon(icon)

COLOR_SCHEMES = {
    'green_on_black': {'bg': (0, 0, 0), 'text': (0, 255, 0)},
    'black_on_white': {'bg': (255, 255, 255), 'text': (0, 0, 0)},
    'white_on_black': {'bg': (0, 0, 0), 'text': (255, 255, 255)}
}

FUN_CONTENTS = [
    # 二进制和图案内容
    "0000111101111000011110001111",
    "1111000011110000111100001111",
    "0101010101010101010101010101",
    "1010101010101010101010101010",
    "0011001100111100001111001100",
    "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
    "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
    "█░█░█░█░█░█░█░█░█░█",
    "░█░█░█░█░█░█░█░█░█░",
    "████████████████████",

    # 系统扫描和操作内容
    "Scanning system... [==================>] 100%",
    "Downloading data... 42% complete.",
    "Analyzing network topology...",
    "Mapping IP addresses in subnet...",
    "Port scanning 192.168.1.0/24...",
    "Detecting open ports: 80, 443, 8080, 22",
    "Checking for vulnerabilities...",
    "Exploiting CVE-2023-1234 vulnerability...",
    "Bypassing IDS detection...",
    "Establishing reverse shell...",

    # 数据处理内容
    "0101010110101010011010101101",
    "1100110010101010001100111100",
    "Decrypting AES-256 encrypted data...",
    "Hashing with SHA-256: 5f4dcc3b5aa765d61d8327deb882cf99",
    "Data packet intercepted: 0x7f3a9c0e12d4",
    "Packet analysis complete: TCP flags SYN-ACK",
    "Encrypting communication channel...",
    "Generating RSA key pair...",
    "Key exchange successful: 4096 bits",

    # 系统入侵内容
    "Accessing mainframe... Permission granted",
    "Bypassing firewall... Success",
    "Decrypting data stream... 78%",
    "Establishing secure connection...",
    "IP Address: 192.168.1.104 - Access Logged",
    "Username: admin - Password: ********",
    "System breach detected! Initiating countermeasures",
    "Port 8080 open - Vulnerability exploited",
    "Encryption key: 4B7D2F9A1C3E5G8H",
    "Root access acquired - System control enabled",
    "Disabling security protocols...",
    "Creating backdoor access...",
    "Hiding intrusion痕迹...",
    "Downloading sensitive documents...",
    "Database credentials obtained...",
    "Executing remote command: ls -la /root",

    # 技术术语内容
    "Buffer overflow detected in application",
    "SQL injection successful: ' OR 1=1 --",
    "XSS vulnerability exploited",
    "Brute force attack in progress: 1243 attempts",
    "Dictionary attack successful after 421 tries",
    "Man-in-the-middle attack established",
    "DNS spoofing activated",
    "ARP cache poisoned",
    "MAC address spoofed: 00:1B:44:11:3A:B7",
    "VPN tunnel established to exit node"
]

ASCII_ARTS = [
    "  /\\_/\\  \n ( o.o ) \n  > ^ <",
    "  /\\\n //\\\\\n///\\\\\\\n",
    "   *\n  ***\n *****\n*******\n *****\n  ***\n   *",
]

PARTICLE_COUNT = 200


class Particle:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.char = random.choice(["0", "1"])
        self.speed = random.uniform(20, 100)
        self.size = random.randint(15, 25)
        self.color = (0, 255, 0, random.randint(50, 150))  # 半透明
        self.screen_width = width  # 存储屏幕宽度到实例变量

    def move(self, dt, height):
        self.y += self.speed * dt
        if self.y > height:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, self.screen_width)  # 使用存储的屏幕宽度
            self.char = random.choice(["0", "1"])


class HackerSimulator:
    def __init__(self):
        self.screen = None
        self.width, self.height = 0, 0
        self.font = pygame.font.SysFont('SimHei', 20, bold=True)
        self.clock = pygame.time.Clock()
        self.selected_scheme = None
        self.bg_color = None
        self.text_color = None
        self.lines = []
        self.current_line = ""
        self.char_index = 0
        self.content_index = 0
        self.start_time = None
        self.duration = 180
        self.running = True
        self.particles = []
        self.typing_speed = 0.03  # 字符输入间隔时间（秒）
        self.last_typed_time = 0  # 上次输入字符的时间

    def select_scheme(self):
        self.screen = pygame.display.set_mode((600, 400))
        self.width, self.height = self.screen.get_size()
        options = [("黑底绿字", 'green_on_black'), ("白底黑字", 'black_on_white'), ("黑底白字", 'white_on_black')]

        while self.selected_scheme is None:
            self.screen.fill((50, 50, 50))
            title = self.font.render("选择 Hacker 风格", True, (255, 255, 255))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, (text, key) in enumerate(options):
                rect = pygame.Rect(150, 150 + i * 60, 300, 50)
                pygame.draw.rect(self.screen, (100, 100, 100), rect)
                option_text = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(option_text, (rect.x + rect.width // 2 - option_text.get_width() // 2,
                                               rect.y + rect.height // 2 - option_text.get_height() // 2))
                if rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(self.screen, (150, 150, 150), rect, 3)
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            self.selected_scheme = key

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(60)

        self.bg_color = COLOR_SCHEMES[self.selected_scheme]['bg']
        self.text_color = COLOR_SCHEMES[self.selected_scheme]['text']

    def run_simulation(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        self.start_time = time.time()
        self.particles = [Particle(self.width, self.height) for _ in range(PARTICLE_COUNT)]
        # 横向扫描线计时器和方向
        self.h_scan_timer = random.randint(3, 8)
        self.h_scan_direction = random.choice([1, -1])  # 1=向右, -1=向左
        self.h_scan_pos = 0 if self.h_scan_direction == 1 else self.width

        # 纵向扫描线计时器和方向
        self.v_scan_timer = random.randint(3, 8)
        self.v_scan_direction = random.choice([1, -1])  # 1=向下, -1=向上
        self.v_scan_pos = 0 if self.v_scan_direction == 1 else self.height

        progress_width = self.width // 4
        progress_height = 20

        while self.running:
            dt = self.clock.tick(60) / 1000.0
            current_time = time.time()
            self.screen.fill(self.bg_color)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.quit()

            # ASCII typing - 调整为基于时间间隔的输入方式，确保速度稳定
            if current_time - self.last_typed_time > self.typing_speed:
                if self.char_index < len(FUN_CONTENTS[self.content_index]):
                    self.current_line += FUN_CONTENTS[self.content_index][self.char_index]
                    self.char_index += 1
                    self.last_typed_time = current_time
                else:
                    self.lines.append(self.current_line)
                    self.current_line = ""
                    self.char_index = 0
                    self.content_index = (self.content_index + 1) % len(FUN_CONTENTS)
                    self.last_typed_time = current_time  # 重置计时器

            if len(self.lines) > 30:
                self.lines = self.lines[-30:]

            y = 20
            for line in self.lines:
                text = self.font.render(line, True, self.text_color)
                self.screen.blit(text, (20, y))
                y += text.get_height() + 2

            current_text = self.font.render(self.current_line + "_", True, self.text_color)
            self.screen.blit(current_text, (20, y))

            # 中间进度条
            elapsed = time.time() - self.start_time
            progress = min(elapsed / self.duration, 1.0)
            progress_percent = int(progress * 100)  # 计算百分比
            progress_x = self.width // 2 - progress_width // 2
            progress_y = self.height // 2 - progress_height // 2
            pygame.draw.rect(self.screen, (50, 50, 50), (progress_x, progress_y, progress_width, progress_height))
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (progress_x, progress_y, int(progress_width * progress), progress_height))

            # 进度条百分比显示
            percent_text = self.font.render(f"{progress_percent}%", True, (0, 255, 0))
            self.screen.blit(percent_text, (progress_x + progress_width + 10, progress_y))

            # 光效
            for i in range(3):
                alpha_surf = pygame.Surface((int(progress_width * progress) // 3, progress_height), pygame.SRCALPHA)
                alpha_surf.fill((0, 255, 0, 50))
                self.screen.blit(alpha_surf, (progress_x + i * progress_width // 6, progress_y))

            # 横向拖尾扫描线 (带方向)
            self.h_scan_timer -= dt
            if self.h_scan_timer <= 0:
                # 更新扫描线位置
                self.h_scan_pos += self.h_scan_direction * 5
                # 绘制拖尾效果
                for i in range(30):
                    trail_alpha = 150 - i * 5
                    if trail_alpha <= 0:
                        break
                    trail_pos = self.h_scan_pos - (self.h_scan_direction * i * 3)
                    if 0 <= trail_pos <= self.width:
                        alpha_surf = pygame.Surface((1, self.height), pygame.SRCALPHA)
                        alpha_surf.fill((*self.text_color[:3], trail_alpha))
                        self.screen.blit(alpha_surf, (trail_pos, 0))

                # 检查是否超出屏幕范围，重置扫描线
                if (self.h_scan_direction == 1 and self.h_scan_pos > self.width) or \
                        (self.h_scan_direction == -1 and self.h_scan_pos < 0):
                    self.h_scan_timer = random.randint(3, 8)
                    self.h_scan_direction = random.choice([1, -1])
                    self.h_scan_pos = 0 if self.h_scan_direction == 1 else self.width

            # 纵向拖尾扫描线 (带方向)
            self.v_scan_timer -= dt
            if self.v_scan_timer <= 0:
                # 更新扫描线位置
                self.v_scan_pos += self.v_scan_direction * 5
                # 绘制拖尾效果
                for i in range(30):
                    trail_alpha = 150 - i * 5
                    if trail_alpha <= 0:
                        break
                    trail_pos = self.v_scan_pos - (self.v_scan_direction * i * 3)
                    if 0 <= trail_pos <= self.height:
                        alpha_surf = pygame.Surface((self.width, 1), pygame.SRCALPHA)
                        alpha_surf.fill((*self.text_color[:3], trail_alpha))
                        self.screen.blit(alpha_surf, (0, trail_pos))

                # 检查是否超出屏幕范围，重置扫描线
                if (self.v_scan_direction == 1 and self.v_scan_pos > self.height) or \
                        (self.v_scan_direction == -1 and self.v_scan_pos < 0):
                    self.v_scan_timer = random.randint(3, 8)
                    self.v_scan_direction = random.choice([1, -1])
                    self.v_scan_pos = 0 if self.v_scan_direction == 1 else self.height

            # 粒子更新
            for p in self.particles:
                p.move(dt, self.height)
                text = self.font.render(p.char, True, self.text_color)
                self.screen.blit(text, (p.x, p.y))

            # ASCII动画闪烁
            if random.random() < 0.01:
                art = random.choice(ASCII_ARTS).split('\n')
                for idx, line in enumerate(art):
                    text = self.font.render(line, True, self.text_color)
                    self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 100 + idx * 25))

            pygame.display.flip()
            if elapsed >= self.duration:
                self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    sim = HackerSimulator()
    sim.select_scheme()
    pygame.mouse.set_visible(False)
    sim.run_simulation()
