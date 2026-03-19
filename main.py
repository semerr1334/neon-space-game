import pygame
import sys
import random
import json
import os
import math
from datetime import datetime, timedelta

# ============================================
# КОНФИГУРАЦИЯ
# ============================================
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
FPS = 60

# Пути к ресурсам
SPRITES_DIR = 'images'
SHIPS_DIR = os.path.join(SPRITES_DIR, 'ships')
ITEMS_DIR = os.path.join(SPRITES_DIR, 'items')
ENEMIES_DIR = os.path.join(SPRITES_DIR, 'enemies')
MUSIC_DIR = 'music'
SAVE_FILE = 'save.json'

# Цвета
COLOR_BG = (10, 10, 25)
COLOR_PLAYER = (0, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (180, 180, 180)
COLOR_HP = (50, 255, 50)
COLOR_SHIELD = (100, 100, 255)
COLOR_COIN = (255, 215, 0)
COLOR_CRYSTAL = (0, 255, 200)
COLOR_COIN_SYMBOL = (200, 150, 0)
COLOR_DASH = (255, 255, 255)
COLOR_TUTORIAL = (0, 255, 200)
COLOR_BUTTON = (50, 50, 80)
COLOR_BUTTON_HOVER = (80, 80, 120)
COLOR_ENEMY_BASIC = (255, 50, 50)
COLOR_ENEMY_FAST = (255, 150, 50)
COLOR_ENEMY_TANK = (150, 50, 255)
COLOR_ENEMY_SHOOTER = (200, 50, 200)
COLOR_ENEMY_ELITE = (100, 255, 255)
COLOR_BOSS = (255, 0, 100)
COLOR_BULLET = (255, 255, 100)
COLOR_BULLET_ENEMY = (255, 100, 100)
COLOR_SLIDER_BG = (40, 40, 60)
COLOR_SLIDER_FILL = (0, 255, 255)
COLOR_SLOW_TIME = (0, 150, 255)
COLOR_MAGNET = (255, 0, 150)
COLOR_INVINCIBLE = (255, 255, 100)
COLOR_UPGRADE = (255, 200, 50)
COLOR_XP = (150, 100, 255)
COLOR_CHEAT = (255, 0, 100)  # ✅ Цвет для читов
COLOR_COMBO = (255, 100, 200)
COLOR_ACHIEVEMENT = (255, 215, 0)
COLOR_CHAOS = (180, 0, 255)
COLOR_BONUS_WAVE = (0, 255, 255)

SHIP_COLORS = [
    (0, 255, 255, "Циан"),
    (255, 0, 100, "Розовый"),
    (0, 255, 100, "Зелёный"),
    (255, 200, 0, "Оранжевый"),
    (150, 100, 255, "Фиолетовый"),
    (255, 255, 255, "Белый"),
    (255, 100, 50, "Огонь"),
    (50, 100, 255, "Лёд")
]

SHIP_SHAPES = ["fighter", "circle", "triangle", "diamond", "stealth"]

DIFFICULTIES = {
    "easy": {"enemy_hp": 0.8, "enemy_speed": 0.8, "spawn_rate": 1.3, "enemy_damage": 0.7, "name": "Легко", "color": (50, 255, 50)},
    "normal": {"enemy_hp": 1.0, "enemy_speed": 1.0, "spawn_rate": 1.0, "enemy_damage": 1.0, "name": "Нормально", "color": (255, 255, 50)},
    "hard": {"enemy_hp": 1.5, "enemy_speed": 1.3, "spawn_rate": 0.7, "enemy_damage": 1.5, "name": "Сложно", "color": (255, 50, 50)},
    "extreme": {"enemy_hp": 2.5, "enemy_speed": 1.8, "spawn_rate": 0.4, "enemy_damage": 2.0, "name": "Экстрим", "color": (255, 0, 0)}
}

LANGUAGES = {
    "ru": {
        "play": "ИГРАТЬ", "shop": "МАГАЗИН", "settings": "НАСТРОЙКИ", "stats": "СТАТИСТИКА", "exit": "ВЫХОД",
        "infinite": "БЕСКОНЕЧНЫЙ", "story": "СЮЖЕТ", "easy": "Легко", "normal": "Нормально", "hard": "Сложно", "extreme": "Экстрим",
        "music": "Музыка", "sound": "Звуки", "volume": "Громкость", "language": "Язык", "back": "НАЗАД",
        "reset": "Сброс", "confirm": "Подтвердить", "cancel": "Отмена", "skins": "Корабли", "colors": "Цвета",
        "upgrades": "Улучшения", "level": "Уровень", "xp": "Опыт", "crystals": "Кристаллы",
        "operator": "ОПЕРАТОР", "cheats": "ЧИТЫ", "enabled": "ВКЛ", "disabled": "ВЫКЛ"
    },
    "en": {
        "play": "PLAY", "shop": "SHOP", "settings": "SETTINGS", "stats": "STATS", "exit": "EXIT",
        "infinite": "INFINITE", "story": "STORY", "easy": "Easy", "normal": "Normal", "hard": "Hard", "extreme": "Extreme",
        "music": "Music", "sound": "SFX", "volume": "Volume", "language": "Language", "back": "BACK",
        "reset": "Reset", "confirm": "Confirm", "cancel": "Cancel", "skins": "Ships", "colors": "Colors",
        "upgrades": "Upgrades", "level": "Level", "xp": "XP", "crystals": "Crystals",
        "operator": "OPERATOR", "cheats": "CHEATS", "enabled": "ON", "disabled": "OFF"
    }
}

# ✅ ИСПРАВЛЕННЫЙ СЮЖЕТ - 8 ГЛАВ
STORY_CHAPTERS = [
    {"id": 1, "title": "Первый контакт", "enemy_count": 30, "boss": False, "reward": 100},
    {"id": 2, "title": "Враг раскрыт", "enemy_count": 45, "boss": False, "reward": 200},
    {"id": 3, "title": "Босс сектора", "enemy_count": 60, "boss": True, "reward": 500},
    {"id": 4, "title": "Глубокий космос", "enemy_count": 75, "boss": False, "reward": 300},
    {"id": 5, "title": "Тайная база", "enemy_count": 90, "boss": True, "reward": 600},
    {"id": 6, "title": "Предательство", "enemy_count": 100, "boss": False, "reward": 400},
    {"id": 7, "title": "Флот вторжения", "enemy_count": 120, "boss": False, "reward": 700},
    {"id": 8, "title": "Финальная битва", "enemy_count": 180, "boss": True, "reward": 2000}
]

# 🎯 ДОСТИЖЕНИЯ
ACHIEVEMENTS = [
    {"id": "first_blood", "name": "Первая кровь", "desc": "Уничтожь первого врага", "icon": "⚔️", "unlocked": False},
    {"id": "combo_10", "name": "Комбо-мастер", "desc": "Достигни комбо x10", "icon": "🔥", "unlocked": False},
    {"id": "combo_50", "name": "Неудержимый", "desc": "Достигни комбо x50", "icon": "💥", "unlocked": False},
    {"id": "coins_1000", "name": "Коллекционер", "desc": "Собери 1000 монет", "icon": "💰", "unlocked": False},
    {"id": "level_10", "name": "Опытный пилот", "desc": "Достигни уровня 10", "icon": "⭐", "unlocked": False},
    {"id": "boss_slayer", "name": "Убийца боссов", "desc": "Победи 5 боссов", "icon": "👹", "unlocked": False},
    {"id": "survivor", "name": "Выживший", "desc": "Продержись 5 минут", "icon": "🛡️", "unlocked": False},
    {"id": "sharpshooter", "name": "Снайпер", "desc": "Уничтожь 100 врагов без урона", "icon": "🎯", "unlocked": False},
    {"id": "chaos_mode", "name": "Хаос", "desc": "Активируй режим хаоса", "icon": "🌀", "unlocked": False},
    {"id": "treasure_hunter", "name": "Охотник за сокровищами", "desc": "Найди 10 бонусных волн", "icon": "💎", "unlocked": False},
    {"id": "legend", "name": "Легенда", "desc": "Набери 10000 очков", "icon": "🏆", "unlocked": False},
    {"id": "speed_demon", "name": "Скоростной демон", "desc": "Используй рывок 50 раз", "icon": "⚡", "unlocked": False},
    {"id": "collector", "name": "Магнат", "desc": "Собери 5000 монет", "icon": "💎", "unlocked": False},
    {"id": "chapter_8", "name": "Герой Земли", "desc": "Пройди все 8 глав", "icon": "🌍", "unlocked": False}
]

# ============================================
# МЕНЕДЖЕР ТЕКСТУР
# ============================================

class TextureManager:
    def __init__(self):
        self.ships = {}
        self.items = {}
        self.enemies = {}
    
    def load_image(self, path, size=(50, 50)):
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                return img
            except Exception as e:
                print(f"⚠️ Ошибка {path}: {e}")
        return None
    
    def load_all(self):
        print("🎨 Загрузка текстур...")
        for shape in SHIP_SHAPES:
            path = os.path.join(SHIPS_DIR, f"{shape}.png")
            img = self.load_image(path, (50, 50))
            if img:
                self.ships[shape] = img
                print(f"✅ {shape}")
        
        items = ['coin', 'health', 'shield', 'powerup', 'bomb', 'dash', 'crystal', 'magnet']
        for item in items:
            path = os.path.join(ITEMS_DIR, f"{item}.png")
            img = self.load_image(path, (30, 30))
            if img:
                self.items[item] = img
        
        enemies = ['basic', 'fast', 'tank', 'shooter', 'elite']
        for enemy in enemies:
            path = os.path.join(ENEMIES_DIR, f"{enemy}.png")
            img = self.load_image(path, (45, 45))
            if img:
                self.enemies[enemy] = img
        print("🎨 Готово!")
    
    def get_ship(self, shape):
        return self.ships.get(shape)
    
    def get_item(self, item_type):
        return self.items.get(item_type)
    
    def get_enemy(self, enemy_type):
        return self.enemies.get(enemy_type)

texture_manager = TextureManager()

# ============================================
# КЛАССЫ ЭФФЕКТОВ
# ============================================

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 3)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)
        self.twinkle = random.uniform(0, math.pi * 2)
    
    def update(self, scroll_speed=0):
        self.y += self.speed + scroll_speed
        self.twinkle += 0.05
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface):
        brightness = int(self.brightness * (0.5 + 0.5 * math.sin(self.twinkle)))
        pygame.draw.circle(surface, (brightness, brightness, brightness), (int(self.x), int(self.y)), self.size)

class Particle:
    def __init__(self, x, y, color, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.life = life
        self.max_life = life
        angle = random.uniform(0, math.pi * 2)
        spd = random.uniform(2, 8)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95
        self.life -= 1
        self.size = max(1, self.size * 0.95)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
    
    def is_alive(self):
        return self.life > 0

class EngineTrail:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 15
        self.size = random.randint(4, 10)
        self.color = (random.randint(100, 255), random.randint(100, 200), 255)
    
    def update(self):
        self.y += 3
        self.life -= 1
        self.size *= 0.9
    
    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
    
    def is_alive(self):
        return self.life > 0

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 60
        self.vy = -2
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
    
    def update(self):
        self.y += self.vy
        self.life -= 1
    
    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (int(self.x), int(self.y)))
    
    def is_alive(self):
        return self.life > 0

class DashEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 15
        self.size = 60
    
    def update(self):
        self.life -= 1
        self.size += 3
    
    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, COLOR_DASH, (int(self.x), int(self.y)), int(self.size), 3)
    
    def is_alive(self):
        return self.life > 0

class Cutscene:
    def __init__(self, chapter_id):
        self.chapter_id = chapter_id
        self.stage = 0
        self.timer = 0
        self.text_alpha = 255
        self.text_fade = -2
        self.setup_texts()
    
    def setup_texts(self):
        texts_map = {
            1: ["Земля, 2157 год...", "Неизвестные сигналы", "Твой корабль готов", "Удачи!"],
            2: ["Враг - пираты!", "Угрожают путям", "Уничтожь их!", "В бой!"],
            3: ["Флагман пиратов!", "Командир в бою", "Это твой шанс!", "ПОБЕДИ!"],
            4: ["Пираты отступают", "К астероидам", "Опасная зона", "Преследуй!"],
            5: ["Секретная база!", "Здесь их сокровища", "Уничтожь!", "Время не ждёт!"],
            6: ["Предатель среди нас", "Сливает информацию", "Найди его!", "Доверяй себе..."],
            7: ["Флот вторжения!", "Тысячи кораблей", "Это ВОЙНА!", "Земля нуждается в тебе!"],
            8: ["ФИНАЛЬНАЯ БИТВА", "Материнский корабль", "Судьба Земли!", "ПОБЕДИ ИЛИ ПРОИГРАЙ!"]
        }
        self.texts = texts_map.get(self.chapter_id, ["Миссия началась!", "Уничтожь врагов!"])
    
    def update(self):
        self.timer += 1
        self.text_alpha += self.text_fade
        if self.text_alpha <= 0:
            self.text_alpha = 0
            self.text_fade = 2
        if self.text_alpha >= 255:
            self.text_alpha = 255
            self.text_fade = -2
        if self.timer > 120:
            self.timer = 0
            self.stage += 1
            self.text_alpha = 0
    
    def is_finished(self):
        return self.stage >= len(self.texts)
    
    def get_current_text(self):
        if self.stage < len(self.texts):
            return self.texts[self.stage]
        return ""
    
    def draw(self, surface):
        if self.stage < len(self.texts):
            for y in range(SCREEN_HEIGHT):
                alpha = int(200 * (1 - y / SCREEN_HEIGHT))
                overlay = pygame.Surface((SCREEN_WIDTH, 1))
                overlay.set_alpha(alpha)
                overlay.fill((0, 0, 0))
                surface.blit(overlay, (0, y))
            text = self.get_current_text()
            font = pygame.font.SysFont("Arial", 28, bold=True)
            text_surface = font.render(text, True, COLOR_TEXT)
            text_surface.set_alpha(self.text_alpha)
            surface.blit(text_surface, (SCREEN_WIDTH//2 - text_surface.get_width()//2, SCREEN_HEIGHT//2))
            chapter_font = pygame.font.SysFont("Arial", 20)
            chapter_text = chapter_font.render(f"Глава {self.chapter_id}", True, COLOR_TEXT)
            chapter_text.set_alpha(self.text_alpha)
            surface.blit(chapter_text, (SCREEN_WIDTH//2 - chapter_text.get_width()//2, SCREEN_HEIGHT//2 - 50))

# 🎯 КЛАСС ДОСТИЖЕНИЙ
class AchievementManager:
    def __init__(self):
        self.achievements = []
        for ach in ACHIEVEMENTS:
            self.achievements.append(ach.copy())
        self.new_unlocks = []
    
    def check_and_unlock(self, player, game_stats):
        """Проверка достижений и разблокировка"""
        unlocked = []
        
        # Первая кровь
        if game_stats.get('total_kills', 0) >= 1:
            self._unlock_achievement('first_blood', unlocked)
        
        # Комбо 10
        if player.combo >= 10:
            self._unlock_achievement('combo_10', unlocked)
        
        # Комбо 50
        if player.combo >= 50:
            self._unlock_achievement('combo_50', unlocked)
        
        # Коллекционер
        if player.coins >= 1000 or game_stats.get('total_coins', 0) >= 1000:
            self._unlock_achievement('coins_1000', unlocked)
        
        # Уровень 10
        if player.level >= 10:
            self._unlock_achievement('level_10', unlocked)
        
        # Убийца боссов
        if game_stats.get('bosses_defeated', 0) >= 5:
            self._unlock_achievement('boss_slayer', unlocked)
        
        # Выживший (5 минут = 300 секунд = 18000 кадров при 60 FPS)
        if game_stats.get('survival_time', 0) >= 18000:
            self._unlock_achievement('survivor', unlocked)
        
        # Охотник за сокровищами
        if game_stats.get('bonus_waves_found', 0) >= 10:
            self._unlock_achievement('treasure_hunter', unlocked)
        
        # Легенда - 10000 очков
        if player.score >= 10000 or game_stats.get('highest_score', 0) >= 10000:
            self._unlock_achievement('legend', unlocked)
        
        # Скоростной демон - 50 рывков
        if game_stats.get('total_dashes', 0) >= 50:
            self._unlock_achievement('speed_demon', unlocked)
        
        # Магнат - 5000 монет
        if player.coins >= 5000 or game_stats.get('total_coins', 0) >= 5000:
            self._unlock_achievement('collector', unlocked)
        
        # Герой Земли - пройдена 8 глава
        if game_stats.get('story_progress', 0) >= 8:
            self._unlock_achievement('chapter_8', unlocked)
        
        return unlocked
    
    def _unlock_achievement(self, ach_id, unlocked_list):
        for ach in self.achievements:
            if ach['id'] == ach_id and not ach['unlocked']:
                ach['unlocked'] = True
                unlocked_list.append(ach)
                self.new_unlocks.append(ach)
                break
    
    def draw_notifications(self, surface):
        """Отрисовка уведомлений о новых достижениях"""
        y_offset = SCREEN_HEIGHT - 100
        for i, ach in enumerate(self.new_unlocks[-3:]):  # Показываем последние 3
            alpha = min(255, (len(self.new_unlocks) - i) * 80)
            overlay = pygame.Surface((SCREEN_WIDTH, 60))
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, y_offset - i * 65))
            
            icon_font = pygame.font.SysFont("Arial", 30)
            icon = icon_font.render(ach['icon'], True, COLOR_ACHIEVEMENT)
            surface.blit(icon, (20, y_offset - i * 65 + 10))
            
            name_font = pygame.font.SysFont("Arial", 18, bold=True)
            name = name_font.render(f"🏆 {ach['name']}!", True, COLOR_ACHIEVEMENT)
            surface.blit(name, (70, y_offset - i * 65 + 5))
            
            desc_font = pygame.font.SysFont("Arial", 14)
            desc = desc_font.render(ach['desc'], True, COLOR_TEXT)
            surface.blit(desc, (70, y_offset - i * 65 + 30))

# ============================================
# ИГРОВЫЕ ОБЪЕКТЫ
# ============================================

class Player(pygame.sprite.Sprite):
    def __init__(self, shape_type="fighter", color=COLOR_PLAYER):
        super().__init__()
        self.shape_type = shape_type
        self.color = color
        self.health = 100
        self.max_health = 100
        self.shield = 0
        self.max_shield = 50
        self.score = 0
        self.coins = 0
        self.crystals = 0
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.combo = 0
        self.combo_multiplier = 1.0
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.weapon_level = 1
        self.dual_bullets = False
        self.rapid_fire = False
        self.speed_boost = False
        self.invincible = False
        self.invincible_timer = 0
        self.size = 50
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 150
        self.sprite_image = texture_manager.get_ship(shape_type)
        self.update_shape()
        self.target_x = self.rect.centerx
        self.target_y = self.rect.centery
        self.thrust = 0
        self.tilt = 0
        self.dash_available = True
        self.dash_cooldown = 90
        self.dash_timer = 0
        self.is_dashing = False
        self.dash_duration = 12
        self.dash_speed = 25
        self.dash_direction = (0, 0)
        self.last_touch_time = 0
        self.slow_time = False
        self.slow_time_timer = 0
        self.magnet = False
        self.magnet_timer = 0
        self.invincible_ability = False
        self.invincible_ability_timer = 0

    def update_shape(self):
        self.image.fill((0, 0, 0, 0))
        if self.sprite_image:
            self.image = self.sprite_image.copy()
            self.rect = self.image.get_rect(center=self.rect.center)
            return
        if self.shape_type == "fighter":
            points = [(self.size//2, 0), (0, self.size), (self.size//2, self.size-10), (self.size, self.size)]
            pygame.draw.polygon(self.image, self.color, points)
            pygame.draw.circle(self.image, (100, 200, 255), (self.size//2, self.size//2), 8)
        elif self.shape_type == "circle":
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2)
        elif self.shape_type == "triangle":
            points = [(self.size//2, 0), (0, self.size), (self.size, self.size)]
            pygame.draw.polygon(self.image, self.color, points)
        elif self.shape_type == "diamond":
            points = [(self.size//2, 0), (self.size, self.size//2), (self.size//2, self.size), (0, self.size//2)]
            pygame.draw.polygon(self.image, self.color, points)
        elif self.shape_type == "stealth":
            points = [(self.size//2, 0), (self.size//4, self.size//2), (0, self.size), (self.size, self.size), (3*self.size//4, self.size//2)]
            pygame.draw.polygon(self.image, self.color, points)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.slow_time and self.slow_time_timer > 0:
            self.slow_time_timer -= 1
        if self.magnet and self.magnet_timer > 0:
            self.magnet_timer -= 1
        if self.invincible_ability and self.invincible_ability_timer > 0:
            self.invincible_ability_timer -= 1
        if self.is_dashing:
            self.dash_duration -= 1
            if self.dash_direction != (0, 0):
                self.rect.centerx += self.dash_direction[0] * self.dash_speed
                self.rect.centery += self.dash_direction[1] * self.dash_speed
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.invincible = False
            return
        dx = self.target_x - self.rect.centerx
        dy = self.target_y - self.rect.centery
        speed_mult = 1.3 if self.speed_boost else 1.0
        self.rect.centerx += dx * 0.15 * speed_mult
        self.rect.centery += dy * 0.15 * speed_mult
        self.tilt = dx * 0.5
        self.tilt = max(-30, min(30, self.tilt))
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        if self.shield > 0:
            self.shield -= 0.03
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dash_available = True

    def move_to(self, x, y):
        if not self.is_dashing:
            self.target_x = x
            self.target_y = y
            self.thrust = min(10, self.thrust + 1)

    def decrease_thrust(self):
        self.thrust = max(0, self.thrust - 0.5)

    def dash(self, direction=None):
        if not (self.dash_available and not self.is_dashing):
            return False
        self.is_dashing = True
        self.dash_available = False
        self.dash_timer = self.dash_cooldown
        self.dash_duration = 12
        self.invincible = True
        self.invincible_timer = 12
        
        # Счётчик рывков для достижения
        game_stats['total_dashes'] = game_stats.get('total_dashes', 0) + 1
        
        if direction:
            self.dash_direction = direction
        else:
            self.dash_direction = (0, -1)
        return True

    def check_double_tap(self, current_time):
        time_diff = current_time - self.last_touch_time
        self.last_touch_time = current_time
        return time_diff < 300

    def shoot(self):
        now = pygame.time.get_ticks()
        delay = self.shoot_delay / 2 if self.rapid_fire else self.shoot_delay
        if now - self.last_shot > delay:
            self.last_shot = now
            bullets = []
            if self.weapon_level >= 2 or self.dual_bullets:
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top, 0))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top, 0))
            else:
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0))
            if self.weapon_level >= 3:
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top, -0.3))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top, 0.3))
            return bullets
        return []

    def take_damage(self, amount):
        if self.invincible:
            return False
        if self.shield > 0:
            self.shield = max(0, self.shield - amount * 2)
            return False
        self.health -= amount
        self.invincible = True
        self.invincible_timer = 60
        return self.health <= 0

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def add_shield(self, amount):
        self.shield = min(self.max_shield, self.shield + amount)

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.level += 1
            self.xp -= self.xp_to_next
            self.xp_to_next = int(self.xp_to_next * 1.5)
            self.max_health += 10
            self.health = self.max_health
            return True
        return False

    def add_combo(self):
        self.combo += 1
        self.combo_multiplier = 1.0 + (self.combo / 10) * 0.5

    def reset_combo(self):
        self.combo = 0
        self.combo_multiplier = 1.0

    def draw(self, surface):
        if self.invincible and pygame.time.get_ticks() % 100 < 50:
            return
        rotated = pygame.transform.rotate(self.image.copy(), -self.tilt)
        surface.blit(rotated, rotated.get_rect(center=self.rect.center))
        if self.shield > 0:
            pygame.draw.circle(surface, COLOR_SHIELD, self.rect.center, int(self.size * 0.8), 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type=None, difficulty=1.0):
        super().__init__()
        self.type = enemy_type if enemy_type else random.choice(['basic', 'fast', 'tank', 'shooter', 'elite'])
        self.difficulty = difficulty
        self.setup_stats()
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.rect.y = random.randint(-100, -40)
        self.health = self.max_health
        self.shoot_timer = random.randint(0, 60)
        self.sprite_image = texture_manager.get_enemy(self.type)
        self.draw_enemy()
        self.start_x = self.rect.x
        self.move_pattern = random.choice(['straight', 'sine', 'zigzag'])
        self.move_timer = 0

    def setup_stats(self):
        stats = {
            'basic': {'size': 45, 'hp': 35, 'speed': 3.0, 'score': 15, 'damage': 30, 'shoot': False},
            'fast': {'size': 35, 'hp': 25, 'speed': 6.0, 'score': 25, 'damage': 25, 'shoot': False},
            'tank': {'size': 70, 'hp': 120, 'speed': 2.0, 'score': 40, 'damage': 50, 'shoot': True, 'interval': 150},
            'shooter': {'size': 50, 'hp': 60, 'speed': 2.5, 'score': 35, 'damage': 35, 'shoot': True, 'interval': 80},
            'elite': {'size': 60, 'hp': 150, 'speed': 4.0, 'score': 75, 'damage': 45, 'shoot': True, 'interval': 50}
        }
        s = stats.get(self.type, stats['basic'])
        self.size = s['size']
        self.max_health = s['hp'] * self.difficulty
        self.speed_y = s['speed'] * self.difficulty
        self.score_value = s['score']
        self.damage = s['damage'] * self.difficulty
        self.can_shoot = s.get('shoot', False)
        self.shoot_interval = s.get('interval', 100)
        self.speed_x = 2 if self.type in ['fast', 'elite'] else 0
        self.color = {'basic': COLOR_ENEMY_BASIC, 'fast': COLOR_ENEMY_FAST, 'tank': COLOR_ENEMY_TANK, 
                      'shooter': COLOR_ENEMY_SHOOTER, 'elite': COLOR_ENEMY_ELITE}.get(self.type, COLOR_ENEMY_BASIC)

    def draw_enemy(self):
        self.image.fill((0, 0, 0, 0))
        if self.sprite_image:
            self.image = self.sprite_image.copy()
            return
        if self.type == 'basic':
            pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size))
        elif self.type == 'fast':
            pygame.draw.polygon(self.image, self.color, [(self.size//2, 0), (0, self.size), (self.size, self.size)])
        elif self.type == 'tank':
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2)
        elif self.type == 'shooter':
            pygame.draw.rect(self.image, self.color, (10, 0, self.size-20, self.size))
        elif self.type == 'elite':
            pygame.draw.polygon(self.image, self.color, [(self.size//2, 0), (self.size, self.size//3), (self.size//2, self.size), (0, self.size//3)])

    def update(self, player=None):
        self.move_timer += 1
        if self.move_pattern == 'straight':
            self.rect.y += self.speed_y
        elif self.move_pattern == 'sine':
            self.rect.y += self.speed_y
            self.rect.x = self.start_x + math.sin(self.move_timer * 0.05) * 50
        elif self.move_pattern == 'zigzag':
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x if self.move_timer % 60 < 30 else -self.speed_x
        if self.can_shoot and player:
            self.shoot_timer += 1
            if self.shoot_timer > self.shoot_interval / self.difficulty:
                self.shoot_timer = 0
                return EnemyBullet(self.rect.centerx, self.rect.bottom)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        return None

class Boss(pygame.sprite.Sprite):
    def __init__(self, level=1):
        super().__init__()
        self.level = level
        self.size = 140
        self.max_health = 500 * level
        self.health = self.max_health
        self.color = COLOR_BOSS
        self.phase = 1
        self.move_timer = 0
        self.move_direction = 1
        self.attack_pattern = 0
        self.attack_timer = 0
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = -50
        self.target_y = 100
        self.draw_boss()

    def draw_boss(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image, self.color, [(self.size//2, 0), (self.size, self.size//3), (self.size*3//4, self.size), (self.size//4, self.size), (0, self.size//3)])
        pygame.draw.circle(self.image, (255, 50, 100), (self.size//2, self.size//2), 40)

    def update(self):
        self.move_timer += 1
        self.attack_timer += 1
        if self.rect.y < self.target_y:
            self.rect.y += 2
            return None
        self.rect.x += self.move_direction * 3
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.move_direction *= -1
        attacks = []
        if self.attack_timer > 30:
            self.attack_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 3
            if self.attack_pattern == 0:
                attacks.append(('spread', self.rect.centerx, self.rect.bottom))
            elif self.attack_pattern == 1:
                for i in range(7):
                    attacks.append(('straight', self.rect.centerx + (i-3)*20, self.rect.bottom))
            else:
                attacks.append(('circle', self.rect.centerx, self.rect.bottom))
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.color = (255, 50, 50)
        return attacks if attacks else None

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0):
        super().__init__()
        self.image = pygame.Surface((8, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLOR_BULLET, (0, 0, 8, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -14
        self.vx = math.sin(angle) * 5 if angle else 0

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.vx
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, speed=6):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLOR_BULLET_ENEMY, (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vy = math.cos(angle) * speed if angle else speed
        self.vx = math.sin(angle) * speed if angle else 0

    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = random.choice(['coin', 'health', 'shield', 'powerup', 'bomb', 'dash', 'crystal'])
        self.size = 30
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.sprite_image = texture_manager.get_item(self.type)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.draw_bonus()

    def draw_bonus(self):
        self.image.fill((0, 0, 0, 0))
        if self.sprite_image:
            self.image = self.sprite_image.copy()
            return
        colors = {'coin': COLOR_COIN, 'health': (0, 255, 100), 'shield': COLOR_SHIELD, 'powerup': (255, 0, 255), 'bomb': (255, 100, 0), 'dash': COLOR_DASH, 'crystal': COLOR_CRYSTAL}
        if self.type == 'coin':
            pygame.draw.circle(self.image, colors[self.type], (15, 15), 15)
        elif self.type == 'health':
            pygame.draw.rect(self.image, colors[self.type], (10, 5, 10, 20))
            pygame.draw.rect(self.image, colors[self.type], (5, 10, 20, 10))
        else:
            pygame.draw.circle(self.image, colors.get(self.type, COLOR_TEXT), (15, 15), 15)

    def update(self):
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ============================================
# МЕНЕДЖЕР ДАННЫХ
# ============================================

class DataManager:
    def __init__(self):
        self.data = {
            "coins": 0, "crystals": 0, "total_coins": 0, "highscore": 0, "total_kills": 0,
            "games_played": 0, "unlocked_skins": ["fighter"], "unlocked_colors": [0],
            "current_skin": "fighter", "current_color": 0, "story_progress": 0,
            "tutorial_completed": False, "difficulty": "normal", "game_mode": "story",
            "music_enabled": True, "volume": 0.7, "language": "ru",
            "dual_bullets": False, "rapid_fire": False, "speed_boost": False, "max_health": 100,
            "player_level": 1, "player_xp": 0,
            # ✅ ЧИТЫ
            "operator_mode": False,
            "cheat_god_mode": False,
            "cheat_infinite_dash": False,
            "cheat_instant_kill": False,
            "cheat_max_weapon": False,
            # 🎯 Статистика для достижений
            "total_dashes": 0,
            "bosses_defeated": 0,
            "bonus_waves_found": 0,
            "highest_score": 0,
            "achievements": []
        }
        self.load()

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for key in self.data:
                        if key in loaded:
                            self.data[key] = loaded[key]
            except Exception as e:
                print(f"Ошибка: {e}")

    def save(self):
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def buy_skin(self, skin_name, cost):
        if skin_name not in self.data["unlocked_skins"] and self.data["coins"] >= cost:
            self.data["coins"] -= cost
            self.data["unlocked_skins"].append(skin_name)
            self.save()
            return True
        return False

    def buy_color(self, color_index, cost):
        if color_index not in self.data["unlocked_colors"] and self.data["coins"] >= cost:
            self.data["coins"] -= cost
            self.data["unlocked_colors"].append(color_index)
            self.save()
            return True
        return False

    def reset_progress(self):
        self.data = {
            "coins": 0, "crystals": 0, "total_coins": 0, "highscore": 0, "total_kills": 0,
            "games_played": 0, "unlocked_skins": ["fighter"], "unlocked_colors": [0],
            "current_skin": "fighter", "current_color": 0, "story_progress": 0,
            "tutorial_completed": False, "difficulty": "normal", "game_mode": "story",
            "music_enabled": True, "volume": 0.7, "language": "ru",
            "dual_bullets": False, "rapid_fire": False, "speed_boost": False, "max_health": 100,
            "player_level": 1, "player_xp": 0,
            "operator_mode": False, "cheat_god_mode": False, "cheat_infinite_dash": False,
            "cheat_instant_kill": False, "cheat_max_weapon": False,
            "total_dashes": 0,
            "bosses_defeated": 0,
            "bonus_waves_found": 0,
            "highest_score": 0,
            "achievements": []
        }
        self.save()

# ============================================
# АУДИО МЕНЕДЖЕР
# ============================================

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_loaded = False
        try:
            pygame.mixer.init()
            if os.path.exists(MUSIC_DIR):
                for f in os.listdir(MUSIC_DIR):
                    if f.endswith(('.mp3', '.ogg', '.wav')):
                        path = os.path.join(MUSIC_DIR, f)
                        try:
                            pygame.mixer.music.load(path)
                            self.music_loaded = True
                            print(f"🎵 Музыка: {f}")
                            break
                        except Exception as e:
                            print(f"⚠️ Не удалось загрузить {f}: {e}")
        except Exception as e:
            print(f"⚠️ Аудио: {e}")

    def play_music(self):
        if self.music_loaded:
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def set_volume(self, volume):
        try:
            pygame.mixer.music.set_volume(volume)
        except:
            pass

# ============================================
# ГЛАВНЫЙ КЛАСС ИГРЫ
# ============================================

class Game:
    def __init__(self):
        pygame.init()
        
        # 1. Создаём окно
        try:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            global SCREEN_WIDTH, SCREEN_HEIGHT
            SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
        except:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 2. ТЕПЕРЬ загружаем текстуры (после окна!)
        texture_manager.load_all()
        
        pygame.display.set_caption("Neon Space: Galactic War")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.dm = DataManager()
        self.audio = AudioManager()
        self.audio.set_volume(self.dm.data["volume"])
        
        self.state = "MENU"
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.player = None
        self.boss = None
        self.boss_active = False
        self.stars = [Star() for _ in range(100)]
        self.particles = []
        self.trails = []
        self.dash_effects = []
        self.floating_texts = []
        self.enemy_spawn_timer = 0
        self.enemies_killed = 0
        self.enemies_to_spawn = 30
        self.combo_timer = 0
        self.mission_complete = False
        self.cutscene = None
        self.cutscene_active = False
        self.shop_page = "skins"
        self.settings_page = "main"  # ✅ Для переключения настроек/читов
        self.reset_confirm = False
        self.show_cursor = True
        self.slider_dragging = False
        self.slider_rect = pygame.Rect(100, 120, SCREEN_WIDTH-200, 20)
        self.cursor_pos = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
        # ✅ Кнопка читов в игре
        self.cheat_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 60, 40, 40)
        self.cheats_open = False
        
        # 🎯 Менеджер достижений
        self.achievement_manager = AchievementManager()
        
        # 🌀 Режим хаоса
        self.chaos_mode = False
        self.chaos_timer = 0
        
        # 💎 Бонусные волны
        self.bonus_wave_active = False
        self.bonus_wave_timer = 0
        self.bonus_waves_found = 0
        
        # ⏱️ Время выживания
        self.survival_time = 0
        
        if self.dm.data["music_enabled"] and self.audio.music_loaded:
            self.audio.play_music()

    def get_lang(self, key):
        return LANGUAGES.get(self.dm.data["language"], LANGUAGES["ru"]).get(key, key)

    def spawn_enemy(self):
        diff = DIFFICULTIES.get(self.dm.data["difficulty"], DIFFICULTIES["normal"])
        enemy = Enemy(difficulty=diff["enemy_hp"])
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def spawn_boss(self):
        self.boss = Boss()
        self.all_sprites.add(self.boss)
        self.boss_active = True

    def create_explosion(self, x, y, color):
        for _ in range(15):
            self.particles.append(Particle(x, y, color))

    def create_floating_text(self, x, y, text, color):
        self.floating_texts.append(FloatingText(x, y, text, color))

    def start_cutscene(self, chapter_id):
        if chapter_id < 1:
            chapter_id = 1
        if chapter_id > len(STORY_CHAPTERS):
            chapter_id = len(STORY_CHAPTERS)
        self.cutscene = Cutscene(chapter_id)
        self.cutscene_active = True

    def reset_game(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.bonuses.empty()
        self.particles = []
        self.trails = []
        self.dash_effects = []
        self.floating_texts = []
        
        color = SHIP_COLORS[self.dm.data["current_color"]][0]
        skin = self.dm.data["current_skin"]
        self.player = Player(shape_type=skin, color=color)
        self.player.dual_bullets = self.dm.data.get("dual_bullets", False)
        self.player.rapid_fire = self.dm.data.get("rapid_fire", False)
        self.player.speed_boost = self.dm.data.get("speed_boost", False)
        self.player.max_health = self.dm.data.get("max_health", 100)
        self.player.health = self.player.max_health
        self.player.level = self.dm.data.get("player_level", 1)
        
        # ✅ Применяем читы
        if self.dm.data["cheat_god_mode"]:
            self.player.invincible = True
        if self.dm.data["cheat_infinite_dash"]:
            self.player.dash_cooldown = 0
        if self.dm.data["cheat_max_weapon"]:
            self.player.weapon_level = 3
        
        self.all_sprites.add(self.player)
        
        self.boss = None
        self.boss_active = False
        self.enemy_spawn_timer = 0
        self.enemies_killed = 0
        
        if self.dm.data["game_mode"] == "story":
            chapter = self.dm.data["story_progress"]
            if chapter < len(STORY_CHAPTERS):
                self.enemies_to_spawn = STORY_CHAPTERS[chapter]["enemy_count"]
            else:
                self.enemies_to_spawn = 30
        else:
            self.enemies_to_spawn = 999
        
        self.combo_timer = 0
        self.mission_complete = False

    def handle_input(self):
        pos = pygame.mouse.get_pos()
        self.cursor_pos = pos
        pressed = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if event.button == 1:
                    if self.cutscene_active:
                        self.cutscene.stage = len(self.cutscene.texts)
                    elif self.cheats_open:
                        self.check_cheat_clicks(mx, my)
                    else:
                        self.check_ui_clicks(mx, my)
                    
                    # ✅ Кнопка читов в игре
                    if self.state == "GAME" and self.dm.data["operator_mode"]:
                        if self.cheat_button_rect.collidepoint(mx, my):
                            self.cheats_open = not self.cheats_open
                    
                    if self.state == "GAME" and self.player and not self.cheats_open:
                        if self.player.check_double_tap(current_time):
                            if self.player.dash():
                                self.create_floating_text(self.player.rect.centerx, self.player.rect.y, "DASH!", COLOR_DASH)
            if event.type == pygame.MOUSEBUTTONUP:
                self.slider_dragging = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.cheats_open:
                        self.cheats_open = False
                    elif self.state == "GAME":
                        self.state = "PAUSE"
                    elif self.state == "PAUSE":
                        self.state = "GAME"
                    elif self.state in ["SHOP", "SETTINGS"]:
                        self.state = "MENU"
                if event.key == pygame.K_SPACE and self.state == "GAME":
                    if self.player and self.player.dash():
                        self.create_floating_text(self.player.rect.centerx, self.player.rect.y, "DASH!", COLOR_DASH)
        
        if self.slider_dragging and self.state == "SETTINGS":
            if not pressed[0]:
                self.slider_dragging = False
            else:
                slider_x = max(100, min(pos[0], SCREEN_WIDTH - 100))
                volume = (slider_x - 100) / (SCREEN_WIDTH - 200)
                self.dm.data["volume"] = volume
                self.audio.set_volume(volume)
                self.dm.save()
        
        if self.cutscene_active:
            return
        if self.state == "GAME" and self.player and not self.player.is_dashing and not self.cheats_open:
            self.player.move_to(pos[0], pos[1])
            if pressed[0]:
                bullets = self.player.shoot()
                for bullet in bullets:
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
        else:
            if self.player:
                self.player.decrease_thrust()

    def check_cheat_clicks(self, x, y):
        """✅ Обработка кликов по читам"""
        cheats = [
            ("cheat_god_mode", "Бессмертие", 200),
            ("cheat_infinite_dash", "Бесконечный рывок", 280),
            ("cheat_instant_kill", "Мгновенное убийство", 360),
            ("cheat_max_weapon", "Макс. оружие", 440),
            ("add_coins", "+1000 монет", 520),
            ("add_crystals", "+100 кристаллов", 600)
        ]
        
        for cheat_key, cheat_name, y_pos in cheats:
            rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_pos, 300, 50)
            if rect.collidepoint(x, y):
                if cheat_key.startswith("add_"):
                    if cheat_key == "add_coins":
                        self.player.coins += 1000
                        self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "+1000 💰", COLOR_COIN)
                    elif cheat_key == "add_crystals":
                        self.player.crystals += 100
                        self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "+100 💎", COLOR_CRYSTAL)
                else:
                    self.dm.data[cheat_key] = not self.dm.data[cheat_key]
                    self.dm.save()
                    # Применяем чит сразу
                    if cheat_key == "cheat_god_mode" and self.player:
                        self.player.invincible = self.dm.data[cheat_key]
                    elif cheat_key == "cheat_infinite_dash" and self.player:
                        self.player.dash_cooldown = 0 if self.dm.data[cheat_key] else 90
                    elif cheat_key == "cheat_max_weapon" and self.player:
                        self.player.weapon_level = 3 if self.dm.data[cheat_key] else 1
                self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, f"{cheat_name}!", COLOR_CHEAT)
                return
        
        # Закрыть читы
        close_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 680, 200, 50)
        if close_rect.collidepoint(x, y):
            self.cheats_open = False

    def check_ui_clicks(self, x, y):
        if self.state == "MENU":
            if 100 < x < SCREEN_WIDTH-100 and 250 < y < 310:
                self.state = "MODE_SELECT"
            elif 100 < x < SCREEN_WIDTH-100 and 340 < y < 400:
                self.state = "SHOP"
            elif 100 < x < SCREEN_WIDTH-100 and 430 < y < 490:
                self.state = "SETTINGS"
            elif 100 < x < SCREEN_WIDTH-100 and 520 < y < 580:
                self.state = "STATS"
            elif 100 < x < SCREEN_WIDTH-100 and 610 < y < 670:
                self.running = False
        elif self.state == "MODE_SELECT":
            if 100 < x < SCREEN_WIDTH-100 and 320 < y < 380:
                self.dm.data["game_mode"] = "infinite"
                self.state = "DIFFICULTY_SELECT"
            elif 100 < x < SCREEN_WIDTH-100 and 420 < y < 480:
                self.dm.data["game_mode"] = "story"
                self.state = "DIFFICULTY_SELECT"
            elif 20 < x < 120 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                self.state = "MENU"
        elif self.state == "DIFFICULTY_SELECT":
            if 100 < x < SCREEN_WIDTH-100 and 220 < y < 280:
                self.dm.data["difficulty"] = "easy"
                self.dm.save()
                self.start_game()
            elif 100 < x < SCREEN_WIDTH-100 and 310 < y < 370:
                self.dm.data["difficulty"] = "normal"
                self.dm.save()
                self.start_game()
            elif 100 < x < SCREEN_WIDTH-100 and 400 < y < 460:
                self.dm.data["difficulty"] = "hard"
                self.dm.save()
                self.start_game()
            elif 100 < x < SCREEN_WIDTH-100 and 490 < y < 550:
                self.dm.data["difficulty"] = "extreme"
                self.dm.save()
                self.start_game()
            elif 20 < x < 120 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                self.state = "MENU"
        elif self.state == "SHOP":
            if 20 < x < 120 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                self.state = "MENU"
            if 30 < x < 150 and 100 < y < 140:
                self.shop_page = "skins"
            elif 160 < x < 280 and 100 < y < 140:
                self.shop_page = "colors"
            if self.shop_page == "skins":
                skins = [("fighter", 0), ("circle", 100), ("triangle", 250), ("diamond", 500), ("stealth", 750)]
                for i, (key, cost) in enumerate(skins):
                    btn_y = 180 + i * 90
                    if (SCREEN_WIDTH//2 - 150) < x < (SCREEN_WIDTH//2 + 150) and btn_y < y < btn_y + 75:
                        if key in self.dm.data["unlocked_skins"]:
                            self.dm.data["current_skin"] = key
                            self.dm.save()
                        else:
                            self.dm.buy_skin(key, cost)
            elif self.shop_page == "colors":
                for i, (r, g, b, name) in enumerate(SHIP_COLORS):
                    btn_y = 180 + i * 75
                    if (SCREEN_WIDTH//2 - 150) < x < (SCREEN_WIDTH//2 + 150) and btn_y < y < btn_y + 65:
                        cost = i * 100 if i > 0 else 0
                        if i in self.dm.data["unlocked_colors"]:
                            self.dm.data["current_color"] = i
                            self.dm.save()
                        else:
                            self.dm.buy_color(i, cost)
        elif self.state == "SETTINGS":
            if 20 < x < 120 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                self.state = "MENU"
            # Вкладки настроек
            if 30 < x < 200 and 80 < y < 120:
                self.settings_page = "main"
            elif 210 < x < 380 and 80 < y < 120:
                self.settings_page = "operator"
            if self.settings_page == "main":
                if self.slider_rect.collidepoint(x, y):
                    self.slider_dragging = True
                if 100 < x < SCREEN_WIDTH//2 - 40 and 190 < y < 230:
                    self.dm.data["volume"] = max(0.0, self.dm.data["volume"] - 0.1)
                    self.dm.save()
                if SCREEN_WIDTH//2 + 40 < x < SCREEN_WIDTH-100 and 190 < y < 230:
                    self.dm.data["volume"] = min(1.0, self.dm.data["volume"] + 0.1)
                    self.dm.save()
                if 100 < x < SCREEN_WIDTH-100 and 270 < y < 330:
                    self.dm.data["music_enabled"] = not self.dm.data["music_enabled"]
                    if self.dm.data["music_enabled"]:
                        self.audio.play_music()
                    else:
                        self.audio.stop_music()
                    self.dm.save()
                if 100 < x < SCREEN_WIDTH-100 and 570 < y < 630:
                    self.reset_confirm = True
            elif self.settings_page == "operator":
                # ✅ Переключатель режима оператора
                if 100 < x < SCREEN_WIDTH-100 and 200 < y < 260:
                    self.dm.data["operator_mode"] = not self.dm.data["operator_mode"]
                    self.dm.save()
        if self.reset_confirm:
            if 100 < x < SCREEN_WIDTH//2 - 20 and 360 < y < 420:
                self.dm.reset_progress()
                self.reset_confirm = False
            elif SCREEN_WIDTH//2 + 20 < x < SCREEN_WIDTH-100 and 360 < y < 420:
                self.reset_confirm = False
        elif self.state == "STATS":
            if 20 < x < 120 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                self.state = "MENU"
        elif self.state == "GAMEOVER":
            if 100 < x < SCREEN_WIDTH-100 and 380 < y < 440:
                self.reset_game()
                self.state = "GAME"
            elif 100 < x < SCREEN_WIDTH-100 and 480 < y < 540:
                self.dm.save()
                self.state = "MENU"
        elif self.state == "PAUSE":
            if 100 < x < SCREEN_WIDTH-100 and 380 < y < 440:
                self.state = "GAME"
            elif 100 < x < SCREEN_WIDTH-100 and 480 < y < 540:
                self.dm.save()
                self.state = "MENU"
        elif self.state == "MISSION_COMPLETE":
            if 100 < x < SCREEN_WIDTH-100 and 480 < y < 540:
                if self.dm.data["game_mode"] == "story":
                    self.dm.data["story_progress"] += 1
                    self.dm.save()
                self.state = "MENU"

    def start_game(self):
        self.reset_game()
        self.state = "GAME"
        self.dm.data["games_played"] += 1
        self.dm.save()

    def update_game(self):
        # ⏱️ Обновляем время выживания
        self.survival_time += 1
        
        # 🌀 Режим хаоса
        if self.chaos_mode:
            self.chaos_timer -= 1
            if self.chaos_timer <= 0:
                self.chaos_mode = False
                self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "ХАОС ЗАВЕРШЁН!", COLOR_TEXT)
        
        # 💎 Проверка бонусной волны (10% шанс каждые 30 секунд)
        if not self.bonus_wave_active and self.survival_time % 1800 == 0 and random.random() < 0.3:
            self.bonus_wave_active = True
            self.bonus_wave_timer = 600  # 10 секунд
            self.bonus_waves_found += 1
            self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "БОНУСНАЯ ВОЛНА!", COLOR_BONUS_WAVE)
            # Спавним много монет
            for _ in range(20):
                bx = random.randint(50, SCREEN_WIDTH - 50)
                by = random.randint(50, SCREEN_HEIGHT - 200)
                bonus = Bonus(bx, by, bonus_type="coin")
                self.all_sprites.add(bonus)
                self.bonuses.add(bonus)
        
        if self.bonus_wave_active:
            self.bonus_wave_timer -= 1
            if self.bonus_wave_timer <= 0:
                self.bonus_wave_active = False
                self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "ВОЛНА ЗАВЕРШЕНА", COLOR_TEXT)
        
        # 🎯 Активация режима хаоса при комбо x30
        if self.player.combo >= 30 and not self.chaos_mode:
            self.chaos_mode = True
            self.chaos_timer = 900  # 15 секунд
            self.achievement_manager._unlock_achievement("chaos_mode", [])
            self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "РЕЖИМ ХАОСА!", COLOR_CHAOS)
        
        if not self.player:
            return
        for star in self.stars:
            star.update(2)
        self.particles = [p for p in self.particles if p.is_alive()]
        for p in self.particles:
            p.update()
        self.trails = [t for t in self.trails if t.is_alive()]
        for t in self.trails:
            t.update()
        self.dash_effects = [e for e in self.dash_effects if e.is_alive()]
        for e in self.dash_effects:
            e.update()
        self.floating_texts = [t for t in self.floating_texts if t.is_alive()]
        for t in self.floating_texts:
            t.update()
        self.all_sprites.update()
        
        if self.player.magnet:
            for bonus in self.bonuses:
                dx = self.player.rect.centerx - bonus.rect.centerx
                dy = self.player.rect.centery - bonus.rect.centery
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0:
                    bonus.rect.x += (dx / dist) * 5
                    bonus.rect.y += (dy / dist) * 5
        
        if not self.boss_active and self.enemies_killed < self.enemies_to_spawn:
            self.enemy_spawn_timer += 1
            diff = DIFFICULTIES.get(self.dm.data["difficulty"], DIFFICULTIES["normal"])
            spawn_rate = max(10, int(50 * diff["spawn_rate"]))
            if self.enemy_spawn_timer > spawn_rate:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
        
        if not self.boss_active and self.enemies_killed >= self.enemies_to_spawn:
            if self.dm.data["game_mode"] == "story":
                self.mission_complete = True
                self.state = "MISSION_COMPLETE"
                self.dm.save()
                return
            else:
                self.enemies_to_spawn += 20
                self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "НОВАЯ ВОЛНА!", COLOR_TEXT)
        
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            for enemy in hits:
                bullet.kill()
                # ✅ Мгновенное убийство
                if self.dm.data["cheat_instant_kill"]:
                    enemy.health = 1
                self.player.add_xp(enemy.score_value // 2)
                self.player.score += enemy.score_value
                self.player.add_combo()
                self.combo_timer = 180
                self.enemies_killed += 1
                
                # 🎯 Проверка достижений
                game_stats = {
                    "total_kills": self.dm.data.get("total_kills", 0) + 1,
                    "bosses_defeated": self.dm.data.get("bosses_defeated", 0),
                    "survival_time": self.survival_time,
                    "bonus_waves_found": self.bonus_waves_found,
                    "highest_score": self.dm.data.get("highest_score", 0),
                    "total_dashes": self.dm.data.get("total_dashes", 0),
                    "total_coins": self.dm.data.get("total_coins", 0),
                    "story_progress": self.dm.data.get("story_progress", 0)
                }
                unlocked = self.achievement_manager.check_and_unlock(self.player, game_stats)
                for ach in unlocked:
                    self.create_floating_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//3, f"🏆 {ach["name"]}!", COLOR_ACHIEVEMENT)
                
                self.create_explosion(enemy.rect.centerx, enemy.rect.centery, enemy.color)
                if random.random() < 0.12:
                    bonus = Bonus(enemy.rect.centerx, enemy.rect.centery)
                    self.all_sprites.add(bonus)
                    self.bonuses.add(bonus)
        
        for enemy in self.enemies:
            enemy_bullet = enemy.update(self.player)
            if enemy_bullet:
                self.all_sprites.add(enemy_bullet)
                self.enemy_bullets.add(enemy_bullet)
        
        if not self.player.invincible:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for enemy in hits:
                diff = DIFFICULTIES.get(self.dm.data["difficulty"], DIFFICULTIES["normal"])
                if self.player.take_damage(int(enemy.damage * diff["enemy_damage"])):
                    self.game_over()
            
            hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            for bullet in hits:
                diff = DIFFICULTIES.get(self.dm.data["difficulty"], DIFFICULTIES["normal"])
                if self.player.take_damage(int(15 * diff["enemy_damage"])):
                    self.game_over()
        
        hits = pygame.sprite.spritecollide(self.player, self.bonuses, True)
        for bonus in hits:
            if bonus.type == 'coin':
                self.player.coins += 5
            elif bonus.type == 'health':
                self.player.heal(25)
            elif bonus.type == 'shield':
                self.player.add_shield(50)
            elif bonus.type == 'powerup':
                self.player.weapon_level = min(3, self.player.weapon_level + 1)
            elif bonus.type == 'dash':
                self.player.dash_available = True
                self.player.dash_timer = 0
            elif bonus.type == 'crystal':
                self.player.crystals += 1
        
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.player.reset_combo()
        
        for enemy in self.enemies:
            enemy.update(self.player)

    def game_over(self):
        self.state = "GAMEOVER"
        self.audio.stop_music()
        if self.player.score > self.dm.data["highscore"]:
            self.dm.data["highscore"] = self.player.score
        self.dm.data["coins"] += self.player.coins
        self.dm.data["crystals"] += self.player.crystals
        self.dm.save()
        self.create_explosion(self.player.rect.centerx, self.player.rect.centery, COLOR_PLAYER)

    def draw_button(self, text, y_pos, width=None):
        w = width if width else SCREEN_WIDTH - 200
        rect = pygame.Rect((SCREEN_WIDTH - w)//2, y_pos, w, 60)
        pygame.draw.rect(self.screen, COLOR_BUTTON, rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PLAYER, rect, 3, border_radius=10)
        txt_surf = self.big_font.render(text, True, COLOR_TEXT)
        self.screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width())//2, rect.y + 10))
        return rect

    def draw_menu(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.title_font.render("NEON SPACE", True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        self.draw_button(self.get_lang("play"), 250)
        self.draw_button(self.get_lang("shop"), 340)
        self.draw_button(self.get_lang("settings"), 430)
        self.draw_button(self.get_lang("stats"), 520)
        self.draw_button(self.get_lang("exit"), 610)

    def draw_mode_select(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.big_font.render("ВЫБЕРИ РЕЖИМ", True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        self.draw_button(self.get_lang("infinite"), 320)
        self.draw_button(self.get_lang("story"), 420)
        self.draw_button(self.get_lang("back"), SCREEN_HEIGHT-100, width=100)

    def draw_difficulty_select(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.big_font.render("СЛОЖНОСТЬ", True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        for key, y in [("easy", 220), ("normal", 310), ("hard", 400), ("extreme", 490)]:
            diff = DIFFICULTIES[key]
            color = diff["color"] if self.dm.data["difficulty"] == key else (100, 100, 100)
            rect = pygame.Rect(100, y, SCREEN_WIDTH - 200, 60)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (255,255,255), rect, 2, border_radius=10)
            self.screen.blit(self.font.render(diff["name"], True, COLOR_TEXT), (rect.x + 20, rect.y + 20))
        self.draw_button(self.get_lang("back"), SCREEN_HEIGHT-100, width=100)

    def draw_shop(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.big_font.render("МАГАЗИН", True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        coins_text = self.font.render(f"💰 {self.dm.data['coins']}  💎 {self.dm.data['crystals']}", True, COLOR_COIN)
        self.screen.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 80))
        pygame.draw.rect(self.screen, COLOR_PLAYER if self.shop_page == "skins" else (100, 100, 100), (30, 100, 120, 40), border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PLAYER if self.shop_page == "colors" else (100, 100, 100), (160, 100, 120, 40), border_radius=10)
        self.screen.blit(self.font.render(self.get_lang("skins"), True, COLOR_TEXT), (45, 110))
        self.screen.blit(self.font.render(self.get_lang("colors"), True, COLOR_TEXT), (175, 110))
        if self.shop_page == "skins":
            skins = [("fighter", 0, "Истребитель"), ("circle", 100, "Сфера"), ("triangle", 250, "Треугольник"), ("diamond", 500, "Ромб"), ("stealth", 750, "Стелс")]
            for i, (key, cost, name) in enumerate(skins):
                y = 180 + i * 90
                is_unlocked = key in self.dm.data["unlocked_skins"]
                is_equipped = key == self.dm.data["current_skin"]
                color = COLOR_PLAYER if is_equipped else (100, 100, 100)
                rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y, 300, 75)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                pygame.draw.rect(self.screen, (255,255,255), rect, 2, border_radius=10)
                self.screen.blit(self.font.render(name, True, (255,255,255)), (rect.x + 20, rect.y + 10))
                status = "ВЫБРАНО" if is_equipped else ("КУПЛЕНО" if is_unlocked else f"{cost} 💰")
                status_color = (0, 255, 0) if is_equipped else ((255, 255, 0) if is_unlocked else (255, 200, 0))
                self.screen.blit(self.font.render(status, True, status_color), (rect.x + 20, rect.y + 40))
        elif self.shop_page == "colors":
            for i, (r, g, b, name) in enumerate(SHIP_COLORS):
                y = 180 + i * 75
                is_unlocked = i in self.dm.data["unlocked_colors"]
                is_equipped = i == self.dm.data["current_color"]
                cost = i * 100 if i > 0 else 0
                rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y, 300, 65)
                pygame.draw.rect(self.screen, (r, g, b), rect, border_radius=10)
                pygame.draw.rect(self.screen, (255,255,255) if is_equipped else (100, 100, 100), rect, 3, border_radius=10)
                self.screen.blit(self.font.render(name, True, (255,255,255)), (rect.x + 80, rect.y + 22))
                status = "✓" if is_equipped else ("" if is_unlocked else f"{cost}💰")
                self.screen.blit(self.font.render(status, True, (255,255,255)), (rect.x + 20, rect.y + 22))
        back_rect = pygame.Rect(20, SCREEN_HEIGHT - 80, 100, 50)
        pygame.draw.rect(self.screen, (200, 50, 50), back_rect, border_radius=10)
        self.screen.blit(self.font.render(self.get_lang("back"), True, (255,255,255)), (35, SCREEN_HEIGHT - 70))

    def draw_settings(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.big_font.render(self.get_lang("settings"), True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # ✅ Вкладки настроек
        main_color = COLOR_PLAYER if self.settings_page == "main" else (100, 100, 100)
        operator_color = COLOR_PLAYER if self.settings_page == "operator" else (100, 100, 100)
        pygame.draw.rect(self.screen, main_color, (30, 80, 170, 40), border_radius=10)
        pygame.draw.rect(self.screen, operator_color, (210, 80, 170, 40), border_radius=10)
        self.screen.blit(self.font.render("⚙️ Основные", True, COLOR_TEXT), (45, 90))
        self.screen.blit(self.font.render("🔧 Оператор", True, COLOR_TEXT), (225, 90))
        
        if self.settings_page == "main":
            vol_text = self.font.render(f"{self.get_lang('volume')}: {int(self.dm.data['volume']*100)}%", True, COLOR_TEXT)
            self.screen.blit(vol_text, (SCREEN_WIDTH//2 - vol_text.get_width()//2, 150))
            self.slider_rect = pygame.Rect(100, 180, SCREEN_WIDTH-200, 20)
            pygame.draw.rect(self.screen, COLOR_SLIDER_BG, self.slider_rect, border_radius=10)
            fill_width = int((SCREEN_WIDTH - 200) * self.dm.data["volume"])
            pygame.draw.rect(self.screen, COLOR_SLIDER_FILL, (100, 180, fill_width, 20), border_radius=10)
            pygame.draw.circle(self.screen, COLOR_PLAYER, (100 + fill_width, 190), 12)
            pygame.draw.rect(self.screen, COLOR_BUTTON, (100, 210, 80, 40), border_radius=10)
            pygame.draw.rect(self.screen, COLOR_BUTTON, (SCREEN_WIDTH-180, 210, 80, 40), border_radius=10)
            self.screen.blit(self.font.render("-", True, COLOR_TEXT), (125, 218))
            self.screen.blit(self.font.render("+", True, COLOR_TEXT), (SCREEN_WIDTH-155, 218))
            music_status = "🔊 ВКЛ" if self.dm.data["music_enabled"] else "🔇 ВЫКЛ"
            self.screen.blit(self.font.render(f"{self.get_lang('music')}: {music_status}", True, COLOR_TEXT), (SCREEN_WIDTH//2 - 100, 280))
            self.draw_button("🔁", 310, width=100)
            self.draw_button("🗑️ Сброс", 570, width=100)
        elif self.settings_page == "operator":
            # ✅ Режим оператора ВКЛ/ВЫКЛ
            operator_status = self.get_lang("enabled") if self.dm.data["operator_mode"] else self.get_lang("disabled")
            status_color = COLOR_HP if self.dm.data["operator_mode"] else (255, 50, 50)
            status_text = self.big_font.render(f"Режим оператора: {operator_status}", True, status_color)
            self.screen.blit(status_text, (SCREEN_WIDTH//2 - status_text.get_width()//2, 180))
            
            toggle_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, 240, 100, 50)
            toggle_color = COLOR_HP if self.dm.data["operator_mode"] else (100, 100, 100)
            pygame.draw.rect(self.screen, toggle_color, toggle_rect, border_radius=25)
            pygame.draw.circle(self.screen, COLOR_TEXT, (toggle_rect.x + 25 if self.dm.data["operator_mode"] else toggle_rect.x + 75, toggle_rect.y + 25), 20)
            
            info_text = self.font.render("Нажми для включения/выключения", True, COLOR_TEXT_DIM)
            self.screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, 310))
            
            warning_text = self.font.render("⚠️ Читы доступны только в игре!", True, (255, 150, 0))
            self.screen.blit(warning_text, (SCREEN_WIDTH//2 - warning_text.get_width()//2, 360))
        
        back_rect = pygame.Rect(20, SCREEN_HEIGHT - 80, 100, 50)
        pygame.draw.rect(self.screen, (200, 50, 50), back_rect, border_radius=10)
        self.screen.blit(self.font.render(self.get_lang("back"), True, (255,255,255)), (35, SCREEN_HEIGHT - 70))
        
        if self.reset_confirm:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(self.big_font.render("СБРОСИТЬ ВСЁ?", True, (255, 100, 100)), (SCREEN_WIDTH//2 - 150, 310))
            self.draw_button(self.get_lang("confirm"), 360, width=100)
            self.draw_button(self.get_lang("cancel"), 440, width=100)

    def draw_stats(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        title = self.big_font.render(self.get_lang("stats"), True, COLOR_PLAYER)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        stats = [f"Игр: {self.dm.data['games_played']}", f"Убито: {self.dm.data['total_kills']}", 
                 f"Монет: {self.dm.data['total_coins']}", f"Уровень: {self.dm.data['player_level']}",
                 f"Рекорд: {self.dm.data['highscore']}", f"Сюжет: {self.dm.data['story_progress']}/8"]
        for i, stat in enumerate(stats):
            self.screen.blit(self.font.render(stat, True, COLOR_TEXT), (SCREEN_WIDTH//2 - 100, 150 + i * 45))
        back_rect = pygame.Rect(20, SCREEN_HEIGHT - 80, 100, 50)
        pygame.draw.rect(self.screen, (200, 50, 50), back_rect, border_radius=10)
        self.screen.blit(self.font.render(self.get_lang("back"), True, (255,255,255)), (35, SCREEN_HEIGHT - 70))

    def draw_game(self):
        self.screen.fill(COLOR_BG)
        for star in self.stars:
            star.draw(self.screen)
        for trail in self.trails:
            trail.draw(self.screen)
        for effect in self.dash_effects:
            effect.draw(self.screen)
        self.all_sprites.draw(self.screen)
        if self.player:
            self.player.draw(self.screen)
        for p in self.particles:
            p.draw(self.screen)
        for t in self.floating_texts:
            t.draw(self.screen)
        if self.player:
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 20), border_radius=5)
            pygame.draw.rect(self.screen, COLOR_HP, (10, 10, 200 * (self.player.health / self.player.max_health), 20), border_radius=5)
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 35, 200, 8), border_radius=3)
            pygame.draw.rect(self.screen, COLOR_XP, (10, 35, 200 * (self.player.xp / self.player.xp_to_next), 8), border_radius=3)
            self.screen.blit(self.font.render(f"Lv.{self.player.level}", True, COLOR_XP), (10, 45))
            self.screen.blit(self.font.render(f"Score: {self.player.score}", True, COLOR_TEXT), (SCREEN_WIDTH - 150, 10))
            self.screen.blit(self.font.render(f"💰 {self.player.coins}", True, COLOR_COIN), (SCREEN_WIDTH - 150, 40))
            mode_text = self.font.render(f"Врагов: {self.enemies_killed}/{self.enemies_to_spawn}", True, COLOR_TEXT)
            self.screen.blit(mode_text, (10, 60))
            if self.boss_active:
                self.screen.blit(self.font.render("⚠ БОСС!", True, COLOR_BOSS), (SCREEN_WIDTH//2 - 50, 60))
        
        # ✅ Кнопка читов (только если оператор включен)
        if self.dm.data["operator_mode"]:
            pygame.draw.rect(self.screen, COLOR_CHEAT, self.cheat_button_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_TEXT, self.cheat_button_rect, 3, border_radius=10)
            cheat_text = self.font.render("🔧", True, COLOR_TEXT)
            self.screen.blit(cheat_text, (self.cheat_button_rect.x + 10, self.cheat_button_rect.y + 5))
        
        # ✅ Меню читов
        if self.cheats_open:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            title = self.big_font.render("ЧИТЫ", True, COLOR_CHEAT)
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
            
            cheats = [
                ("cheat_god_mode", "Бессмертие", 200),
                ("cheat_infinite_dash", "Бесконечный рывок", 280),
                ("cheat_instant_kill", "Мгновенное убийство", 360),
                ("cheat_max_weapon", "Макс. оружие", 440),
                ("add_coins", "+1000 монет", 520),
                ("add_crystals", "+100 кристаллов", 600)
            ]
            
            for cheat_key, cheat_name, y_pos in cheats:
                rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_pos, 300, 50)
                is_enabled = self.dm.data.get(cheat_key, False) if not cheat_key.startswith("add_") else False
                color = COLOR_HP if is_enabled else COLOR_BUTTON
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                pygame.draw.rect(self.screen, (255,255,255), rect, 2, border_radius=10)
                status = "✓" if is_enabled else "+"
                text = self.font.render(f"{status} {cheat_name}", True, COLOR_TEXT)
                self.screen.blit(text, (rect.x + 20, rect.y + 15))
            
            close_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 680, 200, 50)
            pygame.draw.rect(self.screen, (200, 50, 50), close_rect, border_radius=10)
            close_text = self.font.render("ЗАКРЫТЬ", True, COLOR_TEXT)
            self.screen.blit(close_text, (close_rect.x + 40, close_rect.y + 15))
        
        
        # 🎯 Отрисовка уведомлений о достижениях
        self.achievement_manager.draw_notifications(self.screen)
        
        # 🔥 Отрисовка комбо
        if self.player and self.player.combo > 5:
            combo_font = pygame.font.SysFont("Arial", 32, bold=True)
            combo_color = COLOR_COMBO
            if self.chaos_mode:
                combo_color = COLOR_CHAOS
            combo_text = combo_font.render(f"COMBO x{self.player.combo}!", True, combo_color)
            self.screen.blit(combo_text, (SCREEN_WIDTH//2 - combo_text.get_width()//2, 100))
        
        # 🌀 Отрисовка режима хаоса
        if self.chaos_mode:
            chaos_font = pygame.font.SysFont("Arial", 24, bold=True)
            chaos_text = chaos_font.render(f"ХАОС: {self.chaos_timer//60}с", True, COLOR_CHAOS)
            self.screen.blit(chaos_text, (SCREEN_WIDTH//2 - chaos_text.get_width()//2, 140))
        
        # 💎 Отрисовка бонусной волны
        if self.bonus_wave_active:
            bonus_font = pygame.font.SysFont("Arial", 24, bold=True)
            bonus_text = bonus_font.render(f"БОНУС: {self.bonus_wave_timer//60}с", True, COLOR_BONUS_WAVE)
            self.screen.blit(bonus_text, (SCREEN_WIDTH//2 - bonus_text.get_width()//2, 170))
        
        pygame.draw.rect(self.screen, (100, 100, 100), (SCREEN_WIDTH - 50, 10, 35, 35), border_radius=5)

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.draw_button("ПРОДОЛЖИТЬ", 380)
        self.draw_button("МЕНЮ", 480)

    def draw_gameover(self):
        self.screen.fill((30, 0, 0))
        for star in self.stars:
            star.draw(self.screen)
        self.screen.blit(self.big_font.render("GAME OVER", True, (255, 0, 0)), (SCREEN_WIDTH//2 - 150, 150))
        self.screen.blit(self.font.render(f"Score: {self.player.score}", True, COLOR_TEXT), (SCREEN_WIDTH//2 - 80, 250))
        self.draw_button("ЗАНОВО", 380)
        self.draw_button("МЕНЮ", 480)

    def draw_mission_complete(self):
        self.screen.fill((0, 30, 0))
        for star in self.stars:
            star.draw(self.screen)
        self.screen.blit(self.big_font.render("МИССИЯ ВЫПОЛНЕНА!", True, (0, 255, 0)), (SCREEN_WIDTH//2 - 200, 150))
        if self.dm.data["game_mode"] == "story":
            chapter = STORY_CHAPTERS[min(self.dm.data["story_progress"], len(STORY_CHAPTERS)-1)]
            self.screen.blit(self.font.render(f"Награда: {chapter['reward']} 💰", True, COLOR_COIN), (SCREEN_WIDTH//2 - 100, 250))
        self.draw_button("МЕНЮ", 480)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_input()
            if self.cutscene_active:
                self.cutscene.update()
                self.screen.fill(COLOR_BG)
                for star in self.stars:
                    star.draw(self.screen)
                if self.cutscene and not self.cutscene.is_finished():
                    self.cutscene.draw(self.screen)
                elif self.cutscene and self.cutscene.is_finished():
                    self.cutscene_active = False
                    self.state = "GAME"
            elif self.state == "GAME":
                self.update_game()
                self.draw_game()
            elif self.state == "MENU":
                self.draw_menu()
            elif self.state == "MODE_SELECT":
                self.draw_mode_select()
            elif self.state == "DIFFICULTY_SELECT":
                self.draw_difficulty_select()
            elif self.state == "SHOP":
                self.draw_shop()
            elif self.state == "SETTINGS":
                self.draw_settings()
            elif self.state == "STATS":
                self.draw_stats()
            elif self.state == "PAUSE":
                self.draw_game()
                self.draw_pause()
            elif self.state == "GAMEOVER":
                self.draw_gameover()
            elif self.state == "MISSION_COMPLETE":
                self.draw_mission_complete()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

# ============================================
# ЗАПУСК
# ============================================

if __name__ == "__main__":
    game = Game()
    game.run()