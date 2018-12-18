import pygame
import sys
import cv2
import numpy as np

pygame.init()

display_width = 1920
display_height = 960

pygame.mixer.pre_init(44100,16,2,4096)
pygame.display.set_caption("Pro Boxer 5")
win = pygame.display.set_mode((display_width,display_height))

title = pygame.image.load("Pro-Boxer-.png")
title_rect = title.get_rect()
begin_prompt = pygame.image.load("begin prompt.png")
begin_prompt_rect = begin_prompt.get_rect()

player_x = 100
player_y = 660
width = 125
height = 300

bag_x = 1750
bag_y = 660

isJump = False
jumpCount = 10

isPunch = False
punchCount = 10
maxarmLength = (punchCount ** 2)
'''
#Music
pygame.mixer.music.load("Music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
'''
isMenu = True
run = True

while run:
    
    pygame.time.delay(10)
    
    #Break Condtion
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if isMenu:
        win.blit(title, (display_width/2 - title_rect.width/2, display_height/6))
        win.blit(begin_prompt, (display_width/2 - begin_prompt_rect.width/2, 6*display_height/7))
        pygame.display.update()
        continue
    
    #Refresh Background
    win.fill((0))
    
    #Movement for rectangle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and player_x + width < bag_x:
        player_x += 5
    if keys[pygame.K_LEFT]:
        player_x -= 5 

    if not isPunch:
        if keys[pygame.K_UP]:
            isPunch = True
    else:
        if punchCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            armLength = maxarmLength - (punchCount ** 2) * neg
            punchCount -= 1
            pygame.draw.rect(win,(255,0,0),(player_x + width, player_y + 100, armLength, 50))
        else:
            isPunch = False
            punchCount = 10

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            player_y -= (jumpCount ** 2) * 0.7 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    
    pygame.draw.rect(win,(0,255,0),(bag_x,bag_y,width,height))
    pygame.draw.rect(win,(255,0,0),(player_x,player_y,width,height))
    pygame.display.update()
    
    
