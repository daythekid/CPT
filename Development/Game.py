import pygame
import sys
import cv2
import threading
import time
import random

run = True
displayWidth = 1920
displayHeight = 960
width = 125
height = 300
position = 0

playerJump = False

playerPunch = False

player_x = 100
player_y = 660
player_health = 100

bot_health = 100
botJump = False

bot_x = displayWidth - width - 100
bot_y = 660

def opencv():
    global position
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("face.xml")
    while run:
        ret,img = camera.read()
        #Converts video feed to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            position = x+(w/2)
            
def botmove():
    global run, displayHeight, displayWidth, width, height, playerJump, playerPunch, player_x, player_y, player_health, bot_health, botJump, bot_x, bot_y

    title = pygame.image.load("Pro-Boxer-.png")
    title_rect = title.get_rect()
    begin_prompt = pygame.image.load("begin prompt.png")
    begin_prompt_rect = begin_prompt.get_rect()
    isMenu = True

    startPunch = False
    botPunch = False
    punchTimer = 20

    jumpCount = 15

    moveBack = False

    while run:
        print(1)
        if playerPunch:
            if random.randint(1,2) == 1:
                botJump = True
        
        if moveBack and bot_x <= displayWidth - width - 100:
            bot_x+= 15
        elif bot_x - 125 <= player_x + width:
            startPunch = True
        else:
            bot_x -= 15
        
        if startPunch:
            if not botPunch:
                botPunch = True
            elif startPunch:
                punchTimer -= 1
                if punchTimer > 10:
                    pygame.draw.rect(win,(255,0,0),(bot_x + width, bot_y + 100, 100, 50))
                elif punchTimer <= 0:
                    if bot_x - 100 < player_x + width and not playerJump:
                        player_health -= 5
                        moveBack = True
                    botPunch = False
                    startPunch = False
                    punchTimer = 20

        if botJump:
            if jumpCount >= -15:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                bot_y -= (jumpCount ** 2) * 0.2 * neg
                jumpCount -= 1
            else:
                botJump = False
                jumpCount = 15

        pygame.draw.rect(win,(0,255,0),(bot_x,bot_y,width,height))
        pygame.draw.rect(win,(0,255,0),(displayWidth-650,50,600,50),2)
        pygame.draw.rect(win,(0,255,0),(displayWidth-50,50,bot_health*(-6),50))

def main():
    # Music and intial variables
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.init()
    pygame.joystick.init()
    pygame.display.set_caption("Pro Boxer 5")

    win = pygame.display.set_mode((displayWidth,displayHeight))

    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    startPunch = False
    punchTimer = 20

    jumpCount = 15

    global position, run, displayHeight, displayWidth, width, height, playerJump, playerPunch, player_x, player_y, player_health, bot_health, botJump, bot_x, bot_y

    while run:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print("pressed")
            if event.type == pygame.JOYBUTTONUP:
                print("released")
            if event.type == pygame.QUIT:
                run = False
        
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        jump_button = joystick.get_button( 0 )
        punch_button = joystick.get_button( 1 )

        if isMenu:
            win.blit(title, (displayWidth/2 - title_rect.width/2, displayHeight/6))
            win.blit(begin_prompt, (displayWidth/2 - begin_prompt_rect.width/2, 6*displayHeight/7))
            pygame.display.update() # consider removing
            
            if jump_button == 1 or punch_button == 1:
                isMenu = False
            continue

        #Refresh Background
        win.fill((0))
        
        #Movement for rectangle
        #print(position)
        if (450 - position) * 5 + width < bot_x:
            player_x = (450 - position) * 5
        
        if punch_button == 1:
            startPunch = True
    
        if not playerPunch:
            playerPunch = True
        elif startPunch:
            punchTimer -= 1
            if punchTimer > 10:
                pygame.draw.rect(win,(255,0,0),(player_x + width, player_y + 100, 100, 50))
            elif punchTimer <= 0:
                if player_x + width + 100 > bot_x and not botJump:
                    bot_health -= 5
                playerPunch = False
                startPunch = False
                punchTimer = 20

        if not playerJump:
            if jump_button == 1:
                playerJump = True
        else:
            if jumpCount >= -15:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                player_y -= (jumpCount ** 2) * 0.2 * neg
                jumpCount -= 1
            else:
                playerJump = False
                jumpCount = 15

        pygame.draw.rect(win,(255,0,0),(player_x,player_y,width,height))
        pygame.draw.rect(win,(255,0,0),(50,50,600,50),2)
        pygame.draw.rect(win,(255,0,0),(50,50,player_health*6,50))
        pygame.display.update()
        


opencv_thread = threading.Thread(name="OpenCV Thread", target=opencv)
pygame_thread = threading.Thread(name="PyGame Thread", target=main)
bot_thread = threading.Thread(name="Bot Thread", target=botmove)

bot_thread.start()
opencv_thread.start()
pygame_thread.start()
