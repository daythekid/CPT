import pygame
import cv2
import threading
import random

displayWidth = 1920
displayHeight = 960

win = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Pro Boxer 5")

pygame.init()
pygame.joystick.init()
useJoystick = False

# Testing for joystick
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    useJoystick = True
except:
    print("There was an error finding your joystick.")
    print("Please use Z and X instead")

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

jump_button = 0
punch_button = 0

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

run = True
isMenu = True
'''
def opencv():
    global position
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("face.xml")
    while run:
        ret, img = camera.read()
        # Converts video feed to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            position = x + (w/2)

opencv_thread = threading.Thread(name="Facial Detection", target=opencv)
opencv_thread.start()
'''
width = 125
height = 300
position = 0

# Variables for player
playerJump = False
jumpCount = 15
jumpCooldown = 20

player_x = 100
player_y = 660
player_health = 100

startPunch = False
punchTimer = 10
punchCooldown = 0

# Variables for bot
bot_x = displayWidth - width - 100
bot_y = 660
bot_health = 100

bot_startPunch = False
bot_punchTimer = 10
bot_punchCooldown = 0

botJump = False
bot_jumpCount = 15
bot_jumpCooldown = 20

moveBack = False

# Menu Screen and background
title = pygame.image.load("Pro-Boxer-.png")
title_rect = title.get_rect()
begin_prompt = pygame.image.load("begin prompt.png")
begin_prompt_rect = begin_prompt.get_rect()
background = pygame.transform.scale(pygame.image.load("background.gif"), (1920, 1080))
background_rect = background.get_rect()

win_screen = pygame.transform.scale(pygame.image.load("win_screen.jpg"), (1920, 1080))
win_rect = win_screen.get_rect()
lose_screen = pygame.transform.scale(pygame.image.load("lose_screen.jpg"), (1920, 1080))
lose_rect = lose_screen.get_rect()

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                jump_button = 1
            if event.key == pygame.K_z:
                punch_button = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                jump_button = 0
            if event.key == pygame.K_z:
                punch_button = 0
    
    if useJoystick:
        jump_button = joystick.get_button(0)
        punch_button = joystick.get_button(1)

    win.blit(background, background_rect)

    if isMenu:
        win.blit(title, (displayWidth/2 - title_rect.width/2, displayHeight/6))
        win.blit(begin_prompt, (displayWidth/2 - begin_prompt_rect.width/2, 6*displayHeight/7))
        pygame.display.update()

        if jump_button == 1 or punch_button == 1:
            isMenu = False
        continue

    if (450 - position) * 5 + width < bot_x:
        player_x = (450 - position) * 5

    # Player Control
    if punchCooldown == 0:
        if punch_button == 1:
            startPunch = True
    else:
        punchCooldown -= 1
    
    if startPunch:
        punchTimer -= 1
        pygame.draw.rect(win, (255, 0, 0), (player_x + width, player_y + 100, 100, 50))
        if punchTimer == 0:
            if player_x + width + 100 > bot_x and not botJump:
                bot_health -= 5
            startPunch = False
            punchTimer = 10
            punchCooldown = 30

    if jumpCooldown == 0:
        if jump_button == 1:
            playerJump = True
    else:
        jumpCooldown -= 1
    
    if playerJump:
        if jumpCount >= -15:
            neg = 1
            if jumpCount < 0:
                neg = -1
            player_y -= (jumpCount ** 2) * 0.2 * neg
            jumpCount -= 1
        else:
            playerJump = False
            jumpCount = 15
            jumpCooldown = 50

    # Bot movement and fighting
    if bot_jumpCooldown == 0:
        if punchTimer == 1:
            if random.randint(0, 1) == 1:
                botJump = True
    else:
        bot_jumpCooldown -= 1

    if moveBack:
        if bot_x <= displayWidth - width - 100:
            bot_x += 10
        else:
            moveBack = False
    
    elif bot_x - 75 <= player_x + width:
        bot_startPunch = True
    
    else:
        bot_x -= 10

    if bot_startPunch:
        bot_punchTimer -= 1
        pygame.draw.rect(win, (0, 255, 0), (bot_x, bot_y + 100, -100, 50))
        if bot_punchTimer == 0:
            if bot_x - 100 < player_x + width and not playerJump:
                player_health -= 5
                moveBack = True
            bot_startPunch = False
            bot_punchTimer = 10
            bot_punchCooldown = 30

    if botJump:
        if bot_jumpCount >= -15:
            bot_neg = 1
            if bot_jumpCount < 0:
                bot_neg = -1
            bot_y -= (bot_jumpCount ** 2) * 0.2 * bot_neg
            bot_jumpCount -= 1
        else:
            botJump = False
            bot_jumpCount = 15
    
    # Drawing sprites and rectangles
    pygame.draw.rect(win, (0, 255, 0), (bot_x, bot_y, width, height))
    pygame.draw.rect(win, (0, 255, 0), (displayWidth-650, 50, 600, 50), 2)
    pygame.draw.rect(win, (0, 255, 0), (displayWidth-50, 50, bot_health*(-6), 50))
    pygame.draw.rect(win, (255, 0, 0), (player_x, player_y, width, height))
    pygame.draw.rect(win, (255, 0, 0), (50, 50, 600, 50), 2)
    pygame.draw.rect(win, (255, 0, 0), (50, 50, player_health*6, 50))
    
    # Winning or losing
    if player_health <= 0:
        win.blit(lose_screen, lose_rect)
    if bot_health <= 0:
        win.blit(win_screen, win_rect)
    pygame.display.update()
