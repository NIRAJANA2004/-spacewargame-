import pygame
import random
import math
from pygame import mixer
from database import insert_player_name 

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space War Game")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.png")

# Sounds
laser_sound = mixer.Sound("laser.wav")
explosion_sound = mixer.Sound("explosion.wav")

# Fonts
font = pygame.font.Font(None, 32)
input_font = pygame.font.Font(None, 48)
over_font = pygame.font.Font(None, 64)

# Game variables
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 3
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_change = 2
enemy_y_change = 40
bullet_x = 0
bullet_y = 480
bullet_y_change = 6
bullet_state = "ready"
score = 0

clock = pygame.time.Clock()

# Text Input for Name 

def get_player_name():
    input_box = pygame.Rect(250, 250, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text.strip():
                        insert_player_name(text.strip())
                        return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 20:
                            text += event.unicode

        screen.blit(background, (0, 0))
        title = over_font.render("Enter Your Name", True, (255, 255, 255))
        screen.blit(title, (250, 180))
        txt_surface = input_font.render(text, True, (255, 255, 255))
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+10))

        pygame.display.flip()
        clock.tick(30)

# Display functions

def show_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over, (280, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.hypot(enemy_x - bullet_x, enemy_y - bullet_y)
    return distance < 27

player_name = get_player_name()
print("Name Saved:", player_name)
# Main game loop
running = True
while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                laser_sound.play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0

    player_x += player_x_change
    player_x = max(0, min(player_x, 736))

    enemy_x += enemy_x_change
    if enemy_x <= 0 or enemy_x >= 736:
        enemy_x_change *= -1
        enemy_y += enemy_y_change

    if enemy_y > 440:
        game_over_text()
        break

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
        explosion_sound.play()
        bullet_y = 480
        bullet_state = "ready"
        score += 1
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score()
    pygame.display.update()

pygame.quit()
