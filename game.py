import pygame
import random 
import sys   

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Final Hours")



# Player
player_width = 50
player_height = 50
player = pygame.Rect(width / 2 - player_width / 2, height - player_height - 10, player_width, player_height)
player_color = (255, 255, 255)

pygame.draw.rect(window, player_color, player)


# Enemy
enemy_width = 50
enemy_height = 50
num_enemies = 6
enemies = []
for i in range(num_enemies):
    enemy = pygame.Rect(random.randint(0, width - enemy_width), random.randint(-height, 0), enemy_width, enemy_height)
    enemies.append(enemy)
enemy_color = (255, 0, 0)

pygame.draw.rect(window, enemy_color, enemy)

# Projectile
projectile_width = 10
projectile_height = 20
projectile_speed = 2
projectiles = []
projectile_color = (255, 255, 0)
fire_rate = 10 
fire_counter = 0 


# Speed Logic
player_speed = 7
enemy_speed = 3 

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
    pygame.draw.rect(window, player_color, player)

    # Move the enemies
    for enemy in enemies:
        enemy.y += enemy_speed
        pygame.draw.rect(window, enemy_color, enemy)

    # Handle shooting 
    if keys[pygame.K_SPACE] and fire_counter == 0:
        fire_counter = fire_rate 
        projectile = pygame.Rect(player.x + player_width / 2 - projectile_width / 2, player.y - projectile_height, projectile_width, projectile_height)
        projectiles.append(projectile)
        # shoot_sound.play()
    
    if fire_counter > 0:
        fire_counter -= 1
    
    
    # Move and draw the projectiles
    for projectile in projectiles:
        projectile.y -= projectile_speed
        pygame.draw.rect(window, projectile_color, projectile)
    
    # Collision detection
    for enemy in enemies:
        if player.colliderect(enemy):
            pygame.quit()
            sys.exit()
        
        for projectile in projectiles:
            if enemy.colliderect(projectile):
                # explosion_sound.play()
                projectiles.remove(projectile)
                enemies.remove(enemy)
    
    # If all enemies are dead, spawn new ones
    if len(enemies) == 0:
        num_enemies += 1 
        for i in range(num_enemies):
            enemy = pygame.Rect(random.randint(0, width - enemy_width), random.randint(-height, 0), enemy_width, enemy_height)
            enemies.append(enemy)
    
    # Update the display
    pygame.display.update()

    # Limit the framerate
    clock.tick(60)
        