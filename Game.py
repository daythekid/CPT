import pygame
import sys
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("face.xml")

camera = cv2.VideoCapture(0)

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
pygame.display.set_caption("Pro Boxer 5")

displayWidth = 1920
displayHeight = 960

win = pygame.display.set_mode((displayWidth,displayHeight))

title = pygame.image.load("Pro-Boxer-.png")
title_rect = title.get_rect()
begin_prompt = pygame.image.load("begin prompt.png")
begin_prompt_rect = begin_prompt.get_rect()
isMenu = True

player_x = 100
player_y = 660
width = 125
height = 300

bag_x = 1750
bag_y = 660



#Music
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

run = True

isJump = False
jumpCount = 10

isPunch = False
punchCount = 10
maxarmLength = (punchCount ** 2)

def jump():
    global jumpCount,isJump,player_y
    if jumpCount >= -10:
        neg = 1
        if jumpCount < 0:
            neg = -1
        player_y -= (jumpCount ** 2) * 0.7 * neg
        jumpCount -= 1
    else:
        isJump = False
        jumpCount = 10

def punch():
    global punchCount,maxarmLength, isPunch
    if punchCount >= -10:
        neg = 1
        if punchCount < 0:
            neg = -1
        armLength = maxarmLength - (punchCount ** 2) * neg
        punchCount -= 1
        pygame.draw.rect(win,(255,0,0),(player_x + width, player_y + 100, armLength, 50))
    else:
        isPunch = False
        punchCount = 10

joystick = pygame.joystick.Joystick(0)
joystick.init()

while run:
    #Break Condtion
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if isMenu:
        win.blit(title, (displayWidth/2 - title_rect.width/2, displayHeight/6))
        win.blit(begin_prompt, (displayWidth/2 - begin_prompt_rect.width/2, 6*displayHeight/7))
        pygame.display.update()
        '''
        if start is pressed:
            isMenu = False
        '''
        continue
    
    global position
    ret,img = camera.read()
    #Converts video feed to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    
    for (x,y,w,h) in faces:
        position = (displayWidth- (x+(w/2))*3)
    
    #Refresh Background
    win.fill((0))
    #Movement for rectangle
    keys = pygame.key.get_pressed()
    try:
        player_x = position
    except:
        player_x = 0
    '''
    for event in pygame.event.get():
        if not isPunch:
            if joystick.get_button(0) == 1:
                isPunch = True
        else:
            punch()

        if not isJump:
            if joystick.get_button(0) == 0:
                isJump = True
        else:
            jump()
    '''
    pygame.draw.rect(win,(0,255,0),(bag_x,bag_y,width,height))
    pygame.draw.rect(win,(255,0,0),(player_x,player_y,width,height))
    pygame.display.update()

camera.release()
cv2.distoryAllWindows()
