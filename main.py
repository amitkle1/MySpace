import pygame
import random
import math

from pygame import mixer

# initalize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('fanatics.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("MySpace")
icon = pygame.image.load('transport.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('gaming.png')
playerX = 370
playerY = 480
playerXChange = 0
playerYChange = 0
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(1)
    enemyYChange.append(40)

# bullet
bulletImg = pygame.image.load('weapons.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 34)
textX = 500
textY = 10
victoryX = 300
victoryY = 100


def victory():
    victoryFont = pygame.font.Font('freesansbold.ttf', 50)
    victoryText = victoryFont.render("VICTORY ! ", True, (255, 255, 0))
    victoryFon = pygame.font.Font('freesansbold.ttf', 50)
    victoryTex = victoryFont.render("Thanks for playing!", True, (0, 0, 0))
    screen.blit(victoryText, (victoryX, victoryY + 100))
    screen.blit(victoryTex, (victoryX - 140, victoryY + 200))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distace = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distace < 27:
        return True
    else:
        return False


# gameloop
running = True
while running:
    # rgb
    screen.fill((255, 255, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                playerXChange = 5
                # if event.key == pygame.K_UP:
                #     playerYChange = -5
                # if event.key == pygame.K_DOWN:
                #     playerYChange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerXChange = 0
                playerYChange = 0

    playerX += playerXChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if score_value == 5:
            mixer.music.stop()
            victory()
            break
        enemyX[i] += enemyXChange[i]
        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 2.5
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyXChange[i] = -2.5
            enemyY[i] += enemyYChange[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    playerY += playerYChange
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
