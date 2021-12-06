from typing_extensions import runtime
import pygame
from pygame.locals import *
from pygame import mixer
from sys import exit
import math
import time


pygame.init()
clock = pygame.time.Clock()
running = True

class Pygame_variables:
   
    def screen_variables(self, screen_width, screen_height, screen, screen_rect):
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
    
    def font_variable(self,font_type):
        self.font_type = pygame.font.Font("Assets/Pixeltype.ttf" ,50)

    def ball_variables(self, ball, ball_rect):
        self.ball = pygame.image.load("Assets/ball.png").convert()
        self.ball_rect = self.ball.get_rect(midright = (300,300))
        
    def slider_variables(self, slider, slider_rect):
        self.slider = pygame.image.load("Assets/sliderTwo(1).png").convert()
        self.slider_rect = self.slider.get_rect(midleft = (20,80))


# screen_width = 800
# screen_height = 800
# screen = pygame.display.set_mode((screen_width, screen_height))
# screen_rect = screen.get_rect()
pygame.display.set_caption("Pong")

# font = pygame.font.Font("Assets/Pixeltype.ttf" ,50)

# ball = pygame.image.load("Assets/ball.png").convert()
# ball_rect = ball.get_rect(midright = (300,300))

# slider = pygame.image.load("Assets/sliderTwo(1).png").convert()
# slider_rect = slider.get_rect(midleft = (20,80))


score = 0
mixer.init()
mixer.music.load("Assets/pong_background_music.mp3")
mixer.music.play(-1)

collision = pygame.mixer.Sound("Assets/ding.mp3")


def calcBounceVelocity(slider_rect, ball_rect, x_direction):
    relativeY = slider_rect.centery - ball_rect.centery
    normalizedRelativeY = relativeY/(slider_rect.height/2) # convert relativeY to a value between -1 and 1
    bounceAngle = normalizedRelativeY * 5*math.pi/12 
    return math.cos(bounceAngle) * x_direction * ball_velocity, -math.sin(bounceAngle) * x_direction * ball_velocity

def spawnBall():
    global x_speed, y_speed, ball_x, ball_y, startingLoaction, ball_velocity
    ball_velocity = 2
    x_speed, y_speed = -1 * ball_velocity, -1 * ball_velocity
    ball_x, ball_y = startingLoaction

game_over = False

ball_velocity = 2
startingLoaction = float(ball_rect.x), float(ball_rect.y) # remember the starting location as a float

x_speed, y_speed = -1 * ball_velocity, -1 * ball_velocity
ball_x, ball_y = startingLoaction # tracking the ball's loaction as a float

counting = True

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # set background to black
    screen.fill((0, 0, 0))

    if game_over == True:
        pygame.mixer.music.pause()
        text_x = 155
        game_over_text = font.render("game over, your score was "+ str(score), False, "White")
        game_over_text_two = font.render("press backspace to play again", False, "White")
        game_over_text_three = font.render("press escape if you want to quit", False, "White")
        screen.blit(game_over_text, (text_x,340))
        screen.blit(game_over_text_two, (text_x,370))
        screen.blit(game_over_text_three, (text_x,400))
        
        key = pygame.key.get_pressed()
        if key[pygame.K_BACKSPACE]:
            pygame.mixer.music.unpause()
            score = 0

            game_over = False
            counting = True

            slider_rect.x = 20
            slider_rect.y = 40

            spawnBall()
        elif key[pygame.K_ESCAPE]:
            running = False
    
    else:
        text = font.render('Score '+ str(score), False, "White")

        #draws all the elements
        screen.blit(text, (650,10))
        screen.blit(slider, slider_rect)

        # calc the ball's new location
        ball_x += x_speed
        ball_y += y_speed
        ball_rect.x, ball_rect.y = int(ball_x), int(ball_y)
        screen.blit(ball, (ball_rect.x, ball_rect.y)) # draw the ball

        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            slider_rect.y += 3

        if key[pygame.K_UP] or key[pygame.K_w]:
            slider_rect.y -= 3

        slider_rect.clamp_ip(screen_rect)

        # if ball colides with slider
        if slider_rect.colliderect(ball_rect):
            x_speed, y_speed = calcBounceVelocity(slider_rect, ball_rect, 1)
            if counting:
                ball_velocity *= 1.1
                counting = False
                score += 1
                pygame.mixer.Sound.play(collision)

            print(f'speed x,y: {x_speed}, {y_speed}')

        # if ball colides with top or bottom edge reverse y direction
        if ball_rect.top <= 0 or ball_rect.bottom >= screen_height:
            counting = True
            y_speed = -y_speed
            print(f'speed x,y: {x_speed}, {y_speed}')

        screen.blit(text, (650,10))
        
        if ball_rect.right >= screen_width:
            counting = True
            x_speed = -x_speed
            print(f'speed x,y: {x_speed}, {y_speed}')

        if ball_rect.left <= 0:
            game_over = True
        


    pygame.display.update()
    clock.tick(60)
