import pygame
import sys
import random
import math
from pygame import mixer

pygame.init()

# Размер игрового пространства
scr_width = 1000
scr_height = 700

screen = pygame.display.set_mode((scr_width, scr_height))

# Инициализация заднего фона
background = pygame.image.load('./data/background.png')

# Музыка
mixer.music.load('./data/background.wav')
mixer.music.play(-1)

# Иконки
pygame.display.set_caption("./data/Cosmic Attack")
icon = pygame.image.load('./data/icon.png')
pygame.display.set_icon(icon)

# Инициализация игрока
player_img = pygame.image.load('./data/spaceship.png')
player_x = 470
player_y = 600
player_xchange = 10

enemy_img = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
enemy_num = 10

for i in range(enemy_num):
    enemy_img.append(pygame.image.load('./data/ufo.png'))
    enemy_x.append(random.randint(10, 926))
    enemy_y.append(random.randint(50, 400))
    enemy_xchange.append(6)
    enemy_ychange.append(35)

# Инициализация снарядов, которыми стреляет игрок
bullet_img = pygame.image.load('./data/bullet.png')
bullet_x = 470
bullet_y = 600
bullet_ychange = 20
bullet_state = 'ready'

# Инициализация бомб
bomb_img = pygame.image.load('./data/bomb.png')
bomb_x = random.randint(10, 958)
bomb_y = 50
bomb_ychange = 12
bomb_state = 'active'

# Collision
collision_img = pygame.image.load('./data/explosion.png')

# Инициализация шрифтов и счётчиков
scr_val = 0
font1 = pygame.font.Font('./data/JetBrainsMono.ttf', 32)
font3 = pygame.font.Font('./data/JetBrainsMono.ttf', 24)
font2 = pygame.font.Font('./data/JetBrainsMono.ttf', 64)
value = 0
count = 0


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x+15, y+10))


def bomb(x, y):
    screen.blit(bomb_img, (x, y))


def collision(x1, y1, x2, y2):
    x_diff = x2 - x1
    y_diff = y2 - y1
    distance = math.sqrt((math.pow(x_diff, 2)) + (math.pow(y_diff, 2)))
    if distance <= 50:
        screen.blit(collision_img, (x1, y1))
        return True
    else:
        return False


def display():
    score = font1.render('СЧЁТ : ' + str(scr_val), True, (255, 200, 51))
    screen.blit(score, (10, 10))
    instructions = font3.render(
        'Нажимай ← или → для движения, ↑ для выстрела.', True, (255, 200, 51))
    screen.blit(instructions, (300, 35))


def game_over():
    over_text = font2.render('Конец игры !', True, (255, 200, 51))
    screen.blit(over_text, (325, 275))
    global value

    if value == 2:
        msg_text2 = font1.render('ВЫ УБИТЫ БОМБОЙ !', True, (255, 200, 51))
        screen.blit(msg_text2, (400, 350))


# Игровой цикл
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ESC выход
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            # Движение влево
            if event.key == pygame.K_LEFT:
                player_xchange = -10
            # Движение вправо
            if event.key == pygame.K_RIGHT:
                player_xchange = 10
            # Огонь с использованием пробела или клавиши вверх
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('./data/bullet.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_xchange = 0

    # PlayerBoundary
    player_x += player_xchange
    if player_x <= 10:
        player_x = 10
    elif player_x >= 926:
        player_x = 926

    # Расчёт границ в цикле
    for i in range(enemy_num):
        enemy_x[i] += enemy_xchange[i]
        if enemy_x[i] <= 10:
            enemy_xchange[i] = 6
            enemy_y[i] += enemy_ychange[i]
        elif enemy_x[i] >= 926:
            enemy_xchange[i] = -6
            enemy_y[i] += enemy_ychange[i]

        # Исправление коллизий
        col = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if col:
            explosion_sound = mixer.Sound('./data/explosion.wav')
            explosion_sound.play()
            bullet_y = 600
            bullet_state = 'ready'
            scr_val += 1
            enemy_x[i] = random.randint(10, 926)
            enemy_y[i] = random.randint(50, 500)

        enemy(enemy_x[i], enemy_y[i], i)

    # Движение снаряда
    if bullet_y <= 0:
        bullet_y = 600
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet(bullet_x, bullet_y)
        bullet_y -= bullet_ychange

    # Конец игры, когда бомба попадает в игрока
    x_diff2 = bomb_x - player_x
    y_diff2 = bomb_y - player_y
    distance2 = math.sqrt((math.pow(x_diff2, 2)) + (math.pow(y_diff2, 2)))
    if distance2 <= 50:
        bomb_y = 2000
    if bomb_y >= 2000:
        bomb_state = 'passive'
        value = 2
        bomb_y == 2000
        for j in range(enemy_num):
            enemy_y[j] = 2000
        screen.blit(collision_img, (player_x, player_y))
        player_y = -2000
        if count == 0:
            explosion_sound = mixer.Sound('./data/explosion.wav')
            explosion_sound.play()
            over_sound = mixer.Sound('./data/gameover.wav')
            over_sound.play()
            count += 1
        game_over()

    # Падение бомб
    bomb(bomb_x, bomb_y)
    bomb_y += bomb_ychange
    if bomb_y >= 600:
        if bomb_state == 'active':
            bomb_x = random.randint(10, 958)
            bomb_y = 50

    player(player_x, player_y)

    display()

    pygame.display.update()
