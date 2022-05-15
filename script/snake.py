import random
import os
import pygame
from pygame.locals import *

pygame.init()

# defining global variable
clockobject = pygame.time.Clock()
fps = 60
screen_width = 1000
screen_height = 700
start_game = True
pass_game = False
over = False
score = 0
run = True
tile_size = 20

# define font
font = pygame.font.Font('freesansbold.ttf', 60)
font2 = pygame.font.Font('freesansbold.ttf', 22)

# loading and scaling background image
bg = pygame.transform.scale(pygame.image.load(f"./resources/images/bg.png"), (1000, 700))

screen = pygame.display.set_mode((screen_width, screen_height)) # screen resolution
pygame.display.set_caption('Snake game') # window title

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BLUE = (66, 81, 245)
YELLOW = (245, 237, 12)

"""def draw_grid():
    for line in range(0, 700//20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(0, 1000//20):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))"""

######################################################## SNAKE PROPERTY ########################################################
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = True
        self.speed = 20
        self.direction = 1
        self.angle = 0
        self.length = 3
        self.frame_index = 0
        self.new_action = 0
        self.action = 1
        self.body_turn = 0
        self.minus = 1
        self.snake_position2 = []
        self.snake_position = [((20, 20), 0, 0, 0), ((20, 40), 0, 0, 0), ((20, 60), 0, 0, 0)]
        self.sleep_time = pygame.time.get_ticks()
        self.head_time = pygame.time.get_ticks()

        # loading snake head images
        self.head = []
        for i in range(1, len(os.listdir(f'./resources/images/snake/head'))+1):
            img = pygame.image.load(f"./resources/images/snake/head/{i}.png")
            self.head.append(img)
        self.image_head = self.head[0]

        # loading snake turn images
        self.turn = []
        turn_name = ["ld", "lu", "rd", "ru"]
        for i in range(1, len(os.listdir(f'./resources/images/snake/turn'))+1):
            img = pygame.image.load(f"./resources/images/snake/turn/{turn_name[i-1]}.png")
            self.turn.append(img)
        self.image_turn = self.turn[0]

        # loading snake body images
        self.body = []
        for i in range(1, len(os.listdir(f'./resources/images/snake/body'))+1):
            img = pygame.image.load(f"./resources/images/snake/body/{i}.png")
            self.body.append(img)
        self.image_body = self.body[0]

        # starting coordinates
        self.rect = self.image_head.get_rect()
        self.rect.x = 20
        self.rect.y = 60


    def move(self):
        global over
        dx = 0
        dy = 20

        if self.moving_up:
            dy = -self.speed
            dx = 0
            self.direction = -1
    
        elif self.moving_down:
            dy = self.speed
            dx = 0
            self.direction = 1
        
        elif self.moving_right:
            dx = self.speed
            dy = 0
            self.direction = 2

        elif self.moving_left:
            dx = -self.speed
            dy = 0
            self.direction = -2
        
        
        if self.direction == 1:
            self.angle = 0
        elif self.direction == -1:
            self.angle = 180
        elif self.direction == 2:
            self.angle = 90
        elif self.direction == -2:
            self.angle = 270

        #boarder check
        if self.rect.bottom > screen_height-20:
            self.rect.bottom = screen_height-20
            dy = 0
            over = True
        if self.rect.top < 20:
            self.rect.top = 20
            dy = 0
            over = True
        if self.rect.right > screen_width-20:
            self.rect.right = screen_width-20
            dx = 0
            over = True
        if self.rect.left < 20:
            self.rect.left = 20
            dx = 0
            over = True

        if self.sleep_time_fn():
            self.rect.x += dx
            self.rect.y += dy

            
            self.snake_position.append([(self.rect.x, self.rect.y), self.angle, 0, self.body_turn])
            if self.new_action == 1:
                self.snake_position[len(self.snake_position)-2][2] = 1
                self.snake_position[len(self.snake_position)-2][3] = self.body_turn
                self.new_action = 0
            if self.length == len(self.snake_position)-1:
                self.snake_position2 = self.snake_position[:]
                self.snake_position.pop(0)
        

    def sleep_time_fn(self):
        COOLDOWN = 300
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.sleep_time > COOLDOWN:
            self.sleep_time = pygame.time.get_ticks()
            return True

    # snake head animation
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image_head = self.head[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.head_time > ANIMATION_COOLDOWN:
            self.head_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.head):
            self.frame_index = 0
    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            if self.action == 1:
                if new_action == 2: self.body_turn = 3
                elif new_action == -2: self.body_turn = 1
            elif self.action == -1:
                if new_action == 2: self.body_turn = 2
                elif new_action == -2: self.body_turn = 0
            elif self.action == 2:
                if new_action == 1: self.body_turn = 0
                elif new_action == -1: self.body_turn = 1
            elif self.action == -2:
                if new_action == 1: self.body_turn = 2
                elif new_action == -1: self.body_turn = 3
            self.action = new_action
            
    # drawing snake
    def draw(self):
        global over
        self.image_head_r = pygame.transform.rotate(self.image_head, self.angle)
        if over:
            self.snake_position = self.snake_position2[:len(self.snake_position)]
            self.minus = 0
        for i in self.snake_position[1:len(self.snake_position)-self.minus]:
            if i[2] != 1:
                screen.blit(pygame.transform.rotate(self.body[0], i[1]), i[0])
            else:
                screen.blit(self.turn[i[3]], i[0])
        if self.snake_position[0][2] == 1:
            if self.snake_position[0][1] == 0 or self.snake_position[0][1] == 180:
                self.rotate = 270
            else: self.rotate = 0
        else:
            self.rotate = self.snake_position[0][1]
        screen.blit(self.image_head_r, self.rect)
        screen.blit(pygame.transform.rotate(self.body[1], self.rotate), self.snake_position[0][0])

    # checking for body collision
    def collision(self):
        global over
        for i in self.snake_position[:len(self.snake_position)-1]:
            if self.rect.colliderect(i[0][0], i[0][1], 20, 20):
                over = True

    # updating snake action
    def update(self):
        global over
        self.collision()
        self.draw()
        if not over:
            self.update_animation()
            self.move()

######################################################### EGG PROPERTY ########################################################
class Egg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # loading egg images
        self.image_egg = pygame.image.load(f"./resources/images/snake/egg.png")
        self.image_egg = pygame.transform.scale(self.image_egg, (12, 16))
        self.rect = self.image_egg.get_rect()
        # setting random position
        self.rect.x = random.randint(1, 1000//20-2)*tile_size
        self.rect.y = random.randint(1, 700//20-2)*tile_size

    # drawing egg
    def update(self):
        self.collision()
        screen.blit(self.image_egg, self.rect)

    # checking for snake and egg collision
    def collision(self):
        global egg, score
        if snake.rect.colliderect(self.rect.x, self.rect.y, self.image_egg.get_width(), self.image_egg.get_height()):
            snake.length += 1
            score += 1
            egg = Egg()
            self.kill()

# score function
def scorefn():
    score_show = font2.render(f"score {score}", True, BLUE)
    score_Rect = score_show.get_rect()
    score_Rect.center = (screen_width-score_Rect.width//2-5, screen_height-score_Rect.height//2)
    screen.blit(score_show, score_Rect)

# game over function
def GameOverfn():
    GameOver_show = font.render("Game Over", True, RED)
    GameOver_Rect = GameOver_show.get_rect()
    GameOver_Rect.center = (screen_width//2, screen_height//2)
    screen.blit(GameOver_show, GameOver_Rect)

snake = Snake()
egg = Egg()

while run:
    clockobject.tick(fps) # setting fps
    # rendering border and background image
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, YELLOW, (0, 0, screen_width, 20))
    pygame.draw.rect(screen, YELLOW, (0, 0, 20, screen_height))
    pygame.draw.rect(screen, YELLOW, (0, screen_height-20, screen_width, 20))
    pygame.draw.rect(screen, YELLOW, (screen_width-20, 0, 20, screen_height))
    #draw_grid()

    snake.update()
    egg.update()
    scorefn()
    if over:
        GameOverfn()


    # evevts listener
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not snake.moving_right:
                snake.moving_left = True
                snake.moving_right = snake.moving_up = snake.moving_down = False
                snake.new_action = 1
                snake.update_action(-2)
            elif event.key == pygame.K_RIGHT and not snake.moving_left:
                snake.moving_right = True
                snake.moving_left = snake.moving_up = snake.moving_down = False
                snake.new_action = 1
                snake.update_action(2)
            elif event.key == pygame.K_UP and not snake.moving_down:
                snake.moving_up = True
                snake.moving_left = snake.moving_right = snake.moving_down = False
                snake.new_action = 1
                snake.update_action(-1)
            elif event.key == pygame.K_DOWN and not snake.moving_up:
                snake.moving_down = True
                snake.moving_left = snake.moving_right = snake.moving_up = False
                snake.new_action = 1
                snake.update_action(1)

    pygame.display.update()

pygame.quit()