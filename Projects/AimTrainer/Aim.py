import pygame
import random
import sys

pygame.init()

# Initialize some global settings
fullscreen = False
dynamic_targets = True
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)

# Game settings
target_radius = 30
target_speed_range = 1.5  # Maximum speed for target movement
score = 0
time_limit = 30
high_score = 0
particle_list = []
high_score_file = 'high_score.txt'

def read_high_score():
    global high_score
    try:
        with open(high_score_file, 'r') as file:
            high_score = int(file.read().strip())
    except FileNotFoundError:
        high_score = 0
    except ValueError:
        high_score = 0

def write_high_score():
    with open(high_score_file, 'w') as file:
        file.write(str(high_score))

def initialize_screen(fullscreen):
    if fullscreen:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(screen_size)

def initialize_target():
    x = random.randint(target_radius, screen.get_width() - target_radius)
    y = random.randint(target_radius, screen.get_height() - target_radius)
    vx = random.uniform(-target_speed_range, target_speed_range)  # Random x velocity
    vy = random.uniform(-target_speed_range, target_speed_range)  # Random y velocity
    return x, y, vx, vy

def draw_target(x, y):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), target_radius)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), target_radius - 5)  # Adding a border for better visuals

def update_target_position(x, y, vx, vy):
    x += vx
    y += vy

    if x > screen.get_width() - target_radius or x < target_radius:
        vx = -vx
    if y > screen.get_height() - target_radius or y < target_radius:
        vy = -vy

    return x, y, vx, vy

def display_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (50, 50))

def display_timer(elapsed_time):
    timer_text = font.render(f'Time: {int(time_limit - elapsed_time)}', True, (255, 255, 255))
    screen.blit(timer_text, (screen.get_width() - 250, 50))

def display_main_menu():
    screen.fill((0, 0, 0))
    start_text = menu_font.render('Start Game', True, (255, 255, 255))
    high_score_text = menu_font.render(f'High Score: {high_score}', True, (255, 255, 255))
    settings_text = menu_font.render('Settings', True, (255, 255, 255))
    quit_text = menu_font.render('Quit', True, (255, 255, 255))
    screen.blit(start_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 150))
    screen.blit(high_score_text, (screen.get_width() // 2 - 150, screen.get_height() // 2 - 50))
    screen.blit(settings_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 + 50))
    screen.blit(quit_text, (screen.get_width() // 2 - 50, screen.get_height() // 2 + 150))
    pygame.display.flip()

def main_menu():
    while True:
        display_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if screen.get_width() // 2 - 100 <= mouse_x <= screen.get_width() // 2 + 100 and \
                   screen.get_height() // 2 - 150 <= mouse_y <= screen.get_height() // 2 - 100:
                    return 'start'
                elif screen.get_width() // 2 - 100 <= mouse_x <= screen.get_width() // 2 + 100 and \
                     screen.get_height() // 2 + 50 <= mouse_y <= screen.get_height() // 2 + 100:
                    return 'settings'
                elif screen.get_width() // 2 - 50 <= mouse_x <= screen.get_width() // 2 + 50 and \
                     screen.get_height() // 2 + 150 <= mouse_y <= screen.get_height() // 2 + 200:
                    pygame.quit()
                    sys.exit()

def display_settings():
    screen.fill((0, 0, 0))
    fullscreen_text = menu_font.render(f'Fullscreen: {"On" if fullscreen else "Off"}', True, (255, 255, 255))
    dynamic_text = menu_font.render(f'Dynamic Targets: {"On" if dynamic_targets else "Off"}', True, (255, 255, 255))
    back_text = menu_font.render('Back to Menu', True, (255, 255, 255))
    screen.blit(fullscreen_text, (screen.get_width() // 2 - 150, screen.get_height() // 2 - 100))
    screen.blit(dynamic_text, (screen.get_width() // 2 - 150, screen.get_height() // 2))
    screen.blit(back_text, (screen.get_width() // 2 - 150, screen.get_height() // 2 + 100))
    pygame.display.flip()

def settings_menu():
    global fullscreen, screen, dynamic_targets
    while True:
        display_settings()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if screen.get_width() // 2 - 150 <= mouse_x <= screen.get_width() // 2 + 150 and \
                   screen.get_height() // 2 - 100 <= mouse_y <= screen.get_height() // 2 - 50:
                    fullscreen = not fullscreen
                    screen = initialize_screen(fullscreen)
                elif screen.get_width() // 2 - 150 <= mouse_x <= screen.get_width() // 2 + 150 and \
                     screen.get_height() // 2 <= mouse_y <= screen.get_height() // 2 + 50:
                    dynamic_targets = not dynamic_targets
                elif screen.get_width() // 2 - 150 <= mouse_x <= screen.get_width() // 2 + 150 and \
                     screen.get_height() // 2 + 100 <= mouse_y <= screen.get_height() // 2 + 150:
                    return

def create_particles(x, y):
    for _ in range(15):  # Create 15 particles per hit
        particle = {
            'pos': [x, y],
            'velocity': [random.uniform(-3, 3), random.uniform(-3, 3)],
            'color': [255, 0, 0],
            'lifetime': random.randint(20, 50)
        }
        particle_list.append(particle)

def update_particles():
    for particle in particle_list[:]:
        particle['pos'][0] += particle['velocity'][0]
        particle['pos'][1] += particle['velocity'][1]
        particle['lifetime'] -= 1
        particle['color'][0] = max(particle['color'][0] - 5, 0)  # Fade out effect
        if particle['lifetime'] <= 0:
            particle_list.remove(particle)
        else:
            pygame.draw.circle(screen, particle['color'], (int(particle['pos'][0]), int(particle['pos'][1])), 3)

def pause_screen():
    pause_text = font.render('Paused', True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(pause_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
    pygame.display.flip()

def game_loop():
    global score, high_score, start_time, paused, paused_time
    score = 0
    paused = False
    paused_time = 0
    start_time = pygame.time.get_ticks()

    # Initialize the target with position and velocity
    target_x, target_y, target_vx, target_vy = initialize_target()

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
                    create_particles(target_x, target_y)
                    target_x, target_y, target_vx, target_vy = initialize_target()

        if not paused:
            screen.fill((0, 0, 0))
            elapsed_time = (pygame.time.get_ticks() - start_time - paused_time) / 1000
            if elapsed_time >= time_limit:
                if score > high_score:
                    high_score = score
                    write_high_score()
                game_over_text = font.render('Game Over', True, (255, 255, 255))
                screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
                score_text = font.render(f'Score: {score}', True, (255, 255, 255))
                screen.blit(score_text, (50, 50))
                pygame.display.flip()
                pygame.time.wait(3000)
                return  # Exit the game loop and return to the main menu

            display_score()
            display_timer(elapsed_time)

            if dynamic_targets:
                target_x, target_y, target_vx, target_vy = update_target_position(target_x, target_y, target_vx, target_vy)

            draw_target(target_x, target_y)
            update_particles()
            pygame.display.flip()

        clock.tick(60)

# Load the high score when the game starts
read_high_score()

# Main game loop
while True:
    choice = main_menu()
    if choice == 'start':
        game_loop()
    elif choice == 'settings':
        settings_menu()