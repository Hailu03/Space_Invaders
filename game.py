from pygame import mixer
import pygame
import math
import random

# initialize the game
pygame.init()

# FPS
FPS = 60
fpsclock = pygame.time.Clock()

# music and sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# create the screen
screen_length = 800
screen_width = 600
screen = pygame.display.set_mode((screen_length,screen_width))

# title and icon
title = pygame.display.set_caption("space invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# change background
background = pygame.image.load("background.png")

# add spaceship
playerImg = pygame.image.load("space-invaders.png")
playerX = 380
playerY = 500
playerX_change =0
playerY_change = 0

def player(x,y):
    screen.blit(playerImg,(x,y))
    
# add enemy to the game
# add more enemies to the game
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(20)

    def enemy(x,y,i):
        screen.blit(enemyImg[i],(x,y))

# create a bullet to shoot alien
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = -5

bullet_state = "ready"

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y))

# check collision
def isCollison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (150,150,255))
    screen.blit(score,(x,y))

# game over
over_font = pygame.font.Font("freesansbold.ttf",100)

def game_over_text():
    over_text = font.render("GAME OVER" ,True, (150,150,255))
    screen.blit(over_text,(310,250))

# game loop
running = True
while running:

    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # spaceship movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    player(playerX,playerY)

    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 390:
        playerY = 390
    elif playerY >= 530:
        playerY = 530

    for i in range(number_of_enemies):
        if enemyY[i] > 200:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
                

        enemy(enemyX[i],enemyY[i],i)
        if enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i] 

        collision = isCollison(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_state = "ready"
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
            score_value +=1

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY
    if bullet_state == "fire":
        bulletY += bulletY_change
        bullet(bulletX,bulletY)

    fpsclock.tick()
    show_score(textX,textY)
    pygame.display.update()