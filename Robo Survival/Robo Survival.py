import pygame
from pygame.locals import *
import time
import sys
import pyganim
import random
import math

pygame.init()
pygame.font.init()
windowSurface = pygame.display.set_mode((512,512), 0, 32)
#pygame.image.load("facingLeftRobot.png")

class Enemy:
    def __init__(self, name, health_max, x, y, attack, type):
        self.name = name
        self.health_max = health_max
        self.x = x
        self.y = y
        self.attack = attack
        self.type = type #projectile/melee


class Player():
    def __init__(self, health_max, current_health):
        self.health_max = health_max
        self.current_health = current_health

class Room:
    def __init__(self, x, y, textures):
        self.x = x
        self.y = y
        self.textures = textures #modern/old/etc

class Damage:
    def __init__(self, attack_power, range, type):
        self.attack_power = attack_power
        self.range = range
        self.type = type

happened = False
heliMob = Enemy(name="Heli", health_max=10, attack=2, type="projectile", x=128, y=70)
player = Player(health_max=20, current_health=20)
startRoom = Room(x=256, y=256, textures="old")




# Drawing player health bar
def draw_health_bar(health):

        if health > 15:
            health_color = GREEN
        elif health > 10:
            health_color = (255,255,0)
        else:
            health_color = (255,0,0)
        pygame.draw.rect(windowSurface, health_color, (5, 10, health * 2.5, 10))

# Drawing individual health bars for enemy bots

# def enemy_health_bar(health):
#
#         if health > 15:
#             health_color = GREEN
#         elif health > 10:
#             health_color = (255,255,0)
#         else:
#             health_color = (255,0,0)
#
#         healthbar1 = pygame.draw.rect(windowSurface, health_color, (eBox1.x, eBox1.y - 10, health * 2, 6))
#         healthbar2 = pygame.draw.rect(windowSurface, health_color, (eBox2.x, eBox2.y - 10, health * 2, 6))
#
#         return healthbar1, healthbar2

def boss_health_bar(health):

        if health > 15:
            health_color = GREEN
        elif health > 10:
            health_color = (255,255,0)
        else:
            health_color = (255,0,0)
        pygame.draw.rect(windowSurface, health_color, (130, 100, health * 15, 10))



BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (0,0,0)
PLAYERSPEED = 4

background = pygame.image.load("NewBackground.png")
playerBot = pygame.image.load("facingLeftRobot.png").convert_alpha()
transColor = playerBot.get_at((20,20))
playerBot.set_colorkey(transColor)
botRect = pygame.Rect(248,248,32,32)
#background.blit(Robot,playerBot)
playerJab = pygame.Rect(248,248,48,32)

enemy1 = pygame.image.load("EnemyPosition1.png").convert_alpha()
eBox1 = pygame.Rect(120,376,32,32)
e1Life = "alive"

enemy2 = pygame.image.load("EnemyPosition1.png").convert_alpha()
eBox2 = pygame.Rect(376,376,32,32)
e2Life = "alive"

enemy3 = pygame.image.load("EnemyPosition1.png").convert_alpha()
eBox3 = pygame.Rect(240,376,32,32)
e3Life = "alive"

enemy4 = pygame.image.load("EnemyPosition1.png").convert_alpha()
eBox4 = pygame.Rect(192,136,32,32)
e4Life = "alive"

enemy5 = pygame.image.load("EnemyPosition1.png").convert_alpha()
eBox5 = pygame.Rect(320,136,32,32)
e5Life = "alive"

boss = pygame.image.load("SpiderBoss.png").convert_alpha()
bBox = pygame.Rect(224,224,64,64)
bossLife = "alive"

fireballListX = []
fireballListY = []

current_health = 70
health_max = 20
x_speed = 10
y_speed = 10
boss_health = 20
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
attacking = False
direction = "r"
damage = 1

mainClock = pygame.time.Clock()



windowSurface = pygame.display.set_mode((512,512), 0, 32)
pygame.display.set_caption("Dungeon Game")
windowSurface.fill(BLACK)
pygame.display.update()

leftAttackAnim = pyganim.PygAnimation([('facingLeftRobot.png',0.5),
                                        ('leftAttack.png',0.5)])
rightAttackAnim = pyganim.PygAnimation([('facingRightRobot.png',0.5),
                                        ('rightAttack.png',0.5)])
downAttackAnim = pyganim.PygAnimation([('facingDownRobot.png',0.5),
                                        ('downAttack.png',0.5)])
upAttackAnim = pyganim.PygAnimation([('facingUpRobot.png',0.5),
                                        ('upAttack.png',0.5)])
heliAnimLeft = pyganim.PygAnimation([('EnemyPosition1.png',0.5),
                                        ('EnemyPosition2.png',0.5)])
heliAnimRight = pyganim.PygAnimation([('EnemyPosition1f.png',0.5),
                                        ('EnemyPosition2f.png',0.5)])

leftAttackAnim.play()
rightAttackAnim.play()
downAttackAnim.play()
upAttackAnim.play()
heliAnimLeft.play()
heliAnimRight.play()
total_score = 0

againDisplay = pygame.font.Font("freesansbold.ttf",32)
againSurface = againDisplay.render("Retry",True,WHITE,BLACK)
againRect = againSurface.get_rect()
againRect.center = (256,384)

fireball = pygame.image.load("fireball.png").convert_alpha()

fireballListX = []
fireballListY = []
fireballSlopeX = []
fireballSlopeY = []
playing = True
while playing:
    healthText = pygame.font.SysFont('Comic Sans MS', 20)
    displayText = healthText.render("HP: " + str(current_health) , False, (255,255,255))
    displayScore = pygame.font.SysFont('Comic Sans MS', 20)
    currentScore = displayScore.render("Score: " + str(total_score) , False, (255,255,255))
    windowSurface.fill(BLACK)
    windowSurface.blit(background,[0,0])
    windowSurface.blit(playerBot, botRect)
    windowSurface.blit(displayText,[220,11])
    windowSurface.blit(currentScore,[410,11])
    tempHitBox = pygame.Rect(-5,-5,1,1)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord("a"):
                moveLeft = True
                direction = "l"
            if event.key == K_RIGHT or event.key == ord("d"):
                moveRight = True
                direction = "r"
            if event.key == K_UP or event.key == ord("w"):
                moveUp = True
                direction = "u"
            if event.key == K_DOWN or event.key == ord("s"):
                moveDown = True
                direction = "d"
            if event.key == K_SPACE:
                if direction == "l":
                    windowSurface.blit(background,[0,0])
                    leftAttackAnim.blit(windowSurface,(botRect.x-16,botRect.y))
                    tempHitBox = pygame.Rect(botRect.x-16,botRect.y,5,botRect.height)
                elif direction == "r":
                    windowSurface.blit(background,[0,0])
                    rightAttackAnim.blit(windowSurface,(botRect.x,botRect.y))
                    tempHitBox = pygame.Rect(botRect.x+16,botRect.y,5,botRect.height)
                elif direction == "u":
                    windowSurface.blit(background,[0,0])
                    upAttackAnim.blit(windowSurface,(botRect.x,botRect.y-8))
                    tempHitBox = pygame.Rect(botRect.x,botRect.y-16,botRect.width,5)
                elif direction == "d":
                    windowSurface.blit(background,[0,0])
                    downAttackAnim.blit(windowSurface,(botRect.x,botRect.y))
                    tempHitBox = pygame.Rect(botRect.x,botRect.y+16,botRect.width,5)
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord("a"):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord("d"):
                moveRight = False
            if event.key == K_UP or event.key == ord("w"):
                moveUp = False
            if event.key == K_DOWN or event.key == ord("s"):
                moveDown = False
        if event.type == MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            if againRect.collidepoint(mousePos):
                fireballListX = []
                fireballListY = []
                fireballSlopeX = []
                fireballSlopeY = []
                total_score = 0
                current_health = 70
                health_max = 20
                x_speed = 10
                y_speed = 10
                boss_health = 20
                moveLeft = False
                moveRight = False
                moveUp = False
                moveDown = False
                attacking = False
                direction = "r"
                damage = 1
                playing = True



    if (moveLeft == True) and botRect.left >= 0:
        botRect.x -= PLAYERSPEED
    elif (moveRight == True) and botRect.right <= 512:
        botRect.x += PLAYERSPEED

    if (moveUp == True) and botRect.top >= 40:
        botRect.y -= PLAYERSPEED
    elif (moveDown == True) and botRect.bottom <= 512:
        botRect.y += PLAYERSPEED

    if direction == "l":
        playerBot = pygame.image.load("facingLeftRobot.png").convert_alpha()
    elif direction == "r":
        playerBot = pygame.image.load("facingRightRobot.png").convert_alpha()
    elif direction == "u":
        playerBot = pygame.image.load("facingUpRobot.png").convert_alpha()
    elif direction == "d":
        playerBot = pygame.image.load("facingDownRobot.png").convert_alpha()

    def shots(eBox):
        possibleShots = [(eBox.x,eBox.y-16),
                        (eBox.x+(16/math.sqrt(2)),eBox.y-(16/math.sqrt(2))),
                        (eBox.x+16,eBox.y),
                        (eBox.x+(16/math.sqrt(2)),eBox.y+(16/math.sqrt(2))),
                        (eBox.x,eBox.y+16),
                        (eBox.x-(16/math.sqrt(2)),eBox.y+(16/math.sqrt(2))),
                        (eBox.x-16,eBox.y),
                        (eBox.x-(16/math.sqrt(2)),eBox.y-(16/math.sqrt(2)))]

        minimum = 10000
        index = 0
        for i in possibleShots:
            d = math.sqrt(((i[0]-botRect.x) ** 2) + (((i[1]-botRect.y) ** 2)))
            if d < minimum:
                minimum = d
                index = possibleShots.index(i)



        randNum = random.randint(1,20)
        if randNum == 1:
            fireballListX.append(eBox.x)
            fireballListY.append(eBox.y)
            fireballSlopeX.append(possibleShots[index][0]-eBox.x)
            fireballSlopeY.append(possibleShots[index][1]-eBox.y)

    if(e1Life != "dead"):
        shots(eBox1)
    if(e2Life != "dead"):
        shots(eBox2)
    if(e3Life != "dead"):
        shots(eBox3)
    if(e4Life != "dead"):
        shots(eBox4)
    if(e5Life != "dead"):
        shots(eBox5)


    def moveEnemy(eBox):
        x_speed = 10
        y_speed = 10
        x_speed *= random.choice([-1,1])
        y_speed *= random.choice([-1,1])
        randNum = random.randint(1,4)
        if randNum == 4:
            eBox.x += x_speed
            eBox.y += y_speed

    moveEnemy(eBox1)
    moveEnemy(eBox2)
    moveEnemy(eBox3)
    moveEnemy(eBox4)
    moveEnemy(eBox5)

    if eBox1.right >= 512:
        eBox1.right = 512
    elif eBox1.left <= 0:
        eBox1.left = 0

    if eBox1.top <= 0:
        eBox1.top = 0
    elif eBox1.bottom >= 512:
        eBox1.bottom = 512

    if eBox2.right >= 512:
        eBox2.right = 512
    elif eBox2.left <= 0:
        eBox2.left = 0

    if eBox2.top <= 0:
        eBox2.top = 0
    elif eBox2.bottom >= 512:
        eBox2.bottom = 512

    if eBox3.right >= 512:
        eBox3.right = 512
    elif eBox3.left <= 0:
        eBox3.left = 0

    if eBox3.top <= 0:
        eBox3.top = 0
    elif eBox3.bottom >= 512:
        eBox3.bottom = 512

    if eBox4.right >= 512:
        eBox4.right = 512
    elif eBox4.left <= 0:
        eBox4.left = 0

    if eBox4.top <= 0:
        eBox4.top = 0
    elif eBox4.bottom >= 512:
        eBox4.bottom = 512

    if eBox5.right >= 512:
        eBox5.right = 512
    elif eBox5.left <= 0:
        eBox5.left = 0

    if eBox5.top <= 0:
        eBox5.top = 0
    elif eBox5.bottom >= 512:
        eBox5.bottom = 512

    if e1Life == "alive":
        if botRect.x - eBox1.x <= 0:
            heliAnimLeft.blit(windowSurface,(eBox1.x,eBox1.y))
        elif botRect.x - eBox1.x >= 0:
            heliAnimRight.blit(windowSurface,(eBox1.x,eBox1.y))

    if e2Life == "alive":
        if botRect.x - eBox2.x <= 0:
            heliAnimLeft.blit(windowSurface,(eBox2.x,eBox2.y))
        elif botRect.x - eBox2.x >= 0:
            heliAnimRight.blit(windowSurface,(eBox2.x,eBox2.y))

    if e3Life == "alive":
        if botRect.x - eBox3.x <= 0:
            heliAnimLeft.blit(windowSurface,(eBox3.x,eBox3.y))
        elif botRect.x - eBox3.x >= 0:
            heliAnimRight.blit(windowSurface,(eBox3.x,eBox3.y))

    if e4Life == "alive":
        if botRect.x - eBox4.x <= 0:
            heliAnimLeft.blit(windowSurface,(eBox4.x,eBox4.y))
        elif botRect.x - eBox4.x >= 0:
            heliAnimRight.blit(windowSurface,(eBox4.x,eBox4.y))

    if e5Life == "alive":
        if botRect.x - eBox5.x <= 0:
            heliAnimLeft.blit(windowSurface,(eBox5.x,eBox5.y))
        elif botRect.x - eBox5.x >= 0:
            heliAnimRight.blit(windowSurface,(eBox5.x,eBox5.y))

    

    if tempHitBox.colliderect(eBox1):
        e1Life = "dead"
        total_score += 100



    if tempHitBox.colliderect(eBox2):
        e2Life = "dead"
        total_score += 100
        


    if tempHitBox.colliderect(eBox3):
        e3Life = "dead"
        total_score += 100
    

    if tempHitBox.colliderect(eBox4):
        e4Life = "dead"
        total_score += 100
        

    if tempHitBox.colliderect(eBox5):
        e5Life = "dead"
        total_score += 100
        

    if tempHitBox.colliderect(bBox):
        boss_health -= 1
    
        


#     enemyHealth = []

 #   enemyHealth.append(eBox2)

    if e1Life != "alive" and e2Life != "alive" and e3Life != "alive" and e4Life != "alive" and e5Life != "alive":


        windowSurface.blit(boss,(192,192))
        boss_health_bar(boss_health)
        randNum = random.randint(1,30)
        happened = False
        if boss_health <= 0 and happened == False:
            e1Life = "alive"
            e2Life = "alive"
            e3Life = "alive"
            e4Life = "alive"
            e5Life = "alive"
            current_health += 40
            boss_health = 20
            happened = True
        bossLabel = pygame.font.SysFont('Comic Sans MS',20)
        bossText = bossLabel.render("SPIDER BOSS: " + str(boss_health) + "HP", False, (255,255,255))
        windowSurface.blit(bossText,[160,120])
        if randNum == 1:
            fireballPos = [[248,248]] * 8
            for x in range(8):
                xcoord = random.randint(-16,16)
                ycoord = random.randint(-16,16)
                fireballListX.append(xcoord+248)
                fireballListY.append(ycoord+248)
                fireballSlopeX.append(xcoord)
                fireballSlopeY.append(ycoord)

    
    fireballRects = []
    if len(fireballListX) > 0:
        doneFireballs = []
        for i in range(len(fireballListX)):
            fireballRects.append(pygame.Rect(fireballListX[i],fireballListY[i],16,16))
            windowSurface.blit(fireball,(fireballRects[i].x,fireballRects[i].y))
            fireballListX[i] = fireballListX[i]+fireballSlopeX[i]
            fireballListY[i] = fireballListY[i]+fireballSlopeY[i]
            if (fireballListX[i] < 0 or fireballListX[i] > 512) or (fireballListY[i] < 0 or fireballListY[i] > 512):
                doneFireballs.append(i)
            if fireballRects[i].colliderect(botRect):
                
                current_health -= damage
        for i in doneFireballs: 
            fireballListX.remove(fireballListX[len(doneFireballs)-1-i])
            fireballListY.remove(fireballListY[len(doneFireballs)-1-i])
            fireballSlopeX.remove(fireballSlopeX[len(doneFireballs)-1-i])
            fireballSlopeY.remove(fireballSlopeY[len(doneFireballs)-1-i])
            fireballRects.remove(fireballRects[len(doneFireballs)-1-i])

    draw_health_bar(current_health)


                

    pygame.display.flip()
    pygame.display.update()


    if current_health <= 0:
        kText = pygame.font.SysFont('Comic Sans MS', 40)
        failText = kText.render("GAME OVER" , False, (255, 0 , 0))
        windowSurface.fill(BLACK)
        windowSurface.blit(failText,[140,170])
        finalScore = pygame.font.SysFont('Comic Sans MS', 40)
        scoreFinal = finalScore.render("Final Score: " + str(total_score), False, (255,255,255))
        windowSurface.blit(scoreFinal,[140,210])
        windowSurface.blit(againSurface,againRect)
        pygame.display.update()

    mainClock.tick(30)
