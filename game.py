import pygame
import random
import sys

pygame.init()

width = 1280
height = 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Final Hours")
pygame.mixer.init()
pygame.mixer.music.load("./assets/bgmusic.mp3")

# Class for Enemy


class ActiveRect(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.active = True


# Game Title
title_font = pygame.font.Font("./assets/fancy_font.ttf", 80)
title_text = title_font.render("Final Hours", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(width / 2, height / 4))

# Loading screen
start_font = pygame.font.Font(None, 50)
start_text = start_font.render("Start Game", True, (255, 255, 255))
start_rect = start_text.get_rect(center=(width / 2, height * 3 / 4 - 50))

exit_font = pygame.font.Font(None, 50)
exit_text = exit_font.render("Exit Game", True, (255, 255, 255))
exit_rect = exit_text.get_rect(center=(width / 2, height * 7 / 8))

# Sound
shooting_sound = pygame.mixer.Sound("./assets/Shooting_sound.wav")
game_music = "./assets/Game_music.mp3"
explosion_sound = pygame.mixer.Sound("./assets/Explosion.wav")

# Player Image
player_image = pygame.image.load("./assets/Player.png")
# double check to resize the image to 50 x 50, even though it's already 50 x 50 lol
player_image = pygame.transform.scale(player_image, (50, 50))

# Enemy Image
enemy_image = pygame.image.load("./assets/Enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Projectile Image
projectile_image = pygame.image.load("./assets/Projectile.png")
projectile_image = pygame.transform.scale(projectile_image, (10, 20))


def start_game_screen():
    pygame.mixer.music.play(-1)
    while True:
        window.fill((0, 0, 0))
        window.blit(title_text, title_rect)
        window.blit(start_text, start_rect)
        window.blit(exit_text, exit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return
                elif exit_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()


# Game Over Screen
game_over_font = pygame.font.Font(None, 80)
game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(width / 2, height / 2))

# Reset Game


def reset_game():
    global player, enemies, projectiles, enemy_projectiles, enemy_fire_timers, num_enemies

    # Reset player position
    player = pygame.Rect(width / 2 - player_width / 2, height -
                         player_height - 10, player_width, player_height)

    # Reset enemies
    enemies = []
    for i in range(num_enemies):
        enemy = ActiveRect(random.randint(0, width - enemy_width),
                           random.randint(-height, 0), enemy_width, enemy_height)
        enemies.append(enemy)

    # Reset projectiles
    enemy_projectiles = []
    projectiles = []

    # Reset enemy fire timers
    enemy_fire_timers = [random.randint(
        0, enemy_fire_rate) for _ in range(num_enemies)]


def game_over_screen():
    pygame.mixer.music.stop()
    while True:
        window.fill((0, 0, 0))
        window.blit(game_over_text, game_over_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return


start_game_screen()


# Player
player_width = 50
player_height = 50
player = pygame.Rect(width / 2 - player_width / 2, height -
                     player_height - 10, player_width, player_height)
player_color = (255, 255, 255)

window.blit(player_image, (player.x, player.y))


# Enemy
enemy_width = 50
enemy_height = 50
num_enemies = 6
enemies = []
for i in range(num_enemies):
    enemy = ActiveRect(random.randint(0, width - enemy_width),
                       random.randint(-height // 2, 0), enemy_width, enemy_height)
    enemies.append(enemy)
enemy_color = (255, 0, 0)

window.blit(enemy_image, (enemy.x, enemy.y))

# Projectile
projectile_width = 10
projectile_height = 20
projectile_speed = 10
projectiles = []
projectile_color = (255, 255, 0)
fire_rate = 6
fire_counter = 0


# Enemy Projectile
enemy_projectile_width = 10
enemy_projectile_height = 20
enemy_projectile_speed = 3
enemy_projectiles = []
enemy_projectile_color = (0, 255, 255)
enemy_fire_rate = 150
enemy_fire_timers = [random.randint(0, enemy_fire_rate)
                     for _ in range(num_enemies)]


# Speed Logic
player_speed = 7
enemy_speed = 1.5

clock = pygame.time.Clock()


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < width - player_width:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y < height - player_height:
        player.y += player_speed

    # Clear the screen
    window.fill((0, 0, 0))

    # Draw the player
    window.blit(player_image, (player.x, player.y))

    # Move the enemies and handle enemy projectiles
    for i, enemy in enumerate(enemies):
        if enemy.active:
            window.blit(enemy_image, (enemy.x, enemy.y))
            enemy.y += enemy_speed

    # Handle enemy shooting
        if enemy_fire_timers[i] == 0:
            enemy_fire_timers[i] = enemy_fire_rate
            enemy_projectile = pygame.Rect(enemy.x + enemy_width / 2 - enemy_projectile_width / 2,
                                           enemy.y + enemy_height, enemy_projectile_width, enemy_projectile_height)
            enemy_projectiles.append(enemy_projectile)
            # shoot_sound.play()

        enemy_fire_timers[i] -= 1

    # Move and draw the enemy projectiles
    for enemy_projectile in enemy_projectiles:
        enemy_projectile.y += enemy_projectile_speed
        window.blit(projectile_image, (enemy_projectile.x, enemy_projectile.y))

        if player.colliderect(enemy_projectile):
            explosion_sound.play()
            game_over_screen()
            reset_game()
            pygame.mixer.music.load("./assets/bgmusic.mp3")
            pygame.mixer.music.play(-1)
            start_game_screen()

        if enemy_projectile.y > height:
            if enemy_projectile in enemy_projectiles:
                enemy_projectiles.remove(enemy_projectile)

    # Handle shooting
    if keys[pygame.K_SPACE] and fire_counter == 0:
        fire_counter = fire_rate
        projectile = pygame.Rect(player.x + player_width / 2 - projectile_width / 2,
                                 player.y - projectile_height, projectile_width, projectile_height)
        projectiles.append(projectile)
        shooting_sound.play()

    if fire_counter > 0:
        fire_counter -= 1

    # Move and draw the projectiles
    for projectile in projectiles:
        projectile.y -= projectile_speed
        window.blit(projectile_image, (projectile.x, projectile.y))

    # Collision detection
    enmies_to_remove = []

    for enemy in enemies:
        if player.colliderect(enemy) and enemy.active:
            explosion_sound.play()
            game_over_screen()
            reset_game()
            pygame.mixer.music.load("./assets/bgmusic.mp3")
            pygame.mixer.music.play(-1)
            start_game_screen()

        for projectile in projectiles:
            if enemy.colliderect(projectile) and enemy.active:
                explosion_sound.play()
                if projectile in projectiles:
                    projectiles.remove(projectile)
                enemy.active = False
                enmies_to_remove.append(enemy)
                num_enemies -= 1

        # check if enemy is off screen
        if enemy.y > height and enemy.active:
            enemy.active = False
            num_enemies -= 1

    for enemy in enmies_to_remove:
        enemies.remove(enemy)

    # If all enemies are dead, spawn new ones
    if all(enemy.active == False for enemy in enemies):
        num_enemies += 5
        enemies = []
        enemy_fire_timers = []
        for i in range(num_enemies):
            enemy = ActiveRect(random.randint(0, width - enemy_width),
                               random.randint(-height // 2, 0), enemy_width, enemy_height)
            enemies.append(enemy)
            enemy_fire_timers.append(random.randint(0, enemy_fire_rate))

    # Update the display
    pygame.display.update()

    # Limit the framerate
    clock.tick(60)

    # Load and play game music
    if not pygame.mixer.music.get_busy():
        # Load and play game music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)
