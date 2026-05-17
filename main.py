import pygame
import random
import os
import math
import struct
import webbrowser

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GROUND_Y = 476
PLATFORM_Y = 500
GRAVITY = 0.6
JUMP_VELOCITY = -15
FPS = 60

# Sprite sheet coordinates
GROUND_X, GROUND_Y_SPRITE = 0, 104
GROUND_W, GROUND_H = 2404, 18

CACTUS_X, CACTUS_Y_SPRITE = 446, 2
CACTUS_W, CACTUS_H = 34, 70

DINO_FRAMES = [(1514, 0, 88, 94), (1602, 0, 88, 94)]
DINO_ORIG_W, DINO_ORIG_H = 88, 94

# Game over score animation
ANIM_DURATION = 60
INITIAL_FONT_SIZE = 300
TARGET_FONT_SIZE = 150
BOUNCE_AMPLITUDE = 8
BOUNCE_SPEED = 0.1
COIN_ANIM_DURATION = 60

# Day / night colours
DAY_BG = (255, 255, 255)
NIGHT_BG = (60, 60, 60)
SCORE_CYCLE = 800

# Current version
VERSION = [1, 3]

# Coin rate: 1 coin per 20 points
COIN_RATE = 20

# Shop items
SHOP_ITEMS = {
    "consumables": {
        "shield": {
            "name": {"EN": "Shield", "DE": "Schild", "RU": "Щит"},
            "cost": 200,
            "desc": {"EN": "Absorb one hit", "DE": "Blockt einen Treffer", "RU": "Блокирует удар"},
            "key": "Z"
        },
        "score_mult": {
            "name": {"EN": "Score Multiplier", "DE": "Punkteverdoppler", "RU": "Удвоитель очков"},
            "cost": 150,
            "desc": {"EN": "2x points for 20s", "DE": "2x Punkte fur 20s", "RU": "2x очков на 20с"},
            "key": "X"
        },
        "head_start": {
            "name": {"EN": "Head Start", "DE": "Vorsprung", "RU": "Фора"},
            "cost": 100,
            "desc": {"EN": "+500 pts if <100", "DE": "+500 Pkt wenn <100", "RU": "+500 очков если <100"},
            "key": "C"
        },
        "mini_dinos": {
            "name": {"EN": "Mini-Dinos", "DE": "Mini-Dinos", "RU": "Мини-динозавры"},
            "cost": 80,
            "desc": {"EN": "0.8x dino scale 20s", "DE": "0.8x Dino-Größe 20s", "RU": "0.8x размер динозавров 20с"},
            "key": "V"
        },
    },
    "skins": {},
    "upgrades": {
        "coin_bonus": {
            "name": {"EN": "Coin Bonus 1.2x", "DE": "Munzbonus 1.2x", "RU": "Бонус монет 1.2x"},
            "cost": 777,
            "desc": {"EN": "20% more coins forever", "DE": "20% mehr Munzen fur immer", "RU": "20% больше монет навсегда"},
            "key": None
        },
    },
    "special": {
        "immortal": {
            "name": {"EN": "Immortal Mode", "DE": "Unsterblich", "RU": "Бессмертный режим"},
            "cost": 500,
            "desc": {"EN": "Practice, no score", "DE": "Uben, keine Punkte", "RU": "Тренировка, без очков"},
            "key": None
        },
    }
}
# Language dictionaries
LANGUAGES = {
    "EN": {
        "play": "PLAY", "shop": "SHOP", "skins": "SKINS",
        "settings": "SETTINGS", "info": "INFO", "stats": "STATS", "exit": "EXIT",
        "menu": "MENU", "pause": "PAUSE", "resume": "Press ESC to Resume",
        "restart": "Press SPACE to Restart", "start": "Press SPACE to Start",
        "high_score": "HIGH SCORE", "score_label": "SCORE",
        "total_score": "Total Score", "total_time": "Total Time",
        "total_jumps": "Total Jumps", "dark_mode": "Dark mode",
        "time_switches": "Toggle time switches", "language": "EN", "beta": "",
        "shop_title": "SHOP", "consumables": "Consumables", "skins_cat": "Skins",
        "upgrades": "Upgrades", "special": "Special",
        "owned": "Owned", "buy": "Buy", "equip": "Equip", "equipped": "Equipped",
        "immortal_btn": "I", "back": "Press ESC to return",
    },
    "DE": {
        "play": "SPIELEN", "shop": "SHOP", "skins": "SKINS",
        "settings": "OPTIONEN", "info": "INFO", "stats": "STATISTIK", "exit": "BEENDEN",
        "menu": "MENU", "pause": "PAUSE", "resume": "ESC zum Fortsetzen",
        "restart": "LEERTASTE Neustart", "start": "LEERTASTE zum Start",
        "high_score": "HIGH SCORE", "score_label": "PUNKTE",
        "total_score": "Gesamtpunkte", "total_time": "Gesamtzeit",
        "total_jumps": "Spruenge", "dark_mode": "Dunkelmodus",
        "time_switches": "Tag/Nacht wechseln", "language": "DE", "beta": "",
        "shop_title": "SHOP", "consumables": "Verbrauchbar", "skins_cat": "Skins",
        "upgrades": "Upgrades", "special": "Spezial",
        "owned": "Besitzt", "buy": "Kaufen", "equip": "Anlegen", "equipped": "Angelegt",
        "immortal_btn": "I", "back": "ESC zum Zurueck",
    },
    "RU": {
        "play": "ИГРАТЬ", "shop": "МАГАЗИН", "skins": "СКИНЫ",
        "settings": "НАСТРОЙКИ", "info": "ИНФО", "stats": "СТАТИСТИКА", "exit": "ВЫХОД",
        "menu": "МЕНЮ", "pause": "ПАУЗА", "resume": "ESC - Продолжить",
        "restart": "ПРОБЕЛ - Заново", "start": "ПРОБЕЛ - Начать",
        "high_score": "РЕКОРД", "score_label": "СЧЁТ",
        "total_score": "Всего очков", "total_time": "Время игры",
        "total_jumps": "Прыжков", "dark_mode": "Тёмный режим",
        "time_switches": "Смена дня и ночи", "language": "RU", "beta": "",
        "shop_title": "МАГАЗИН", "consumables": "Расходники", "skins_cat": "Скины",
        "upgrades": "Улучшения", "special": "Особое",
        "owned": "Куплено", "buy": "Купить", "equip": "Надеть", "equipped": "Надето",
        "immortal_btn": "Б", "back": "ESC - Назад",
    }
}


# Game classes
class Cactus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_velocity = 0
        self.on_ground = True
        self.width = CACTUS_W
        self.height = CACTUS_H
        self.hitbox = pygame.Rect(x, y, self.width, self.height)
        self.image = None

    def jump(self):
        if self.on_ground:
            self.y_velocity = JUMP_VELOCITY
            self.on_ground = False
            return True
        return False

    def update(self):
        self.y_velocity += GRAVITY
        self.y += self.y_velocity
        if self.y + self.height > PLATFORM_Y:
            self.y = PLATFORM_Y - self.height
            self.y_velocity = 0
            self.on_ground = True
        else:
            self.on_ground = False
        self.hitbox.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Dino:
    def __init__(self, x, scale, frames, dino_scale_mult=1.0):
        self.base_scale = scale
        self.scale_mult = dino_scale_mult
        self.scale = scale * dino_scale_mult
        self.width = int(DINO_ORIG_W * self.scale)
        self.height = int(DINO_ORIG_H * self.scale)
        self.x = x
        self.y = PLATFORM_Y - self.height
        hitbox_w = int(self.width * 0.9)
        hitbox_h = int(self.height * 0.9)
        hitbox_y = self.y + (self.height - hitbox_h)
        hitbox_x = self.x + (self.width - hitbox_w) // 2
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_w, hitbox_h)
        self.frame_index = 0
        self.frame_timer = 0
        self.images = []
        for frame in frames:
            scaled = pygame.transform.scale(frame, (self.width, self.height))
            mirrored = pygame.transform.flip(scaled, True, False)
            self.images.append(mirrored)

    def update(self, speed):
        self.x -= speed
        self.hitbox.x = self.x + (self.width - self.hitbox.width) // 2
        self.frame_timer += 1
        if self.frame_timer > 5:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

    def draw(self, screen):
        screen.blit(self.images[self.frame_index], (self.x, self.y))

    def is_off_screen(self):
        return self.x + self.width < 0


class Ground:
    def __init__(self, image):
        self.image = image
        self.x = 0
        self.width = image.get_width()

    def update(self, speed):
        self.x -= speed
        if self.x <= -self.width:
            self.x += self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, GROUND_Y))
        if self.x < 0:
            screen.blit(self.image, (self.x + self.width, GROUND_Y))


# Data handling
def pack_settings(dark_mode, time_switches_on, lang):
    lang_map = {"EN": 0, "DE": 1, "RU": 2}
    val = lang_map.get(lang, 0)
    if dark_mode:
        val |= 0b0100
    if time_switches_on:
        val |= 0b1000
    return val

def unpack_settings(byte):
    lang_map = {0: "EN", 1: "DE", 2: "RU"}
    lang = lang_map.get(byte & 0b0011, "EN")
    dark_mode = bool(byte & 0b0100)
    time_switches_on = bool(byte & 0b1000)
    return dark_mode, time_switches_on, lang

def pack_shop_items(owned_items):
    val = 0
    bit = 0
    for cat in ["consumables", "upgrades", "special"]:
        for item_id in SHOP_ITEMS[cat]:
            if item_id in owned_items:
                val |= (1 << bit)
            bit += 1
    return val

def unpack_shop_items(val):
    owned = set()
    bit = 0
    for cat in ["consumables", "upgrades", "special"]:
        for item_id in SHOP_ITEMS[cat]:
            if val & (1 << bit):
                owned.add(item_id)
            bit += 1
    return owned

def load_progress():
    if not os.path.exists("data.bin"):
        return 0, 0, 0, 0, 0, set(), [0, 0], False, True, "EN"
    try:
        with open("data.bin", "rb") as f:
            data = f.read()
        dark_mode = False
        time_switches_on = True
        lang = "EN"
        coins = 0
        owned_items = set()
        ver = [0, 0]
        if len(data) >= 18:
            ver = list(struct.unpack('<BB', data[:2]))
        if len(data) >= 18:
            high, total_score, total_time, total_jumps = struct.unpack('<IIII', data[2:18])
        if len(data) >= 22:
            coins = struct.unpack('<I', data[18:22])[0]
        if len(data) >= 26:
            shop_val = struct.unpack('<I', data[22:26])[0]
            owned_items = unpack_shop_items(shop_val)
        if len(data) >= 27:
            settings_byte = data[26]
            dark_mode, time_switches_on, lang = unpack_settings(settings_byte)
        return high, total_score, total_time, total_jumps, coins, owned_items, ver, dark_mode, time_switches_on, lang
    except:
        return 0, 0, 0, 0, 0, set(), [0, 0], False, True, "EN"

def save_progress(high, total_score, total_seconds, jumps, coins, owned_items, version, dark_mode, time_switches_on, lang):
    try:
        with open("data.bin", "wb") as f:
            f.write(struct.pack('<BB', version[0], version[1]))
            f.write(struct.pack('<IIII', high, total_score, total_seconds, jumps))
            f.write(struct.pack('<I', coins))
            shop_val = pack_shop_items(owned_items)
            f.write(struct.pack('<I', shop_val))
            settings_byte = pack_settings(dark_mode, time_switches_on, lang)
            f.write(bytes([settings_byte]))
    except:
        pass


# Helpers
def load_sprites(sheet):
    ground_img = sheet.subsurface(pygame.Rect(GROUND_X, GROUND_Y_SPRITE, GROUND_W, GROUND_H)).convert_alpha()
    cactus_img = sheet.subsurface(pygame.Rect(CACTUS_X, CACTUS_Y_SPRITE, CACTUS_W, CACTUS_H)).convert_alpha()
    dino_frames = []
    for rect in DINO_FRAMES:
        frame = sheet.subsurface(pygame.Rect(rect)).convert_alpha()
        dino_frames.append(frame)
    return ground_img, cactus_img, dino_frames

def blend_colours(a, b, amount):
    return tuple(int(a[i] + (b[i] - a[i]) * amount) for i in range(3))

def draw_big_score(screen, font, number, size, centre):
    text = font.render(f"{number:07d}", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=centre))


# Main game
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CactusJump")
    clock = pygame.time.Clock()

    sprite_path = os.path.join("assets", "sprite.png")
    if not os.path.exists(sprite_path):
        pygame.quit()
        return
    sheet = pygame.image.load(sprite_path).convert_alpha()

    cactus_icon = sheet.subsurface(pygame.Rect(CACTUS_X, CACTUS_Y_SPRITE, CACTUS_W, CACTUS_H))
    pygame.display.set_icon(cactus_icon)

    ground_img, cactus_img, dino_frames = load_sprites(sheet)

    # Load the main font
    font_path = os.path.join("assets", "font.ttf")
    if os.path.exists(font_path):
        main_font_small = pygame.font.Font(font_path, 30)
        main_font_big = pygame.font.Font(font_path, 60)
    else:
        main_font_small = pygame.font.Font(None, 30)
        main_font_big = pygame.font.Font(None, 60)

    # Load the Russian font
    ru_font_path = os.path.join("assets", "ru.ttf")
    ru_font_small = None
    ru_font_big = None
    ru_font_tiny = None
    if os.path.exists(ru_font_path):
        ru_font_small = pygame.font.Font(ru_font_path, 30)
        ru_font_big = pygame.font.Font(ru_font_path, 60)
        ru_font_tiny = pygame.font.Font(ru_font_path, 16)

    version_font = pygame.font.Font(font_path, 20) if os.path.exists(font_path) else pygame.font.Font(None, 20)
    tiny_font = pygame.font.Font(font_path, 16) if os.path.exists(font_path) else pygame.font.Font(None, 16)

    # Load persistent data
    high_score, total_score, saved_seconds, total_jumps, coins, owned_items, saved_ver, dark_mode, time_switches_on, lang = load_progress()
    total_frames = saved_seconds * FPS

    def get_font_small():
        if lang == "RU" and ru_font_small:
            return ru_font_small
        return main_font_small

    def get_font_big():
        if lang == "RU" and ru_font_big:
            return ru_font_big
        return main_font_big

    def get_font_tiny():
        if lang == "RU" and ru_font_tiny:
            return ru_font_tiny
        return tiny_font

    # Version bounce animation
    version_bounce_timer = 0
    version_bounce_active = False
    if saved_ver != VERSION:
        version_bounce_active = True
        version_bounce_timer = 5 * FPS

    # The player and world
    player = Cactus(100, PLATFORM_Y - CACTUS_H)
    player.image = cactus_img
    ground = Ground(ground_img)
    dinos = []
    speed = 0.0
    score = 0
    score_timer = 0
    state = "menu"
    paused = False

    anim_frame = 0
    final_score = 0
    new_high_score = False

    # Coin animation state
    coin_earned = 0
    old_coins = 0
    coin_anim_frame = 0

    # Active consumables
    active_shield = False
    active_score_mult = False
    active_mini_dinos = False
    immortal_active = False
    score_mult_timer = 0
    mini_dinos_timer = 0
    dino_scale_mult = 1.0

    # Shop state
    shop_category = "consumables"

    # Decorative dinos on the menu
    menu_dinos = []
    big_dino = Dino(600, 0.9, dino_frames)
    menu_dinos.append(big_dino)
    small_dino1 = Dino(750, 0.6, dino_frames)
    small_dino2 = Dino(850, 0.6, dino_frames)
    menu_dinos.append(small_dino1)
    menu_dinos.append(small_dino2)
    menu_ground_x = 0

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))

    # Main menu buttons
    btn_w, btn_h = 200, 50
    play_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, 180, btn_w, btn_h)
    immortal_btn = pygame.Rect(play_btn.right + 10, play_btn.y, 40, btn_h)
    shop_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, 250, btn_w, btn_h)
    skins_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, 320, btn_w, btn_h)

    base_w, base_h = 140, 40
    scale_factor = 1.45
    bottom_w = int(base_w * scale_factor)
    bottom_h = int(base_h * scale_factor)
    settings_btn = pygame.Rect(30, SCREEN_HEIGHT - 120, bottom_w, bottom_h)
    info_btn = pygame.Rect(30 + bottom_w + 20, SCREEN_HEIGHT - 120, bottom_w, bottom_h)
    stats_btn = pygame.Rect(30 + 2*(bottom_w + 20), SCREEN_HEIGHT - 120, bottom_w, bottom_h)
    exit_btn = pygame.Rect(30 + 3*(bottom_w + 20), SCREEN_HEIGHT - 120, bottom_w, bottom_h)
    lang_btn = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 70, 60, 40)

    # Shop category buttons on the left
    shop_categories = ["consumables", "skins", "upgrades", "special"]
    cat_buttons = {}
    cat_btn_h = 40
    cat_start_y = 200
    for i, cat in enumerate(shop_categories):
        cat_buttons[cat] = pygame.Rect(80, cat_start_y + i * (cat_btn_h + 10), 250, cat_btn_h)

    buy_buttons = {}
    item_start_y = 200
    item_x = 350

    # Settings panel
    settings_panel = pygame.Rect(SCREEN_WIDTH//2 - 250, 100, 500, 300)
    dark_mode_check = pygame.Rect(settings_panel.x + 40, settings_panel.y + 100, 30, 30)
    time_check = pygame.Rect(settings_panel.x + 40, settings_panel.y + 160, 30, 30)
    settings_visible = False
    stats_panel = pygame.Rect(SCREEN_WIDTH//2 - 250, 100, 500, 300)
    stats_visible = False
    info_panel = pygame.Rect(SCREEN_WIDTH//2 - 200, 150, 400, 200)
    info_visible = False
    github_btn = pygame.Rect(info_panel.centerx - 80, info_panel.bottom - 50, 160, 35)

    close_w = 20
    close_h = 20
    close_settings_btn = pygame.Rect(settings_panel.right - 40, settings_panel.y + 10, close_w, close_h)
    close_stats_btn = pygame.Rect(stats_panel.right - 40, stats_panel.y + 10, close_w, close_h)
    close_info_btn = pygame.Rect(info_panel.right - 40, info_panel.y + 10, close_w, close_h)

    # Pause and game over buttons
    menu_btn = pygame.Rect(0, 0, 200, 50)
    menu_btn_gameover = pygame.Rect(0, 0, 140, 35)

    running = True
    while running:
        lang_dict = LANGUAGES[lang]

        # Blend the background colour based on day/night cycle
        active_score = score if state != "menu" else 0
        pos_in_cycle = active_score % SCORE_CYCLE
        blend = pos_in_cycle / SCORE_CYCLE
        smooth = (math.sin((blend - 0.5) * math.pi) + 1) / 2

        if dark_mode:
            day_col = NIGHT_BG
            night_col = DAY_BG
        else:
            day_col = DAY_BG
            night_col = NIGHT_BG

        if not time_switches_on:
            bg_colour = day_col
        else:
            bg_colour = blend_colours(day_col, night_col, smooth)

        text_colour = (255, 255, 255) if smooth > 0.5 else (0, 0, 0)
        title_colour = (255, 255, 255) if dark_mode else (0, 0, 0)
        score_colour = (255, 255, 255) if dark_mode else text_colour
        ver_colour = (255, 255, 255) if dark_mode else text_colour
        coin_colour = (0, 0, 0) if not dark_mode else (255, 215, 0)
        inv_colour = (255, 255, 255) if dark_mode else text_colour

        # Handle all inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                total_sec = total_frames // FPS
                save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "playing":
                        paused = not paused
                    elif state == "over":
                        # Return to menu
                        total_sec = total_frames // FPS
                        save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                        state = "menu"
                        dinos.clear()
                        speed = 0.0
                        score = 0
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        anim_frame = 0
                        active_shield = False
                        active_score_mult = False
                        active_mini_dinos = False
                        immortal_active = False
                        dino_scale_mult = 1.0
                    elif state == "shop":
                        state = "menu"
                    elif state == "menu":
                        settings_visible = False
                        stats_visible = False
                        info_visible = False

                # Jump with W, Space, Up
                if event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                    if state == "menu":
                        speed = 7.0
                        score = 0
                        dinos.clear()
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        state = "playing"
                        immortal_active = False
                        if player.jump():
                            total_jumps += 1
                    elif state == "playing" and not paused:
                        if player.jump():
                            total_jumps += 1
                    elif state == "over":
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        dinos.clear()
                        score = 0
                        speed = 0.0
                        state = "playing"
                        ground.x = 0
                        anim_frame = 0
                        active_shield = False
                        active_score_mult = False
                        active_mini_dinos = False
                        immortal_active = False
                        dino_scale_mult = 1.0
                        if player.jump():
                            total_jumps += 1

                # Consumable hotkeys during gameplay
                if state == "playing" and not paused:
                    key_map = {"Z": "shield", "X": "score_mult", "C": "head_start", "V": "mini_dinos"}
                    if event.key in (pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v):
                        key_name = pygame.key.name(event.key).upper()
                        if key_name in key_map:
                            item_id = key_map[key_name]
                            if item_id in owned_items:
                                if item_id == "shield":
                                    active_shield = True
                                    owned_items.discard(item_id)
                                elif item_id == "score_mult":
                                    active_score_mult = True
                                    score_mult_timer = 20 * FPS
                                    owned_items.discard(item_id)
                                elif item_id == "head_start":
                                    if score < 100:
                                        score += 500
                                        total_score += 500
                                        owned_items.discard(item_id)
                                elif item_id == "mini_dinos":
                                    active_mini_dinos = True
                                    mini_dinos_timer = 20 * FPS
                                    dino_scale_mult = 0.8
                                    owned_items.discard(item_id)
                                total_sec = total_frames // FPS
                                save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = event.pos
                if state == "menu":
                    if play_btn.collidepoint(mouse):
                        speed = 7.0
                        score = 0
                        dinos.clear()
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        state = "playing"
                        active_shield = False
                        active_score_mult = False
                        active_mini_dinos = False
                        immortal_active = False
                        dino_scale_mult = 1.0
                        if player.jump():
                            total_jumps += 1
                    elif "immortal" in owned_items and immortal_btn.collidepoint(mouse):
                        speed = 7.0
                        score = 0
                        dinos.clear()
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        state = "playing"
                        immortal_active = True
                        if player.jump():
                            total_jumps += 1
                    elif shop_btn.collidepoint(mouse):
                        state = "shop"
                        shop_category = "consumables"
                    elif settings_btn.collidepoint(mouse):
                        if settings_visible:
                            settings_visible = False
                        else:
                            settings_visible = True
                            stats_visible = False
                            info_visible = False
                    elif stats_btn.collidepoint(mouse):
                        if stats_visible:
                            stats_visible = False
                        else:
                            stats_visible = True
                            settings_visible = False
                            info_visible = False
                    elif info_btn.collidepoint(mouse):
                        if info_visible:
                            info_visible = False
                        else:
                            info_visible = True
                            settings_visible = False
                            stats_visible = False
                    elif exit_btn.collidepoint(mouse):
                        total_sec = total_frames // FPS
                        save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                        running = False
                    elif lang_btn.collidepoint(mouse):
                        if lang == "EN":
                            lang = "DE"
                        elif lang == "DE":
                            lang = "RU"
                        else:
                            lang = "EN"
                        total_sec = total_frames // FPS
                        save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                    # Close buttons on panels
                    if settings_visible and close_settings_btn.collidepoint(mouse):
                        settings_visible = False
                    if stats_visible and close_stats_btn.collidepoint(mouse):
                        stats_visible = False
                    if info_visible and close_info_btn.collidepoint(mouse):
                        info_visible = False
                    if info_visible and github_btn.collidepoint(mouse):
                        webbrowser.open("https://github.com/fomybe/cactusjump/tree/main")
                    # Toggle checkboxes in settings
                    if settings_visible:
                        if dark_mode_check.collidepoint(mouse):
                            dark_mode = not dark_mode
                            total_sec = total_frames // FPS
                            save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                        if time_check.collidepoint(mouse):
                            time_switches_on = not time_switches_on
                            total_sec = total_frames // FPS
                            save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)

                elif state == "shop":
                    for cat, btn in cat_buttons.items():
                        if btn.collidepoint(mouse):
                            shop_category = cat
                    if shop_category in buy_buttons:
                        for item_id, btn_info in buy_buttons[shop_category].items():
                            if btn_info["btn"].collidepoint(mouse):
                                item = SHOP_ITEMS[shop_category][item_id]
                                if coins >= item["cost"]:
                                    coins -= item["cost"]
                                    owned_items.add(item_id)
                                    total_sec = total_frames // FPS
                                    save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)

                elif state == "playing" and paused:
                    if menu_btn.collidepoint(mouse):
                        total_sec = total_frames // FPS
                        save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                        state = "menu"
                        paused = False
                        dinos.clear()
                        speed = 0.0
                        score = 0
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        active_shield = False
                        active_score_mult = False
                        active_mini_dinos = False
                        immortal_active = False
                        dino_scale_mult = 1.0

                elif state == "over":
                    if menu_btn_gameover.collidepoint(mouse):
                        total_sec = total_frames // FPS
                        save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                        state = "menu"
                        dinos.clear()
                        speed = 0.0
                        score = 0
                        player.y = PLATFORM_Y - CACTUS_H
                        player.y_velocity = 0
                        player.on_ground = True
                        ground.x = 0
                        anim_frame = 0
                        active_shield = False
                        active_score_mult = False
                        active_mini_dinos = False
                        immortal_active = False
                        dino_scale_mult = 1.0

        # Update the real gameplay
        if state == "playing" and not paused:
            player.update()
            ground.update(speed)
            total_frames += 1

            if active_score_mult:
                score_mult_timer -= 1
                if score_mult_timer <= 0:
                    active_score_mult = False
            if active_mini_dinos:
                mini_dinos_timer -= 1
                if mini_dinos_timer <= 0:
                    active_mini_dinos = False
                    dino_scale_mult = 1.0

            speed = min(17.0, 7.0 + score * 0.01)

            score_timer += 1
            if score_timer > 6:
                score_add = 2 if active_score_mult else 1
                score += score_add
                if not immortal_active:
                    total_score += score_add
                score_timer = 0

            spawn_gap = 500 + int(speed * 30)

            if len(dinos) == 0 or dinos[-1].x < SCREEN_WIDTH - spawn_gap:
                scale = random.uniform(0.6, 1.0)
                dinos.append(Dino(SCREEN_WIDTH + 50, scale, dino_frames, dino_scale_mult))
                # Pairs can appear with any dino size
                if random.random() < 0.4:
                    dinos.append(Dino(SCREEN_WIDTH + 150, scale, dino_frames, dino_scale_mult))
                    # Triples when score is above 500
                    if score > 500 and random.random() < 0.3:
                        dinos.append(Dino(SCREEN_WIDTH + 250, scale, dino_frames, dino_scale_mult))
                        # Quad when score is above 1200
                        if score > 1200 and random.random() < 0.3:
                            dinos.append(Dino(SCREEN_WIDTH + 350, scale, dino_frames, dino_scale_mult))

            for dino in dinos[:]:
                dino.update(speed)
                if dino.is_off_screen():
                    dinos.remove(dino)

            for dino in dinos:
                if player.hitbox.colliderect(dino.hitbox):
                    if active_shield or immortal_active:
                        if dinos:
                            dinos.remove(dino)
                        if active_shield:
                            active_shield = False
                        break
                    state = "over"
                    final_score = score
                    new_high_score = score > high_score
                    if new_high_score:
                        high_score = score
                    coin_bonus = 1.2 if "coin_bonus" in owned_items else 1.0
                    coin_earned = int((final_score / COIN_RATE) * coin_bonus)
                    old_coins = coins
                    coins += coin_earned
                    total_sec = total_frames // FPS
                    save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)
                    anim_frame = 0
                    active_shield = False
                    active_score_mult = False
                    active_mini_dinos = False
                    immortal_active = False
                    dino_scale_mult = 1.0
                    break

        if state == "over":
            anim_frame += 1

        # Version bounce
        if version_bounce_active:
            version_bounce_timer -= 1
            if version_bounce_timer <= 0:
                version_bounce_active = False
                saved_ver = VERSION[:]
                total_sec = total_frames // FPS
                save_progress(high_score, total_score, total_sec, total_jumps, coins, owned_items, VERSION, dark_mode, time_switches_on, lang)

        # Draw everything
        screen.fill(bg_colour)

        if state in ("menu", "shop"):
            screen.blit(ground_img, (menu_ground_x, GROUND_Y))
            player.image = cactus_img
            player.draw(screen)
            for dino in menu_dinos:
                dino.frame_timer += 1
                if dino.frame_timer > 5:
                    dino.frame_timer = 0
                    dino.frame_index = (dino.frame_index + 1) % 2
                dino.draw(screen)

        if state not in ("menu", "shop"):
            ground.draw(screen)
            player.draw(screen)
            for dino in dinos:
                dino.draw(screen)

        # Live score in the top right
        if state == "playing":
            surf = main_font_small.render(f"{score:07d}", True, score_colour)
            screen.blit(surf, surf.get_rect(topright=(SCREEN_WIDTH - 20, 20)))

            # Show active and available consumables top left
            consumable_texts = []
            if active_shield:
                consumable_texts.append("Shield [ACTIVE]")
            if active_score_mult:
                s = max(0, score_mult_timer // FPS)
                consumable_texts.append(f"2x Score [{s}s]")
            if active_mini_dinos:
                s = max(0, mini_dinos_timer // FPS)
                consumable_texts.append(f"Mini-Dinos [{s}s]")
            if immortal_active:
                consumable_texts.append("Immortal [ACTIVE]")
            key_map = {"shield": "Z", "score_mult": "X", "head_start": "C", "mini_dinos": "V"}
            for item_id, item in SHOP_ITEMS["consumables"].items():
                if item_id in owned_items:
                    condition = ""
                    if item_id == "head_start":
                        if score < 100:
                            condition = " (<100)"
                        else:
                            condition = " (need <100)"
                    item_name = item["name"][lang]
                    consumable_texts.append(f"{item_name}{condition} [{key_map[item_id]}]")
            y_off = 20
            for txt in consumable_texts:
                cons_surf = get_font_small().render(txt, True, inv_colour)
                screen.blit(cons_surf, (20, y_off))
                y_off += 25

        # Coin counter on the menu
        if state == "menu":
            coin_text = f"${coins}"
            coin_surf = main_font_small.render(coin_text, True, coin_colour)
            screen.blit(coin_surf, coin_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20)))

        # Main menu overlay
        if state == "menu":
            menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            menu_overlay.fill((0, 0, 0, 120))
            screen.blit(menu_overlay, (0, 0))

            title_surf = main_font_big.render("CactusJump", True, title_colour)
            screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, 80)))

            def draw_button(rect, text, active=True):
                colour = (255, 255, 255) if active else (150, 150, 150)
                pygame.draw.rect(screen, colour, rect, 2)
                font = get_font_small()
                txt = font.render(text, True, colour)
                screen.blit(txt, txt.get_rect(center=rect.center))

            draw_button(play_btn, lang_dict["play"], True)
            if "immortal" in owned_items:
                pygame.draw.rect(screen, (255, 255, 255), immortal_btn, 2)
                imm_txt = get_font_small().render(lang_dict["immortal_btn"], True, (255, 255, 255))
                screen.blit(imm_txt, imm_txt.get_rect(center=immortal_btn.center))
            draw_button(shop_btn, lang_dict["shop"], True)
            draw_button(skins_btn, lang_dict["skins"], False)

            draw_button(settings_btn, lang_dict["settings"], True)
            draw_button(info_btn, lang_dict["info"], True)
            draw_button(stats_btn, lang_dict["stats"], True)
            draw_button(exit_btn, lang_dict["exit"], True)

            pygame.draw.rect(screen, (255, 255, 255), lang_btn, 2)
            lang_txt = get_font_small().render(lang, True, (255, 255, 255))
            screen.blit(lang_txt, lang_txt.get_rect(center=lang_btn.center))

        # Shop screen
        elif state == "shop":
            shop_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            shop_overlay.fill((0, 0, 0, 180))
            screen.blit(shop_overlay, (0, 0))

            shop_title = get_font_big().render(lang_dict["shop_title"], True, (255, 255, 255))
            screen.blit(shop_title, (100, 80))

            coin_surf = main_font_small.render(f"${coins}", True, coin_colour)
            screen.blit(coin_surf, (SCREEN_WIDTH - 150, 80))

            for cat, btn in cat_buttons.items():
                colour = (255, 255, 0) if cat == shop_category else (255, 255, 255)
                pygame.draw.rect(screen, colour, btn, 2)
                if cat == "skins":
                    cat_name = lang_dict["skins_cat"]
                else:
                    cat_name = lang_dict.get(cat, cat.capitalize())
                cat_surf = get_font_small().render(cat_name, True, colour)
                screen.blit(cat_surf, cat_surf.get_rect(center=btn.center))

            if shop_category in SHOP_ITEMS and SHOP_ITEMS[shop_category]:
                buy_buttons[shop_category] = {}
                y = item_start_y
                for item_id, item in SHOP_ITEMS[shop_category].items():
                    owned = item_id in owned_items
                    name_colour = (0, 255, 0) if owned else (255, 255, 255)
                    name_surf = get_font_small().render(item["name"][lang], True, name_colour)
                    screen.blit(name_surf, (item_x, y))
                    desc_surf = get_font_tiny().render(item["desc"][lang], True, (200, 200, 200))
                    screen.blit(desc_surf, (item_x, y + 25))
                    if owned:
                        count_text = lang_dict["owned"]
                    else:
                        count_text = f"${item['cost']}"
                    count_surf = get_font_small().render(count_text, True, (255, 255, 255))
                    screen.blit(count_surf, (item_x + 400, y))
                    if not owned:
                        btn = pygame.Rect(item_x + 500, y + 5, 100, 30)
                        buy_buttons[shop_category][item_id] = {"btn": btn}
                        btn_colour = (0, 255, 0) if coins >= item["cost"] else (150, 150, 150)
                        pygame.draw.rect(screen, btn_colour, btn, 2)
                        buy_surf = get_font_small().render(lang_dict["buy"], True, btn_colour)
                        screen.blit(buy_surf, buy_surf.get_rect(center=btn.center))
                    y += 60
            else:
                if shop_category == "skins":
                    if lang == "EN":
                        coming_soon = "Coming soon..."
                    elif lang == "DE":
                        coming_soon = "Kommt bald..."
                    elif lang == "RU":
                        coming_soon = "Скоро..."
                    else:
                        coming_soon = "Coming soon..."
                    gray_text = get_font_small().render(coming_soon, True, (150, 150, 150))
                    screen.blit(gray_text, (item_x, item_start_y))

            back_surf = get_font_small().render(lang_dict["back"], True, (200, 200, 200))
            screen.blit(back_surf, (50, SCREEN_HEIGHT - 80))

        # Version number bottom left
        ver_text = f"v{VERSION[0]}.{VERSION[1]}"
        if version_bounce_active:
            bounce_offset = math.sin(version_bounce_timer * 0.2) * 2
            ver_size = 20 + bounce_offset
            ver_font = pygame.font.Font(font_path, int(ver_size)) if os.path.exists(font_path) else pygame.font.Font(None, int(ver_size))
        else:
            ver_font = version_font
        ver_surf = ver_font.render(ver_text, True, ver_colour)
        screen.blit(ver_surf, (10, SCREEN_HEIGHT - 30))

        # Game over screen
        if state == "over":
            screen.blit(overlay, (0, 0))
            label = lang_dict["high_score"] if new_high_score else lang_dict["score_label"]
            label_surf = get_font_big().render(label, True, (255, 255, 255))
            screen.blit(label_surf, label_surf.get_rect(center=(SCREEN_WIDTH//2, 120)))

            centre = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            if anim_frame <= ANIM_DURATION:
                t = anim_frame / ANIM_DURATION
                size = INITIAL_FONT_SIZE + (TARGET_FONT_SIZE - INITIAL_FONT_SIZE) * (t**2)
                shown = int(round(final_score * t))
            else:
                bounce = math.sin((anim_frame - ANIM_DURATION) * BOUNCE_SPEED) * BOUNCE_AMPLITUDE
                size = TARGET_FONT_SIZE + bounce
                shown = final_score
            draw_big_score(screen, pygame.font.Font(font_path, int(size)) if os.path.exists(font_path) else pygame.font.Font(None, int(size)),
                           shown, size, centre)

            coin_anim_frame = anim_frame - ANIM_DURATION
            if coin_anim_frame >= 0 and coin_earned > 0:
                t = min(1.0, coin_anim_frame / COIN_ANIM_DURATION)
                earned_display = int(coin_earned * (1 - t))
                total_display = old_coins + int(coin_earned * t)
                if coin_anim_frame >= COIN_ANIM_DURATION:
                    earned_display = 0
                    total_display = coins
                coin_y = centre[1] + int(size * 0.5) + 30
                total_x = int(centre[0] + 60 * (1 - t))
                total_surf = main_font_small.render(f"${total_display}", True, coin_colour)
                total_rect = total_surf.get_rect(center=(total_x, coin_y))
                screen.blit(total_surf, total_rect)
                if earned_display > 0:
                    plus_surf = main_font_small.render(f"+${earned_display}", True, coin_colour)
                    plus_rect = plus_surf.get_rect(center=(total_x - 120, coin_y))
                    screen.blit(plus_surf, plus_rect)

            restart = get_font_small().render(lang_dict["restart"], True, (200, 200, 200))
            restart_rect = restart.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 40))
            screen.blit(restart, restart_rect)

            menu_btn_gameover.width = 140
            menu_btn_gameover.height = 35
            menu_btn_gameover.x = 30
            menu_btn_gameover.centery = restart_rect.centery
            pygame.draw.rect(screen, (255, 255, 255), menu_btn_gameover, 2)
            menu_txt = get_font_small().render(lang_dict["menu"], True, (255, 255, 255))
            screen.blit(menu_txt, menu_txt.get_rect(center=menu_btn_gameover.center))

        # Pause screen
        elif state == "playing" and paused:
            screen.blit(overlay, (0, 0))
            pause_txt = get_font_big().render(lang_dict["pause"], True, (255, 255, 255))
            screen.blit(pause_txt, pause_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)))

            total_sec = total_frames // FPS
            lines = [
                f"{lang_dict['total_score']}: {total_score:07d}",
                f"High Score: {high_score:07d}",
                f"{lang_dict['total_time']}: {total_sec}s",
                f"{lang_dict['total_jumps']}: {total_jumps}"
            ]
            y = SCREEN_HEIGHT//2 - 20
            for line in lines:
                s = get_font_small().render(line, True, (255, 255, 255))
                screen.blit(s, s.get_rect(center=(SCREEN_WIDTH//2, y)))
                y += 35

            resume = get_font_small().render(lang_dict["resume"], True, (200, 200, 200))
            resume_rect = resume.get_rect(center=(SCREEN_WIDTH//2, y + 20))
            screen.blit(resume, resume_rect)

            coin_surf = main_font_small.render(f"${coins}", True, coin_colour)
            screen.blit(coin_surf, (20, 20))

            menu_btn.centerx = SCREEN_WIDTH // 2
            menu_btn.y = resume_rect.bottom + 20
            pygame.draw.rect(screen, (255, 255, 255), menu_btn, 2)
            menu_txt = get_font_small().render(lang_dict["menu"], True, (255, 255, 255))
            screen.blit(menu_txt, menu_txt.get_rect(center=menu_btn.center))

        # Settings panel
        if settings_visible and state == "menu":
            pygame.draw.rect(screen, (50, 50, 50), settings_panel)
            pygame.draw.rect(screen, (200, 200, 200), settings_panel, 3)

            title_font = get_font_big()
            if lang in ("DE", "RU"):
                title_font = pygame.font.Font(ru_font_path if lang == "RU" else font_path, 40) if os.path.exists(font_path) else get_font_big()
            title_surf = title_font.render(lang_dict["settings"], True, (255, 255, 255))
            screen.blit(title_surf, title_surf.get_rect(center=(settings_panel.centerx, settings_panel.y + 40)))

            pygame.draw.line(screen, (255, 255, 255), close_settings_btn.topleft, close_settings_btn.bottomright, 5)
            pygame.draw.line(screen, (255, 255, 255), close_settings_btn.topright, close_settings_btn.bottomleft, 5)

            dm_text = get_font_small().render(lang_dict["dark_mode"], True, (255, 255, 255))
            screen.blit(dm_text, (settings_panel.x + 90, settings_panel.y + 95))
            pygame.draw.rect(screen, (255, 255, 255), dark_mode_check, 2)
            if dark_mode:
                inner = dark_mode_check.inflate(-6, -6)
                pygame.draw.rect(screen, (255, 255, 255), inner)

            ts_text = get_font_small().render(lang_dict["time_switches"], True, (255, 255, 255))
            screen.blit(ts_text, (settings_panel.x + 90, settings_panel.y + 155))
            pygame.draw.rect(screen, (255, 255, 255), time_check, 2)
            if time_switches_on:
                inner = time_check.inflate(-6, -6)
                pygame.draw.rect(screen, (255, 255, 255), inner)

        # Stats panel
        if stats_visible and state == "menu":
            pygame.draw.rect(screen, (50, 50, 50), stats_panel)
            pygame.draw.rect(screen, (200, 200, 200), stats_panel, 3)

            title_font = get_font_big()
            if lang in ("DE", "RU"):
                title_font = pygame.font.Font(ru_font_path if lang == "RU" else font_path, 40) if os.path.exists(font_path) else get_font_big()
            title_surf = title_font.render(lang_dict["stats"], True, (255, 255, 255))
            screen.blit(title_surf, title_surf.get_rect(center=(stats_panel.centerx, stats_panel.y + 40)))

            pygame.draw.line(screen, (255, 255, 255), close_stats_btn.topleft, close_stats_btn.bottomright, 5)
            pygame.draw.line(screen, (255, 255, 255), close_stats_btn.topright, close_stats_btn.bottomleft, 5)

            total_sec = total_frames // FPS
            lines = [
                f"{lang_dict['total_score']}: {total_score:07d}",
                f"High Score: {high_score:07d}",
                f"{lang_dict['total_time']}: {total_sec}s",
                f"{lang_dict['total_jumps']}: {total_jumps}"
            ]
            y = stats_panel.y + 100
            for line in lines:
                s = get_font_small().render(line, True, (255, 255, 255))
                screen.blit(s, s.get_rect(center=(stats_panel.centerx, y)))
                y += 35

        # Info panel
        if info_visible and state == "menu":
            pygame.draw.rect(screen, (50, 50, 50), info_panel)
            pygame.draw.rect(screen, (200, 200, 200), info_panel, 3)

            pygame.draw.line(screen, (255, 255, 255), close_info_btn.topleft, close_info_btn.bottomright, 5)
            pygame.draw.line(screen, (255, 255, 255), close_info_btn.topright, close_info_btn.bottomleft, 5)

            ver = f"v{VERSION[0]}.{VERSION[1]}"
            text1 = get_font_small().render(f"Version: {ver}", True, (255, 255, 255))
            text2 = get_font_small().render("Made by fomybe", True, (255, 255, 255))
            screen.blit(text1, (info_panel.x + 40, info_panel.y + 50))
            screen.blit(text2, (info_panel.x + 40, info_panel.y + 90))

            pygame.draw.rect(screen, (255, 255, 255), github_btn, 2)
            github_txt = get_font_small().render("GITHUB", True, (255, 255, 255))
            screen.blit(github_txt, github_txt.get_rect(center=github_btn.center))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
