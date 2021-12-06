import pygame
from pygame.locals import *
from pygame import mixer

import math


pygame.init()
clock = pygame.time.Clock()
running = True


class Screen:
    def __init__(self, width=800, height=800) -> None:
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.rect = self.screen.get_rect()


pygame.display.set_caption("Pong")

class Slider:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.image.load("Assets/sliderTwo(1).png").convert()
        self.rect = self.surface.get_rect(midleft=(20, 80))

    # move slider up or down 
    # positive distance -> move down
    # negative distance -> move up
    def move(self, distance):
        self.rect.y += distance
        slider.rect.clamp_ip(self.screen.rect) # makes it so that the slider can not go beyond the screen


class Ball:
    x_speed, y_speed = 0, 0
    x, y = 0, 0

    def __init__(self, startingLocation=(300, 300), velocity=2) -> None:
        self.startingLocation = float(
            startingLocation[0]), float(startingLocation[1])
        self.velocity = velocity

        self.surface = pygame.image.load("Assets/ball.png").convert()
        self.rect = self.surface.get_rect(midright=startingLocation)
        self.collision = pygame.mixer.Sound("Assets/ding.mp3")

    # reset ball to starting location
    def spawn_ball(self):
        self.x_speed, self.y_speed = -1 * self.velocity, -1 * self.velocity
        self.x, self.y = self.startingLocation

    # move the ball based on the x_speed and y_speed
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x, self.rect.y = int(self.x), int(self.y)
    
    # increase velocity by a multiplier
    def multiply_velocity(self, multiplier):
        self.velocity *= multiplier

    # calculates the direction of where the ball will go
    def calc_bounce_velocity(slider_rect, ball_rect):
        relativeY = slider_rect.centery - ball_rect.centery
        # convert relativeY to a value between -1 and 1
        normalizedRelativeY = relativeY/(slider.rect.height/2)
        bounceAngle = normalizedRelativeY * 5*math.pi/12
        return math.cos(bounceAngle) * ball.velocity, -math.sin(bounceAngle)* ball.velocity

    # change the direction based on where the ball hits the slider
    def bounce(self, slider):
        self.x_speed, self.y_speed = Ball.calc_bounce_velocity(slider.rect, self.rect)

    # reverse the speed in the x direction
    def reverse_x_direction(self):
        self.x_speed = -self.x_speed

    # reverse the speed in the y direction
    def reverse_y_direction(self):
        self.y_speed = -self.y_speed


# screen_variables class
screen = Screen()

# font_variable class
font = pygame.font.Font("Assets/Pixeltype.ttf", 50)

# slider_variables class
slider = Slider(screen)

# ball class
ball = Ball()
ball.spawn_ball()

score = 0
mixer.init()
mixer.music.load("Assets/ambient-piano-amp-strings-10711.mp3")
mixer.music.play(-1)

game_over = False

counting = True


def print_game_over(screen, font, score):
    text_x = 155
    game_over_text = font.render(
        "game over, your score was " + str(score), False, "White")
    game_over_text_two = font.render(
        "press backspace to play again", False, "White")
    game_over_text_three = font.render(
        "press escape if you want to quit", False, "White")
    screen.screen.blit(game_over_text, (text_x, 340))
    screen.screen.blit(game_over_text_two, (text_x, 370))
    screen.screen.blit(game_over_text_three, (text_x, 400))


while running == True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checks if the user pressed esc so that it can exit the game
        if key[pygame.K_ESCAPE]:
            running = False

    # set background to black
    screen.screen.fill((0, 0, 0))

    # checks if the game is over
    if game_over == True:
        pygame.mixer.music.pause()
        print_game_over(screen, font, score)

        # checks if backspace was pressed so that it can restart the game
        if key[pygame.K_BACKSPACE]:
            pygame.mixer.music.rewind()
            pygame.mixer.music.unpause()
            score = 0

            game_over = False
            counting = True

            slider.rect.x = 20
            slider.rect.y = 40

            ball.spawn_ball()
        # checks if the user pressed esc so that it can exit the game
        elif key[pygame.K_ESCAPE]:
            running = False

    else:
        text = font.render('Score ' + str(score), False, "White")

        # draws all the elements
        screen.screen.blit(text, (650, 10))
        screen.screen.blit(slider.surface, slider.rect)

        # calc the ball's new location
        ball.move()
        # draw the ball
        screen.screen.blit(ball.surface, (ball.rect.x, ball.rect.y))

        # makes the slider go down
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            slider.move(3)

        # makes the slider go up
        if key[pygame.K_UP] or key[pygame.K_w]:
            slider.move(-3)

        # if ball colides with slider
        if slider.rect.colliderect(ball.rect):
            ball.bounce(slider)
            if counting:
                # increases the ball speed by 10%
                ball.multiply_velocity(1.1)
                counting = False
                score += 1
                pygame.mixer.Sound.play(ball.collision)

            print(f'speed x,y: {ball.x_speed}, {ball.y_speed}')

        # if ball colides with top or bottom edge reverse y direction
        if ball.rect.top <= 0 or ball.rect.bottom >= screen.screen_height:
            counting = True
            ball.reverse_y_direction()
            print(f'speed x,y: {ball.x_speed}, {ball.y_speed}')

        screen.screen.blit(text, (650, 10))

        # if ball colides with the right side
        if ball.rect.right >= screen.screen_width:
            counting = True
            ball.reverse_x_direction()
            print(f'speed x,y: {ball.x_speed}, {ball.y_speed}')
        # if the ball colides with the left and delcares game over
        if ball.rect.left <= 0:
            game_over = True

    pygame.display.update()
    clock.tick(60)
