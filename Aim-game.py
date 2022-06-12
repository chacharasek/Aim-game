# Aim trainer

import math
import pygame
import random
import sys
import time
from pygame.locals import *

# check if there are any errors in the code
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initialising errors".format(check_errors[1]))
    print("Exiting...")
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialised!")
    print("You can play without any problems!")

# Play Surface
width = 750
height = 750
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Aim trainer')

# font
FONT = pygame.font.SysFont(None, 48)

# game speed controller
tick_rate = 30
fpsController = pygame.time.Clock()

# Game state
tickCounter = 0
spawnTargetTimer = 30
aimPoints = []
lives = 3
score = 0
widthMax = 40

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


def gameOver():
    # font and size
    myFont = pygame.font.SysFont('monaco', 72)
    # text, antialias, collor
    gameOverSurface = myFont.render('Game Over!', True, "white")
    gameOverRectangle = gameOverSurface.get_rect()
    gameOverRectangle.midtop = (width / 2, height / 20)
    playSurface.blit(gameOverSurface, gameOverRectangle)
    showScore(0)
    pygame.display.flip()
    # wait 3 seconds
    time.sleep(3)
    # close window
    pygame.quit()
    sys.exit()


def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Score: {0}'.format(score), True, "white")
    scoreRectangle = scoreSurface.get_rect()
    if choice == 1:
        scoreRectangle.midtop = (width / 10, height / 20)
    else:
        scoreRectangle.midtop = (width / 2, height / 4)
    playSurface.blit(scoreSurface, scoreRectangle)


def showMisses():
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Lives: {0}'.format(lives), True, "white")
    scoreRectangle = scoreSurface.get_rect()
    scoreRectangle.midtop = (width - (width / 7), height / 20)
    playSurface.blit(scoreSurface, scoreRectangle)


def distance(A, B):
    # clicked distance from center of the point
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)


def drawText(text, surface, x, y, font=FONT, color="red"):
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObject, textRect)


def populateConfig(difficulty):
    config = {}
    if difficulty == "easy":
        difficultyFile = open("easy.txt", "r")
    elif difficulty == "medium":
        difficultyFile = open("medium.txt", "r")
    elif difficulty == "hard":
        difficultyFile = open("hard.txt", "r")
    for line in difficultyFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    difficultyFile.close()
    return config


def quit():
    pygame.quit()
    sys.exit()


class InputBox:

    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.text = ""
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    global username
                    username = self.text
                    self.text = ""
                    global done
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, playSurface):
        # Blit the text.
        playSurface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(playSurface, self.color, self.rect, 2)


def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(300, 300, 140, 48, "enter your username")
    input_boxes = [input_box1]
    global done
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        playSurface.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(playSurface)

        pygame.display.flip()
        clock.tick(10)


def playAgain():
    playSurface = pygame.display.set_mode((750, 750))
    # Settings
    option = 0
    timer = 0
    color = "blue"
    while True:
        playSurface.fill("black")
        optionRects = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100), pygame.Rect(505, 450, 240, 100)]
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            if event.type == MOUSEBUTTONDOWN:
                if optionRects[0].collidepoint(pygame.mouse.get_pos()):
                    option = "Yes"
                if optionRects[1].collidepoint(pygame.mouse.get_pos()):
                    quit()
                if optionRects[2].collidepoint(pygame.mouse.get_pos()):
                    quit()
        for rect in optionRects:
            pygame.draw.rect(playSurface, "red", rect)
        drawText("play again", playSurface, 10, 150, pygame.font.SysFont(None, 112), color)
        drawText("Yes", playSurface, 83, 485, FONT, "black")
        drawText("No", playSurface, 312, 485, FONT, "black")
        drawText("Quit", playSurface, 580, 485, FONT, "black")
        fpsController.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = "blue"
        elif timer % 50 == 0:
            color = "red"
        pygame.display.update()
        if option != 0:
            break
    if option == "Yes":
        menu()

    return option


def saveScore():
    playSurface = pygame.display.set_mode((750, 750))
    if maxUserScore() > score or maxBestScore() > score:
        option1 = "green"
        option2 = "red"
    else:
        option1 = "red"
        option2 = "green"
    # Settings
    save = 0
    timer = 0
    color = "blue"
    while True:
        playSurface.fill("black")
        saveRects = []
        saveRects1 = []
        saveRects2 = []
        saveRects1.append(pygame.Rect(5, 450, 240, 100))
        saveRects2.append(pygame.Rect(255, 450, 240, 100))
        saveRects.append(pygame.Rect(505, 450, 240, 100))
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            if event.type == MOUSEBUTTONDOWN:
                if saveRects1[0].collidepoint(pygame.mouse.get_pos()):
                    save = "Yes"
                if saveRects2[0].collidepoint(pygame.mouse.get_pos()):
                    save = "No"
                if saveRects[0].collidepoint(pygame.mouse.get_pos()):
                    quit()
        for rect in saveRects:
            pygame.draw.rect(playSurface, "red", rect)
        for rect in saveRects1:
            pygame.draw.rect(playSurface, option2, rect)
        for rect in saveRects2:
            pygame.draw.rect(playSurface, option1, rect)
        drawText("Save score", playSurface, 90, 150, pygame.font.SysFont(None, 112), color)
        drawText("Yes", playSurface, 83, 485, FONT, "black")
        drawText("No", playSurface, 312, 485, FONT, "black")
        drawText("Quit", playSurface, 580, 485, FONT, "black")
        fpsController.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = "blue"
        elif timer % 50 == 0:
            color = "red"
        pygame.display.update()
        if save != 0:
            break

    return save


def maxUserScore():
    config = {}
    leaderFile = open(r"klikacka/leaderboard.ini", 'r')

    for line in leaderFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    leaderFile.close()

    PB = config.get(username)
    if not isinstance(PB, int):
        PB = 0
    return int(PB)


def maxBestScore():
    config = {}
    leaderFile = open(r"klikacka/leaderboard.ini", 'r')

    for line in leaderFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    leaderFile.close()

    maxScore = config.get("maxScore")
    if not isinstance(maxScore, int):
        maxScore = 0
    return int(maxScore)


def menu():
    # Menu
    setting = 0
    timer = 0
    color = "blue"
    while True:
        playSurface.fill("black")
        settingReacts = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100),
                         pygame.Rect(505, 450, 240, 100)]
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            if event.type == MOUSEBUTTONDOWN:
                if settingReacts[0].collidepoint(pygame.mouse.get_pos()):
                    setting = "Play"
                if settingReacts[1].collidepoint(pygame.mouse.get_pos()):
                    setting = "Settings"
                if settingReacts[2].collidepoint(pygame.mouse.get_pos()):
                    setting = "Quit"
        for rect in settingReacts:
            pygame.draw.rect(playSurface, "red", rect)
        drawText("veri gut gejm", playSurface, 150, 150, pygame.font.SysFont(None, 112), color)
        drawText("Play", playSurface, 83, 485, FONT, "black")
        drawText("Settings", playSurface, 312, 485, FONT, "black")
        drawText("Quit", playSurface, 580, 485, FONT, "black")
        fpsController.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = "blue"
        elif timer % 50 == 0:
            color = "red"
        pygame.display.update()
        if setting != 0:
            break

    if setting == "Quit":
        quit()
    elif setting == "Settings":
        # Settings
        fgh = 0
        timer = 0
        color = "blue"
        while True:
            playSurface.fill("black")
            fghRects = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100), pygame.Rect(505, 450, 240, 100)]
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                if event.type == MOUSEBUTTONDOWN:
                    if fghRects[0].collidepoint(pygame.mouse.get_pos()):
                        quit()
                    if fghRects[1].collidepoint(pygame.mouse.get_pos()):
                        quit()
                    if fghRects[2].collidepoint(pygame.mouse.get_pos()):
                        fgh = "menu"
            for rect in fghRects:
                pygame.draw.rect(playSurface, "red", rect)
            drawText("Settings", playSurface, 90, 150, pygame.font.SysFont(None, 112), color)
            drawText("Neviem", playSurface, 83, 485, FONT, "black")
            drawText("Neviem", playSurface, 312, 485, FONT, "black")
            drawText("Back", playSurface, 580, 485, FONT, "black")
            fpsController.tick(50)
            timer += 1
            if timer % 100 == 0:
                color = "blue"
            elif timer % 50 == 0:
                color = "red"
            pygame.display.update()
            if fgh != 0:
                break

        if fgh == "menu":
            menu()
    else:
        # Difficulty chooser
        difficulty = 0
        timer = 0
        color = "blue"
        while True:
            playSurface.fill("black")
            difficultyRects = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100),
                               pygame.Rect(505, 450, 240, 100),
                               pygame.Rect(255, 575, 240, 100)]
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                if event.type == MOUSEBUTTONDOWN:
                    if difficultyRects[0].collidepoint(pygame.mouse.get_pos()):
                        difficulty = "easy"
                    if difficultyRects[1].collidepoint(pygame.mouse.get_pos()):
                        difficulty = "medium"
                    if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                        difficulty = "hard"
                    if difficultyRects[3].collidepoint(pygame.mouse.get_pos()):
                        difficulty = "back"
            for rect in difficultyRects:
                pygame.draw.rect(playSurface, "red", rect)
            drawText("Pick a difficulty", playSurface, 90, 150, pygame.font.SysFont(None, 112), color)
            drawText("Easy", playSurface, 83, 485, FONT, "black")
            drawText("Medium", playSurface, 312, 485, FONT, "black")
            drawText("Hard", playSurface, 580, 485, FONT, "black")
            drawText("Back", playSurface, 330, 610, FONT, "black")
            fpsController.tick(50)
            timer += 1
            if timer % 100 == 0:
                color = "blue"
            elif timer % 50 == 0:
                color = "red"
            pygame.display.update()
            if difficulty != 0:
                break

        if difficulty == "back":
            menu()


menu()

main()

# Game
config = populateConfig(difficulty)
# Play Surface
width = config.get("windowWidth")
height = config.get("windowHeight")
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Aim trainer')

widthMax = config.get("maxWidthOfTarget")
lives = config.get("lives")
spawnTargetTimer = config.get("gameSpeeds")

while True:
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            quit()
        # exit with ESC
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.quit))
                # click
        if event.type == pygame.MOUSEBUTTONDOWN:
            foundPoint = False
            for point in aimPoints:
                # if foundPoint is false and distance from center of point is less than width of point
                if not foundPoint and distance(event.pos, point) < point[2]:
                    if point[3]:
                        score += ((widthMax - point[2]) * config.get("scoreMultiply"))
                        foundPoint = True
                    else:
                        score += ((50 + (widthMax - point[2])) * config.get("scoreMultiply"))
                        foundPoint = True
                    # remove clicked point
                    aimPoints.remove(point)
            # missed
            if not foundPoint:
                lives -= 1

    # new target/point 0
    if tickCounter == spawnTargetTimer:
        tickCounter = 0
        # insert target/point in aimPoint
        aimPoints.insert(0,
                         [
                             random.randrange(1, width),
                             random.randrange(1, height),
                             # width
                             0,
                             False
                         ])
        # print all targest/points on screen
        print(aimPoints)

    else:
        # speed of spawning
        tickCounter += 1
    # background
    playSurface.fill("black")
    # target width change and lives change
    for point in aimPoints:
        # width decreasing
        if point[3]:
            # width is 0
            if point[2] == 0:
                # point remove
                aimPoints.remove(point)
                lives -= 1
            # width else than 0
            else:
                point[2] -= 1
        # width not decreasing
        else:
            # if width is max
            if point[2] == widthMax:
                # width decreasing start
                point[3] = True
            # width increasing
            point[2] += 1
        # target spawn
        pygame.draw.circle(playSurface, "white",
                           (point[0], point[1]), point[2])
    # if you don't have any lives
    if lives <= 0:
        option = saveScore()
        if option == "No":
            if playAgain() == "Yes":
                # Difficulty chooser
                option = 0
                difficulty = 0
                timer = 0
                color = "blue"
                switch = False
                while True:
                    playSurface.fill("black")
                    difficultyRects = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100),
                                       pygame.Rect(505, 450, 240, 100), pygame.Rect(255, 575, 240, 100)]
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            quit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                quit()
                        if event.type == MOUSEBUTTONDOWN:
                            if difficultyRects[0].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "easy"
                            if difficultyRects[1].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "medium"
                            if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "hard"
                            if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                                option = "back"
                    for rect in difficultyRects:
                        pygame.draw.rect(playSurface, "red", rect)
                    drawText("Pick a difficulty", playSurface, 90, 150, pygame.font.SysFont(None, 112), color)
                    drawText("Easy", playSurface, 83, 485, FONT, "black")
                    drawText("Medium", playSurface, 312, 485, FONT, "black")
                    drawText("Hard", playSurface, 580, 485, FONT, "black")
                    drawText("Back", playSurface, 330, 610, FONT, "black")
                    fpsController.tick(50)
                    timer += 1
                    if timer % 100 == 0:
                        color = "blue"
                    elif timer % 50 == 0:
                        color = "red"
                    pygame.display.update()
                    if option != 0 or difficulty != 0:
                        break

                if option == "back":
                    menu()
                config = populateConfig(difficulty)
                width = config.get("windowWidth")
                height = config.get("windowHeight")
                playSurface = pygame.display.set_mode((width, height))
                pygame.display.set_caption('Aim trainer')

                widthMax = config.get("maxWidthOfTarget")
                lives = config.get("lives")
                spawnTargetTimer = config.get("gameSpeeds")
            else:
                quit()
        elif option == "Yes":
            if not isinstance(username, str):
                username = "none"
            value = config.get(username)
            if isinstance(value, str):
                value = int(value)
            elif not isinstance(value, int):
                value = 0

            if int(maxBestScore()) < int(score):
                with open(r"klikacka/leaderboard.ini", 'r+') as config:
                    config.write("maxScore" + ":" + str(score) + "\n")
                    config.seek(0)

            if value < score:
                with open(r"klikacka/leaderboard.ini", 'a') as config:
                    config.write(username + ":" + str(score) + "\n")

            if playAgain() == "Yes":
                # Difficulty chooser
                option = 0
                difficulty = 0
                timer = 0
                color = "blue"
                switch = False
                while True:
                    playSurface.fill("black")
                    difficultyRects = [pygame.Rect(5, 450, 240, 100), pygame.Rect(255, 450, 240, 100),
                                       pygame.Rect(505, 450, 240, 100), pygame.Rect(255, 575, 240, 100)]
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            quit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                quit()
                        if event.type == MOUSEBUTTONDOWN:
                            if difficultyRects[0].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "easy"
                            if difficultyRects[1].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "medium"
                            if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                                difficulty = "hard"
                            if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                                option = "back"
                    for rect in difficultyRects:
                        pygame.draw.rect(playSurface, "red", rect)
                    drawText("Pick a difficulty", playSurface, 90, 150, pygame.font.SysFont(None, 112), color)
                    drawText("Easy", playSurface, 83, 485, FONT, "black")
                    drawText("Medium", playSurface, 312, 485, FONT, "black")
                    drawText("Hard", playSurface, 580, 485, FONT, "black")
                    drawText("Back", playSurface, 330, 610, FONT, "black")
                    fpsController.tick(50)
                    timer += 1
                    if timer % 100 == 0:
                        color = "blue"
                    elif timer % 50 == 0:
                        color = "red"
                    pygame.display.update()
                    if option != 0 or difficulty != 0:
                        break

                if option == "back":
                    menu()
                config = populateConfig(difficulty)
                width = config.get("windowWidth")
                height = config.get("windowHeight")
                playSurface = pygame.display.set_mode((width, height))
                pygame.display.set_caption('Aim trainer')

                widthMax = config.get("maxWidthOfTarget")
                lives = config.get("lives")
                spawnTargetTimer = config.get("gameSpeeds")
                score = 0
            else:
                quit()

    showScore()
    showMisses()
    pygame.display.flip()
    pygame.display.update()
    fpsController.tick(tick_rate)
