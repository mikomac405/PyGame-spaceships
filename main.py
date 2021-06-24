import pygame
from pygame.time import Clock
import random
import os

# TODO - Sound player problems [$$$]
pygame.mixer.pre_init(44100, 16, 2, 4096)

WIDTH, HEIGHT = 900,500
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle spaceships")

pygame.font.init()
pygame.mixer.init()


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

BORDER = pygame.Rect((WIDTH/2)-5, 0, 10, HEIGHT)

FPS = 60
VELOCITY = 5
BULLETS_VELOCITY = 7
BONUS_VELOCITY = 3
BOMB_VELOCITY_VERTICAL = 4
BOMB_VELOCITY_HORIZONTAL = 6

MAX_BULLETS = 3
HEALTHS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 44

# [$$$]
SHOT_SOUND = pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))
# [$$$]
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_WIN = pygame.USEREVENT + 3
RED_WIN = pygame.USEREVENT + 4
YELLOW_LIFE = pygame.USEREVENT + 5
RED_LIFE = pygame.USEREVENT + 6
YELLOW_BOMB = pygame.USEREVENT + 7
RED_BOMB = pygame.USEREVENT + 8
YELLOW_HIT_BOMB = pygame.USEREVENT + 9
RED_HIT_BOMB = pygame.USEREVENT + 10

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BOMB = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets","bomb.png")),(25,25)
)

HEART = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "heart.png")),(25,25)
)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_status, yellow_status, hearts, bombs, red_bombs_amount, yellow_bombs_amount, red_bombs, yellow_bombs):
    SURFACE.blit(SPACE, (0,0))
    pygame.draw.rect(SURFACE, BLACK, BORDER)
    SURFACE.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    SURFACE.blit(RED_SPACESHIP, (red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(SURFACE, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(SURFACE, RED, bullet)
    for heart in hearts:
        SURFACE.blit(HEART, (heart.x, heart.y))
    for bomb in bombs:
        SURFACE.blit(BOMB, (bomb.x, bomb.y))
    if yellow_bombs_amount > 0:
        SURFACE.blit(BOMB, (5, HEIGHT-30))
        if yellow_bombs_amount > 1:
            SURFACE.blit(BOMB, (35, HEIGHT-30))
    if red_bombs_amount > 0:
        SURFACE.blit(BOMB, (WIDTH-30, HEIGHT-30))
        if red_bombs_amount > 1:
            SURFACE.blit(BOMB, (WIDTH-60, HEIGHT-30))

    for bomb in red_bombs:
        SURFACE.blit(BOMB, (bomb[0].x, bomb[0].y))
    
    for bomb in yellow_bombs:
        SURFACE.blit(BOMB, (bomb[0].x, bomb[0].y))

    SURFACE.blit(yellow_status,(0,0))    
    w, h = red_status.get_size()
    SURFACE.blit(red_status,(WIDTH-w,0))
    pygame.display.update()

def yellow_handle_movement(keys, yellow):
    if keys[pygame.K_a] and yellow.x - VELOCITY > 0: # LEFT
        yellow.x -= VELOCITY
    if keys[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: # RIGHT
        yellow.x += VELOCITY
    if keys[pygame.K_w] and yellow.y - VELOCITY > 0: # UP
        yellow.y -= VELOCITY
    if keys[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT: # DOWN
        yellow.y += VELOCITY

def red_handle_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: # LEFT
        red.x -= VELOCITY
    if keys[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: # RIGHT
        red.x += VELOCITY
    if keys[pygame.K_UP] and red.y - VELOCITY > 0: # UP
        red.y -= VELOCITY
    if keys[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT: # DOWN
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            # [$$$]
            HIT_SOUND.play()
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # [$$$]
            HIT_SOUND.play()
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)

def handle_bonus(hearts, bombs, red, yellow):
    for heart in hearts:
        heart.y += BONUS_VELOCITY
        if yellow.colliderect(heart):
            pygame.event.post(pygame.event.Event(YELLOW_LIFE))
            hearts.remove(heart)
        if red.colliderect(heart):
            pygame.event.post(pygame.event.Event(RED_LIFE))
            hearts.remove(heart)
        if heart.y > HEIGHT:
            hearts.remove(heart)
    for bomb in bombs:
        bomb.y += BONUS_VELOCITY
        if yellow.colliderect(bomb):
            pygame.event.post(pygame.event.Event(YELLOW_BOMB))
            bombs.remove(bomb)
        if red.colliderect(bomb):
            pygame.event.post(pygame.event.Event(RED_BOMB))
            bombs.remove(bomb)
        if bomb.y > HEIGHT:
            bombs.remove(bomb)

def handle_bombs(red_bombs, yellow_bombs, red, yellow):
    for red_bomb in red_bombs:
        bomb, initX, initY = red_bomb
        if bomb.x > initX-70 and bomb.y > initY-40:
            bomb.x -= BOMB_VELOCITY_HORIZONTAL
            bomb.y -= BOMB_VELOCITY_VERTICAL
        else:
            bomb.x -= BOMB_VELOCITY_HORIZONTAL
            bomb.y += BOMB_VELOCITY_VERTICAL
        if yellow.colliderect(bomb):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_BOMB))
            # [$$$]
            HIT_SOUND.play()
            red_bombs.remove(red_bomb)
        if bomb.y > HEIGHT:
            red_bombs.remove(red_bomb)

    for yellow_bomb in yellow_bombs:
        bomb, initX, initY = yellow_bomb
        if bomb.x < initX+70 and bomb.y > initY-40:
            bomb.x += BOMB_VELOCITY_HORIZONTAL
            bomb.y -= BOMB_VELOCITY_VERTICAL
        else:
            bomb.x += BOMB_VELOCITY_HORIZONTAL
            bomb.y += BOMB_VELOCITY_VERTICAL
        if red.colliderect(bomb):
            pygame.event.post(pygame.event.Event(RED_HIT_BOMB))
            # [$$$]
            HIT_SOUND.play()
            yellow_bombs.remove(yellow_bomb)
        if bomb.y > HEIGHT:
            yellow_bombs.remove(yellow_bomb)


def check_win(red_health, yellow_health):
    if yellow_health < 1:
        pygame.event.post(pygame.event.Event(RED_WIN))
    elif red_health < 1:
        pygame.event.post(pygame.event.Event(YELLOW_WIN))

def main():
    myFont = pygame.font.SysFont('Arial',20, bold=True)

    red = pygame.Rect((WIDTH/4)*3-SPACESHIP_WIDTH/2, HEIGHT/2-SPACESHIP_HEIGHT/2, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    yellow = pygame.Rect(WIDTH/4-SPACESHIP_WIDTH/2, HEIGHT/2-SPACESHIP_HEIGHT/2, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    red_bullets = []
    yellow_bullets = []

    hearts = []
    bombs = []

    red_bombs_amount = 2
    yellow_bombs_amount = 2

    red_bombs = []
    yellow_bombs = []

    red_health = HEALTHS
    yellow_health = HEALTHS

    winner = 'DRAW!'

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # [$$$]
                    SHOT_SOUND.play()
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height/2 - 3, 10, 6)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # [$$$]
                    SHOT_SOUND.play()
                    bullet = pygame.Rect(
                        red.x-10, red.y + red.height/2-3, 10, 6)
                    red_bullets.append(bullet)
                if event.key == pygame.K_LSHIFT and yellow_bombs_amount > 0:
                    # [$$$]
                    SHOT_SOUND.play()
                    yellow_bombs_amount -= 1
                    bomb = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height/2 - 12, 25, 25)
                    yellow_bombs.append((bomb,bomb.x,bomb.y))
                if event.key == pygame.K_RSHIFT and red_bombs_amount > 0:
                    # [$$$]
                    SHOT_SOUND.play()
                    red_bombs_amount -= 1
                    bomb = pygame.Rect(
                        red.x-25, red.y + red.height/2 - 12, 25, 25)
                    red_bombs.append((bomb,bomb.x,bomb.y))
                    
            if event.type == YELLOW_HIT:
                yellow_health -=1
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == RED_LIFE:
                red_health += 1
            if event.type == YELLOW_LIFE:
                yellow_health += 1
            if event.type == YELLOW_BOMB and yellow_bombs_amount < 2:
                yellow_bombs_amount += 1
            if event.type == RED_BOMB and red_bombs_amount < 2:
                red_bombs_amount += 1
            if event.type == RED_HIT_BOMB:
                red_health -= 3
            if event.type == YELLOW_HIT_BOMB:
                yellow_health -= 3
            if event.type == RED_WIN:
                winner = "RED WINS!"
                run = False
            elif event.type == YELLOW_WIN:
                winner = "YELLOW WINS!"
                run = False

        random_heart = random.randint(1,100)
        random_bomb = random.randint(1,100)

        if random_heart == 1:
            heart = pygame.Rect(random.randint(0,WIDTH-10), -10, 10, 10)
            hearts.append(heart)
        
        if random_bomb == 1:
            bomb = pygame.Rect(random.randint(0,WIDTH-10), -10, 10, 10)
            bombs.append(bomb)


        red_status = myFont.render("Healths: {}".format(red_health), False, WHITE)
        yellow_status = myFont.render("Healths: {}".format(yellow_health), False, WHITE)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)        
        red_handle_movement(keys_pressed, red) 
        
        handle_bonus(hearts, bombs, red, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        handle_bombs(red_bombs, yellow_bombs, red, yellow)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_status, yellow_status, hearts, bombs, red_bombs_amount, yellow_bombs_amount, red_bombs, yellow_bombs)
        
        check_win(red_health,yellow_health)
    myFont = pygame.font.SysFont('Arial',50, bold=True)
    win_text = myFont.render(winner, False, WHITE)
    w, h = win_text.get_size()
    SURFACE.blit(win_text,((WIDTH/2)-(w/2),(HEIGHT/2)-(h/2)))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()
