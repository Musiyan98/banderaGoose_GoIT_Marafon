import pygame
import random
import os

from pygame.constants import QUIT, K_DOWN, K_RIGHT, K_LEFT, K_UP, K_SPACE, KSCAN_KP_ENTER

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 30)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()

player_moove_down = [0, 1]
player_moove_left = [-1, 0]
player_moove_up = [0, -1]
player_moove_right = [1, 0]

def createEnemy():
    enemy_size = (50, 10)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    # enemy.fill(COLOR_RED)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, WIDTH), enemy.get_width(), enemy.get_height())
    enemy_moove = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_moove] 

def createBuf():
    buf_size = (30, 30)
    buf = pygame.image.load('bonus.png').convert_alpha()
    # buf.fill(COLOR_GREEN)
    buf_rect = pygame.Rect(random.randint(0, WIDTH), 0, buf.get_width(), buf.get_height())
    buf_moove = [0, random.randint(1, 2)]
    return [buf, buf_rect, buf_moove] 

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 3000)

CREATE_BUF = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BUF, 5000)

FLYBANDERA = pygame.USEREVENT + 3
pygame.time.set_timer(FLYBANDERA, 300)

bufs = []
enemies = []
playing = True
score = 0
image_index = 0

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(createEnemy())
        if event.type == CREATE_BUF:
            bufs.append(createBuf())
        if event.type == FLYBANDERA:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
            

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 <= -bg.get_width():
        bg_x1 = (bg.get_width() - 7)

    if bg_x2 <= -bg.get_width():
        bg_x2 = (bg.get_width() - 7)

    main_display.fill(COLOR_BLACK)
    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()


    if keys[K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_moove_down)

    if keys[K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_moove_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_moove_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_moove_left)

    if keys[K_SPACE]:
        print("space")

    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False


    for buf in bufs:
        buf[1] = buf[1].move(buf[2])
        main_display.blit(buf[0], buf[1])

        if player_rect.colliderect(buf[1]):
            bufs.pop(bufs.index(buf))
            score += 1

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for buf in bufs:
        if buf[1].bottom > HEIGHT:
            bufs.pop(bufs.index(buf))


