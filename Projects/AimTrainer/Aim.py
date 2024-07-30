import pygame
import random
import sys

pygame.init()

def initialize_screen(fullscreen):
    if fullscreen:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((800, 600))

fullscreen = input("Do you want to run in fullscreen mode? (yes/no): ").lower() == 'yes'
screen = initialize_screen(fullscreen)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)

target_radius = 30
score = 0
time_limit = 30
start_time = pygame.time.get_ticks()
paused_time = 0
paused = False

def draw_target():
    x = random.randint(target_radius, screen.get_width() - target_radius)
    y = random.randint(target_radius, screen.get_height() - target_radius)
    pygame.draw.circle(screen, (255, 0, 0), (x, y), target_radius)
    return x, y

def display_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (50, 50))

def display_timer():
    elapsed_time = (pygame.time.get_ticks() - start_time - paused_time) / 1000
    timer_text = font.render(f'Time: {int(time_limit - elapsed_time)}', True, (255, 255, 255))
    screen.blit(timer_text, (screen.get_width() - 250, 50))
    return elapsed_time

def pause_screen():
    pause_text = font.render('Paused', True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(pause_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
    pygame.display.flip()

target_x, target_y = draw_target()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused_time += pygame.time.get_ticks() - pause_start_time
                paused = not paused
                if paused:
                    pause_start_time = pygame.time.get_ticks()
                    pause_screen()
                else:
                    start_time += pygame.time.get_ticks() - pause_start_time - paused_time
        if event.type == pygame.MOUSEBUTTONDOWN and not paused:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x - target_x) ** 2 + (mouse_y - target_y) ** 2 <= target_radius ** 2:
                score += 1
                target_x, target_y = draw_target()

    if not paused:
        screen.fill((0, 0, 0))
        
        elapsed_time = display_timer()
        if elapsed_time >= time_limit:
            game_over_text = font.render('Game Over', True, (255, 255, 255))
            screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        display_score()
        pygame.draw.circle(screen, (255, 0, 0), (target_x, target_y), target_radius)
        pygame.display.flip()
        
    clock.tick(60)
