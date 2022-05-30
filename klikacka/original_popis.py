#Aim trainer

import pygame, sys, random, time, math, os

#check if there are any errors in the code
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initialising errors".format(check_errors[1]))
    print("Exiting...")
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialised!")
    print("You can play without any problems!")

#Play Surface
width = 1280
height = 720
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Aim trainer')

#Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

#game speed controller
tick_rate = 30
fpsController = pygame.time.Clock()

#Game state
tickCounter = 0
spawnTargetTimer = 30
aimPoints = []
score = 0
lives = 3
widthMax = 40


#Game over function
def gameOver():
    #font and size
    myFont = pygame.font.SysFont('monaco', 72)
    #text, antialias, collor
    gameOverSurface = myFont.render('Game Over!', True, white)
    gameOverRectangle = gameOverSurface.get_rect()
    gameOverRectangle.midtop = (width/2, height/20)
    playSurface.blit(gameOverSurface, gameOverRectangle)
    showScore(0)
    pygame.display.flip()
    #wait 3 seconds
    time.sleep(3)
    #close window
    pygame.quit()
    sys.exit()

def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Score: {0}'.format(score), True, white)
    scoreRectangle = scoreSurface.get_rect()
    if choice == 1:
        scoreRectangle.midtop=(width/20,height/20)
    else:
        scoreRectangle.midtop=(width/2,height/4)
    playSurface.blit(scoreSurface,scoreRectangle)

def showMisses():
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Lives: {0}'.format(lives), True, white)
    scoreRectangle = scoreSurface.get_rect()
    scoreRectangle.midtop=(width-(width/20),height/20)
    playSurface.blit(scoreSurface,scoreRectangle)

def timer():
    tFont = pygame.font.SysFont('monaco', 24)

def distance(A, B):
    #clicked distance from center of the point
    return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)





#Main game logic
while True:
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #exoit with ESC
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.quit))   
        #click
        if event.type == pygame.MOUSEBUTTONDOWN:
            foundPoint = False
            for point in aimPoints:
                #if foundPoint is false and distance from center of point is less than width of point
                if not foundPoint and distance(event.pos, point) < point[2]:
                    if point[3]:
                        score+= (widthMax - point[2])
                    else:
                        score+= (50 + (widthMax - point[2]))
                        foundPoint = True
                    #remove clicked point
                    aimPoints.remove(point)
            #missed
            if not foundPoint:
                lives-=1

    #new target/point 0
    if tickCounter == spawnTargetTimer:
        tickCounter = 0
        #insert target/point in aimPoint
        aimPoints.insert(0,
        [
        random.randrange(1,width),
        random.randrange(1,height),
        #width
        0,
        False
        ])
        #print all targest/points on screen
        print(aimPoints)
        
    else:
        #speed of spawning
        tickCounter+=1
    #background
    playSurface.fill(black)
    #target width change and lives change
    for point in aimPoints:
        #width decreasing
        if point[3]:
            #width is 0
            if point[2] == 0:
                #point remove
                aimPoints.remove(point)
                lives-=1
            #width else than 0
            else:
                point[2]-=1
        #width not decreasing
        else:
            #if width is max
            if point[2] == widthMax:
                #width decreasing start
                point[3] = True
            #width increasing
            point[2]+=1
        #target spawn
        pygame.draw.circle(playSurface, white, 
        (point[0], point[1]), point[2])
    #if you don't have any lives
    if lives == 0:
        #you die
        gameOver()

    showScore()
    showMisses()
    pygame.display.flip()
    fpsController.tick(tick_rate)