import sys
import os
import random

import pygame
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

# global constants
FPS = 6
BOARD_WIDTH = 800
BOARD_HEIGHT = 800
FIELD_SIDE = 40
NUM_OF_FIELDS = int(BOARD_WIDTH / FIELD_SIDE)

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVYBLUE = (60, 60, 100)
AQUA = (0, 255, 255)
LIMEGREEN = (50, 205, 50)
YELLOWGREEN = (154, 205, 50)
MAROON = (128, 0, 0)

# global variables
playerHead = [5, 15]
playerTail = [(2, 15), (3, 15), (4, 15)]
mainBoard = []
score = 0
direction = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, score, food, direction, fontObj
    pygame.init()
    pygame.display.set_caption('Snejk 2D')
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    fontObj = pygame.font.Font('freesansbold.ttf', 32)

    createBoard()
    drawBoard()
    food = randomFood()

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and direction != 'down':
                    direction = 'up'
                    break
                elif event.key == K_DOWN and direction != 'up':
                    direction = 'down'
                    break
                elif event.key == K_RIGHT and direction != 'left':
                    direction = 'right'
                    break
                elif event.key == K_LEFT and direction != 'right':
                    direction = 'left'
                    break
            elif event.type == KEYUP:
                if event.key == K_p:
                    pauseGame()
                elif event.key == K_r:
                    restartGame()

        tailEnd = movePlayer(direction)
        if (detectCollision()):
            endGame()
            restartGame()
        if (isEatingFood()):
            increaseScoreAndLength(tailEnd)
            food = randomFood()
        drawBoard()
        drawPlayer()
        drawFood()
        displayScore()

        # redraw screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def createBoard():
    for x in range(NUM_OF_FIELDS):
        column = []
        for y in range(NUM_OF_FIELDS):
            column.append(pygame.Rect(FIELD_SIDE * x, FIELD_SIDE * y, FIELD_SIDE, FIELD_SIDE))
        mainBoard.append(column)


def drawBoard():
    for x in range(1, NUM_OF_FIELDS - 1):
        for y in range(1, NUM_OF_FIELDS - 1):
            pygame.draw.rect(DISPLAYSURF, AQUA, mainBoard[x][y], 0)

    for x in range(NUM_OF_FIELDS): pygame.draw.rect(DISPLAYSURF, NAVYBLUE, mainBoard[x][0], 0)
    for x in range(NUM_OF_FIELDS): pygame.draw.rect(DISPLAYSURF, NAVYBLUE, mainBoard[x][NUM_OF_FIELDS - 1], 0)
    for y in range(NUM_OF_FIELDS): pygame.draw.rect(DISPLAYSURF, NAVYBLUE, mainBoard[0][y], 0)
    for y in range(NUM_OF_FIELDS): pygame.draw.rect(DISPLAYSURF, NAVYBLUE, mainBoard[NUM_OF_FIELDS - 1][y], 0)


def drawPlayer():
    # draw head
    pygame.draw.rect(DISPLAYSURF, YELLOWGREEN, mainBoard[playerHead[0]][playerHead[1]])

    # draw rest of the snake
    for field in playerTail:
        pygame.draw.rect(DISPLAYSURF, LIMEGREEN, mainBoard[field[0]][field[1]])


def drawFood():
    pygame.draw.rect(DISPLAYSURF, MAROON, mainBoard[food[0]][food[1]], 0)


def displayScore():
    textSurfaceObj = fontObj.render("Score: " + str(score), True, WHITE, NAVYBLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (FIELD_SIDE * 2, FIELD_SIDE / 2)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def randomFood():
    while True:
        x = random.randrange(NUM_OF_FIELDS)
        y = random.randrange(NUM_OF_FIELDS)
        if x != 0 and y != 0 and x != NUM_OF_FIELDS - 1 and y != NUM_OF_FIELDS - 1 \
                and x != playerHead[0] and y != playerHead[1] and (x, y) not in playerTail:
            return (x, y)


def isEatingFood():
    if food[0] == playerHead[0] and food[1] == playerHead[1]:
        return True


def increaseScoreAndLength(tailEnd):
    global score
    score += 1
    playerTail.insert(0, tailEnd)


def pauseGame():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_p:
                return
        FPSCLOCK.tick(FPS)


def endGame():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_r:
                return
        FPSCLOCK.tick(FPS)


def restartGame():
    global playerHead, playerTail, score, direction, food
    playerHead = [5, 15]
    playerTail = [(2, 15), (3, 15), (4, 15)]
    score = 0
    direction = 'right'
    food = randomFood()


def detectCollision():
    collision = False
    if playerHead[0] == 0:
        for y in range(NUM_OF_FIELDS):
            if playerHead[1] == y:
                collision = True
                break
    elif playerHead[0] == NUM_OF_FIELDS - 1:
        for y in range(NUM_OF_FIELDS):
            if playerHead[1] == y:
                collision = True
                break
    elif playerHead[1] == 0:
        for x in range(NUM_OF_FIELDS):
            if playerHead[0] == x:
                collision = True
                break
    elif playerHead[1] == NUM_OF_FIELDS - 1:
        for x in range(NUM_OF_FIELDS):
            if playerHead[0] == x:
                collision = True
                break
    else:
        for tail in playerTail:
            if playerHead[0] == tail[0] and playerHead[1] == tail[1]:
                collision = True
                break

    return collision


def movePlayer(direction):
    if direction == 'right':
        playerTail.append((playerHead[0], playerHead[1]))
        playerHead[0] += 1
        return playerTail.pop(0)
    elif direction == 'left':
        playerTail.append((playerHead[0], playerHead[1]))
        playerHead[0] -= 1
        return playerTail.pop(0)
    elif direction == 'up':
        playerTail.append((playerHead[0], playerHead[1]))
        playerHead[1] -= 1
        return playerTail.pop(0)
    elif direction == 'down':
        playerTail.append((playerHead[0], playerHead[1]))
        playerHead[1] += 1
        return playerTail.pop(0)


if __name__ == '__main__':
    main()
