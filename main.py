import pygame
import random

pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TIME_LIMIT = 60
TEXT_COLOR = (0, 0, 0)  # Цвет текста

# Параметры цели
TARGET_WIDTH = 80
TARGET_HEIGHT = 80
target_speed = 50  # Начальная скорость
CHANGE_DIRECTION_PROBABILITY = 0.01
TARGET_SPEED_RANGE = (-3, 3)  # Диапазон для случайной скорости

# Загрузка ресурсов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Тир")
icon = pygame.image.load("image/3548755.png")
pygame.display.set_icon(icon)
target_img = pygame.image.load("image/target.png")
hit_sound = pygame.mixer.Sound("image/hit_sound.wav")
miss_sound = pygame.mixer.Sound("image/miss_sound.wav")
font = pygame.font.Font(None, 36)

def get_random_speed():
    """Возвращает случайные значения скорости в заданном диапазоне."""
    return random.randint(*TARGET_SPEED_RANGE), random.randint(*TARGET_SPEED_RANGE)


# Инициализация игры
clock = pygame.time.Clock()
target_x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
target_y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)
target_speed_x, target_speed_y = get_random_speed()
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
shots_fired = 0
targets_hit = 0
start_time = pygame.time.get_ticks()
game_over = False

running = True
while running:
    screen.fill(color)

    # Проверка окончания времени
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time >= TIME_LIMIT:
        game_over = True
        target_speed_x = 0
        target_speed_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            shots_fired += 1
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + TARGET_WIDTH and target_y < mouse_y < target_y + TARGET_HEIGHT:
                targets_hit += 1
                hit_sound.play()
                target_x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
                target_y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)
                target_speed_x, target_speed_y = get_random_speed()
                target_speed += 1  # Увеличиваем скорость при попадании
            else:
                miss_sound.play()

    # Движение цели
    if not game_over:
        time_delta = clock.tick(FPS) / 1000.0
        target_x += target_speed_x * time_delta * target_speed
        target_y += target_speed_y * time_delta * target_speed

    # Проверка выхода за границы экрана и изменение направления
    if target_x < 0 or target_x > SCREEN_WIDTH - TARGET_WIDTH:
        target_speed_x *= -1
    if target_y < 0 or target_y > SCREEN_HEIGHT - TARGET_HEIGHT:
        target_speed_y *= -1

    # Случайное изменение направления
    if random.random() < CHANGE_DIRECTION_PROBABILITY and not game_over:
        target_speed_x, target_speed_y = get_random_speed()

    # Отрисовка цели
    screen.blit(target_img, (target_x, target_y))

    # Отображение текста
    shots_text = font.render("Выстрелы: " + str(shots_fired), True, TEXT_COLOR)
    hits_text = font.render("Попадания: " + str(targets_hit), True, TEXT_COLOR)
    screen.blit(shots_text, (10, 10))
    screen.blit(hits_text, (10, 40))

    # Отображение времени
    remaining_time = max(0, TIME_LIMIT - int(elapsed_time))
    time_text = font.render("Время: " + str(remaining_time), True, TEXT_COLOR)
    screen.blit(time_text, (10, 70))

    # Отображение итогового результата
    if game_over:
        game_over_text = font.render("Игра окончена!", True, TEXT_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pygame.display.update()

pygame.quit()