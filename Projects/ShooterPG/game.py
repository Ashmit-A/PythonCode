import pygame as p
from sys import exit
import random

# Initialize Pygame
p.init()
p.display.set_caption("Loads of fun!")

# Constants

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
FPS = 60

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = p.font.Font(None, 40)

# Paths
BACKGROUND_PATH = 'ShooterPG/BG.png'
BASE_PATH = 'ShooterPG/pixil-layer-Background.png'
PLAYER_PATH = 'ShooterPG/ShooterSprite.png'
PROJECTILE_PATHS = [
    'ShooterPG/p1.png',
    # 'ShooterPG/p2.png',
    # 'ShooterPG/p3.png'
]
TARGET_PATHS = [
    'ShooterPG/Target1.png',
]

# Classes
class Game:
    def __init__(self):
        self.screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = p.time.Clock()
        self.background = p.image.load(BACKGROUND_PATH).convert()
        self.base = p.image.load(BASE_PATH).convert()
        self.score = 0
        self.lives = 5
        self.running = False
        self.player = Player(self)
        self.projectiles = []
        self.targets = []
        self.target_timer = 0
        self.GAME_SPEED = 2
        self.PLAYER_SPEED = 3
        self.TARGET_SPAWN_RATE = 120

    def run(self):
        self.show_title_screen("Press SPACE to Start")
        while True:
            if not self.running:
                self.show_title_screen(
                    f"Game Over! Final Score: {self.score}\nPress SPACE to Start"
                )
                self.reset_game()  # Reset the game state here
                self.running = True  # Set running to True to restart the game loop

            self.handle_events()
            self.update_game_objects()
            self.render_game_objects()
            self.GAME_SPEED += 0.0005
            self.PLAYER_SPEED += 0.0005
            self.TARGET_SPAWN_RATE -= 0.01
            self.clock.tick(FPS)

    def show_title_screen(self, message):
        while True:
            self.screen.blit(self.background, (0,0))
            lines = message.split("\n")
            y_offset = 200
            for line in lines:
                text_surface = FONT.render(line, True, WHITE)
                self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, y_offset))
                y_offset += 50
            p.display.update()

            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    exit()
                if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                    self.running = True
                    return

    def handle_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if self.running:
                if event.type == p.KEYDOWN:
                    if event.key == p.K_a:
                        self.player.set_direction(-self.PLAYER_SPEED)
                    elif event.key == p.K_d:
                        self.player.set_direction(self.PLAYER_SPEED)
                    elif event.key in (p.K_SPACE, p.K_w):
                        self.player.attempt_shoot()
                if event.type == p.KEYUP:
                    if event.key in (p.K_a, p.K_d):
                        self.player.set_direction(0)

    def update_game_objects(self):
        self.player.update()
        for projectile in self.projectiles[:]:
            projectile.update(self.GAME_SPEED)
            if projectile.rect.bottom < 0:
                self.projectiles.remove(projectile)

        for target in self.targets[:]:
            target.update(self.GAME_SPEED)
            if target.rect.top > SCREEN_HEIGHT - 100:
                self.targets.remove(target)
                self.lives -= 1
                if self.lives <= 0:
                    self.running = False

        self.check_collisions()

        self.target_timer += 1
        if self.target_timer > self.TARGET_SPAWN_RATE:
            self.spawn_target()
            self.target_timer = 0

    def render_game_objects(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.base, (0, 500))
        self.player.render()
        for projectile in self.projectiles:
            projectile.render(self.screen)
        for target in self.targets:
            target.render(self.screen)

        score_surface = FONT.render(f"Score: {self.score}", True, WHITE)
        lives_surface = FONT.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_surface, (10, 510))
        self.screen.blit(lives_surface, (SCREEN_WIDTH - 120, 510))
        p.display.update()

    def check_collisions(self):
        for target in self.targets[:]:
            for projectile in self.projectiles[:]:
                if target.rect.colliderect(projectile.rect):
                    self.targets.remove(target)
                    self.projectiles.remove(projectile)
                    self.score += 10
                    break

    def spawn_target(self):
        x_position = random.randint(50, SCREEN_WIDTH - 50)
        target_image = random.choice(TARGET_PATHS)
        self.targets.append(Target(x_position, -50, target_image))

    def reset_game(self):
        self.score = 0
        self.lives = 5
        self.projectiles.clear()
        self.targets.clear()
        self.target_timer = 0
        self.player.cooldown_timer = 0  # Reset player's cooldown
        self.player.rect.midbottom = (SCREEN_WIDTH // 2, 500)  # Reset player's position

        self.GAME_SPEED = 2  # Reset game speed
        self.PLAYER_SPEED = 3  # Reset player speed
        self.TARGET_SPAWN_RATE = 120 # Rest target speed
        
class Player:
    def __init__(self, game):
        self.game = game
        self.image = p.image.load(PLAYER_PATH).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, 500))
        self.direction = 0
        self.cooldown_timer = 0  # Cooldown time for shooting
        self.shoot_timestamps = []  # Track the times of recent shots
        self.BLUE_BALLS = 9 # how many loads before punishment
        self.BLUE_BALLS_TIMER = 1500 # in how much time (in ms)
        self.BLUE_BALLS_PUNISH = 2.5 #punishment time

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        self.rect.x += self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.rect.x -= self.direction

        # Update the cooldown timer
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def attempt_shoot(self):
        # Prevent shooting if in cooldown
        if self.cooldown_timer > 0:
            return

        current_time = p.time.get_ticks()
        self.shoot_timestamps.append(current_time)

        self.shoot_timestamps = [ts for ts in self.shoot_timestamps if current_time - ts <= self.BLUE_BALLS_TIMER]

        if len(self.shoot_timestamps) > self.BLUE_BALLS:
            self.cooldown_timer = FPS * self.BLUE_BALLS_PUNISH 
        else:
            self.game.projectiles.append(self.fire_projectile())

    def fire_projectile(self):
        return Projectile(self.rect.centerx, self.rect.top)

    def render(self):
        self.game.screen.blit(self.image, self.rect)

class Projectile:
    def __init__(self, x, y):
        self.images = [p.image.load(path).convert_alpha() for path in PROJECTILE_PATHS]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.y = y

    def update(self, GAME_SPEED):
        self.y -= GAME_SPEED
        self.rect.y = self.y
        self.index = (self.index + 0.15) % len(self.images)
        self.image = self.images[int(self.index)]

    def render(self, screen):
        screen.blit(self.image, self.rect)


class Target:
    def __init__(self, x, y, image_path):
        self.image = p.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))
        self.y = y

    def update(self,GAME_SPEED):
        self.y += GAME_SPEED
        self.rect.y = self.y

    def render(self, screen):
        screen.blit(self.image, self.rect)

# Start the game
if __name__ == "__main__":
    Game().run()
