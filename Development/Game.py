import pygame
import sys
import cv2
import threading

global position


# Music and intial variables
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
pygame.joystick.init()
pygame.display.set_caption("Pro Boxer 5")

face_cascade = cv2.CascadeClassifier("face.xml")
try:
    camera = cv2.VideoCapture(0)
except:
    print("No camera found!")

displayWidth = 1920
displayHeight = 960

win = pygame.display.set_mode((displayWidth,displayHeight))

pygame.mixer.music.load("song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

run = True

isJump = False
jumpCount = 15

isPunch = False
startPunch = False
punchTimer = 20

title = pygame.image.load("Pro-Boxer-.png")
title_rect = title.get_rect()
begin_prompt = pygame.image.load("begin prompt.png")
begin_prompt_rect = begin_prompt.get_rect()
isMenu = True

player_x = 100
player_y = 660
player_health = 100

bag_x = 1000
bag_y = 660
bag_health = 100

width = 125
height = 300

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


    
    ret,img = camera.read()
    #Converts video feed to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        position = x+(w/2)

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

    try:
        player_x = (450 - position) * 5
    except:
        player_x = 100
    
    if punch_button == 1:
        startPunch = True
  
    if not isPunch:
        isPunch = True
    elif startPunch:
        punchTimer -= 1
        if punchTimer > 10:
            pygame.draw.rect(win,(255,0,0),(player_x + width, player_y + 100, 100, 50))
        elif punchTimer <= 0:
            if player_x + width + 100 > bag_x:
                bag_health -= 5
            isPunch = False
            startPunch = False
            punchTimer = 20

    if not isJump:
        if jump_button == 1:
            isJump = True
    else:
        if jumpCount >= -15:
            neg = 1
            if jumpCount < 0:
                neg = -1
            player_y -= (jumpCount ** 2) * 0.2 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 15
    
    pygame.draw.rect(win,(0,255,0),(bag_x,bag_y,width,height))
    pygame.draw.rect(win,(0,255,0),(displayWidth-650,50,600,50),2)
    pygame.draw.rect(win,(0,255,0),(displayWidth-50,50,bag_health*(-6),50))
    pygame.draw.rect(win,(255,0,0),(player_x,player_y,width,height))
    pygame.draw.rect(win,(255,0,0),(50,50,600,50),2)
    pygame.draw.rect(win,(255,0,0),(50,50,player_health*6,50))
    pygame.display.update()