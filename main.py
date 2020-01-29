import pygame
import random
import math
from pygame import mixer

#iniciando o pygame
pygame.init()
#iniciando tela                     X, Y
screen = pygame.display.set_mode((800, 600))
#setando background
background = pygame.image.load('backgroung_cats_astronauts.jpg')
#setando as musicas
lista_musicas = []
lista_musicas.append('background.wav')
lista_musicas.append('lofi-trap-melody_C_minor.wav')
lista_musicas.append('lofi-melody_84bpm_C_major.wav')
lista_musicas.append('muffled-lofi-guitar_80bpm.wav')

faixa = random.randint(0, 3)
mixer.music.load(lista_musicas[faixa])
mixer.music.play(-1)
#setando nome do jogo e icone(nao aparce no linux)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)
#jogador
player_Velocity = 5
playerImg = pygame.image.load("spaceship.png")
playerX = 373
playerY = 480
playerXChange = 0
#o jogador nao altera na vertical
#playerYChange = 0

alien_Velocity = 4
alienImg = []
alienX = []
alienY = []
alienXChange = []
alienYChange = []
numberOfEnemys = 3
for i in range(numberOfEnemys):
    alienImg.append(pygame.image.load("ufo.png"))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienXChange.append(alien_Velocity)
    alienYChange.append(40)
#laser
# ready you can see it on screen
# Fire the bullet is moving
laserImg = pygame.image.load('laser.png')
laserImg = pygame.transform.rotate(laserImg, 180)
laserX = 0
laserY = 480
laserXChange = 0
laserYChange = 10
laserState = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render('Score : '+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player (x,y):
    screen.blit(playerImg, (x, y))

def alien (x,y,i):
    screen.blit(alienImg[i], (x, y))

def fireLaser(x,y):
    global laserState
    laserState = 'fire'
    screen.blit(laserImg, (x+16, y+10))

def isColission(enemyX,enemyY,projectileX,projectileY):
    distance = math.sqrt(math.pow(enemyX-projectileX,2)+math.pow(enemyY-projectileY,2))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:             
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN):
            #pressed
            if(event.key == pygame.K_LEFT):
                playerXChange = -player_Velocity
            if(event.key == pygame.K_RIGHT):
                playerXChange = player_Velocity
            if(event.key == pygame.K_SPACE):
                if laserState is 'ready':
                    laserSound = mixer.Sound('laser.wav')
                    laserSound.play()

                    laserX = playerX
                    fireLaser(laserX, laserY)

        if(event.type == pygame.KEYUP):
            #realeased
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerXChange = 0


    playerX += playerXChange
    if(playerX <= 0):
        playerX = 0
    elif(playerX >= 736):
        playerX = 736
    #
    for i in range(numberOfEnemys):

        if alienY[i] > 440:
            for j in range(numberOfEnemys):
                del(alienY[j])
            game_over_text()
            break


        alienX[i] += alienXChange[i]
        if (alienX[i] <= 0):
            alienXChange[i] = alien_Velocity
            alienY[i] += alienYChange[i]
        if (alienX[i] >= 736):

            alienXChange[i] = -alien_Velocity
            alienY[i] += alienYChange[i]

        collisision = isColission(alienX[i], alienY[i], laserX, laserY)
        if collisision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            laserY = 480
            laserState = 'ready'
            score_value += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i )

    if laserY <= 0:
        laserY = 480
        laserState = 'ready'
    if laserState is 'fire':
        fireLaser(laserX,laserY)
        laserY -=laserYChange

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

