from typing_extensions import runtime
import pygame
from pygame.locals import *
from pygame import mixer

import math



pygame.init()
clock = pygame.time.Clock()
running = True

#calculates the direction of where the ball will go 
def calcBounceVelocity(slider_rect, ball_rect, x_direction):
    relativeY = slider_rect.centery - ball_rect.centery
    normalizedRelativeY = relativeY/(sV.slider_rect.height/2) # convert relativeY to a value between -1 and 1
    bounceAngle = normalizedRelativeY * 5*math.pi/12 
    return math.cos(bounceAngle) * x_direction * ball.ball_velocity, -math.sin(bounceAngle) * x_direction * ball.ball_velocity

#spawns the ball in it's defualt location
def spawnBall():
    global x_speed, y_speed, ball_x, ball_y, startingLoaction, ball_velocity
    ball.ball_velocity = 2
    x_speed, y_speed = -1 * ball.ball_velocity, -1 * ball.ball_velocity
    ball_x, ball_y = ball.startingLoaction

class screen_variables:
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen_rect = screen.get_rect()
    


pygame.display.set_caption("Pong")

class font_variable:
    font = pygame.font.Font("Assets/Pixeltype.ttf" ,50)

class ball_variables:
    ball = pygame.image.load("Assets/ball.png").convert()
    ball_rect = ball.get_rect(midright = (300,300))

class slider_variables:
    slider = pygame.image.load("Assets/sliderTwo(1).png").convert()
    slider_rect = slider.get_rect(midleft = (20,80))

#screen_variables class
SV = screen_variables()

#font_variable class
FV = font_variable()

#ball_variables class
BV = ball_variables()

class ball:
    collision = pygame.mixer.Sound("Assets/ding.mp3")
    startingLoaction = float(BV.ball_rect.x), float(BV.ball_rect.y) # remember the starting location as a float
    ball_velocity = 2
    collision = pygame.mixer.Sound("Assets/ding.mp3")

#slider_variables class
sV = slider_variables()

#ball class
ball = ball()

score = 0
mixer.init()
mixer.music.load("Assets/ambient-piano-amp-strings-10711.mp3")
mixer.music.play(-1)

game_over = False

x_speed, y_speed = -1 * ball.ball_velocity, -1 * ball.ball_velocity
ball_x, ball_y = ball.startingLoaction # tracking the ball's loaction as a float

counting = True

while running == True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #checks if the user pressed esc so that it can exit the game
        if key[pygame.K_ESCAPE]:
            running = False

    # set background to black
    SV.screen.fill((0, 0, 0))

    #checks if the game is over
    if game_over == True:
        pygame.mixer.music.pause()
        text_x = 155
        game_over_text =       FV.font.render("game over, your score was "+ str(score), False, "White")
        game_over_text_two =   FV.font.render("press backspace to play again", False, "White")
        game_over_text_three = FV.font.render("press escape if you want to quit", False, "White")
        SV.screen.blit(game_over_text, (text_x,340))
        SV.screen.blit(game_over_text_two, (text_x,370))
        SV.screen.blit(game_over_text_three, (text_x,400))
        
        #checks if backspace was pressed so that it can restart the game
        if key[pygame.K_BACKSPACE]:
            pygame.mixer.music.rewind()
            pygame.mixer.music.unpause()
            score = 0

            game_over = False
            counting = True

            sV.slider_rect.x = 20
            sV.slider_rect.y = 40

            spawnBall()
        #checks if the user pressed esc so that it can exit the game
        elif key[pygame.K_ESCAPE]:
            running = False
    
    else:
        text = FV.font.render('Score '+ str(score), False, "White")

        #draws all the elements
        SV.screen.blit(text, (650,10))
        SV.screen.blit(sV.slider, sV.slider_rect)

        # calc the ball's new location
        ball_x += x_speed
        ball_y += y_speed
        BV.ball_rect.x, BV.ball_rect.y = int(ball_x), int(ball_y)
        SV.screen.blit(BV.ball, (BV.ball_rect.x, BV.ball_rect.y)) # draw the ball

        # makes the slider go down
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            sV.slider_rect.y += 3

        # makes the slider go up
        if key[pygame.K_UP] or key[pygame.K_w]:
            sV.slider_rect.y -= 3

        #makes it so that the slider can not go beyond the screen
        sV.slider_rect.clamp_ip(SV.screen_rect)

        # if ball colides with slider
        if sV.slider_rect.colliderect(BV.ball_rect):
            x_speed, y_speed = calcBounceVelocity(sV.slider_rect, BV.ball_rect, 1)
            if counting:
                #increases the ball speed by 10%
                ball.ball_velocity *= 1.1
                counting = False
                score += 1
                pygame.mixer.Sound.play(ball.collision)

            print(f'speed x,y: {x_speed}, {y_speed}')

        # if ball colides with top or bottom edge reverse y direction
        if BV.ball_rect.top <= 0 or BV.ball_rect.bottom >= SV.screen_height:
            counting = True
            y_speed = -y_speed
            print(f'speed x,y: {x_speed}, {y_speed}')

        SV.screen.blit(text, (650,10))
        
        #if ball colides with the right side
        if BV.ball_rect.right >= SV.screen_width:
            counting = True
            x_speed = -x_speed
            print(f'speed x,y: {x_speed}, {y_speed}')
        #if the ball colides with the left and delcares game over
        if BV.ball_rect.left <= 0:
            game_over = True
        
    pygame.display.update()
    clock.tick(60)