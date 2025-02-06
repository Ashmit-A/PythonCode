import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = (800, 600)
TARGET_RADIUS = 30
TARGET_SPEED_RANGE = 1.5
TIME_LIMIT = 30
BG_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)
PARTICLE_COUNT = 15
PARTICLE_FADE_RATE = 5
PARTICLE_LIFETIME_RANGE = (20, 50)
HIGH_SCORE_FILE = 'high_score.txt'

# Initialize Pygame objects
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)

# Utility Functions
def read_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def write_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))


class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.color = [255, 0, 0]
        self.lifetime = random.randint(*PARTICLE_LIFETIME_RANGE)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.lifetime -= 1
        self.color[0] = max(self.color[0] - PARTICLE_FADE_RATE, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), 3)


class Target:
    def __init__(self, screen_width, screen_height, dynamic):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dynamic = dynamic
        self.reset()

    def reset(self):
        self.x = random.randint(TARGET_RADIUS, self.screen_width - TARGET_RADIUS)
        self.y = random.randint(TARGET_RADIUS, self.screen_height - TARGET_RADIUS)
        self.vx = random.uniform(-TARGET_SPEED_RANGE, TARGET_SPEED_RANGE)
        self.vy = random.uniform(-TARGET_SPEED_RANGE, TARGET_SPEED_RANGE)

    def update(self):
        if self.dynamic:
            self.x += self.vx
            self.y += self.vy
            if self.x <= TARGET_RADIUS or self.x >= self.screen_width - TARGET_RADIUS:
                self.vx = -self.vx
            if self.y <= TARGET_RADIUS or self.y >= self.screen_height - TARGET_RADIUS:
                self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), TARGET_RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), TARGET_RADIUS - 5)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Dynamic Target Game")
        self.fullscreen = False
        self.dynamic_targets = True
        self.high_score = read_high_score()
        self.score = 0
        self.start_time = 0
        self.particles = []
        self.target = Target(SCREEN_SIZE[0], SCREEN_SIZE[1], self.dynamic_targets)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if self.fullscreen else pygame.display.set_mode(SCREEN_SIZE)

    def toggle_dynamic_targets(self):
        self.dynamic_targets = not self.dynamic_targets
        self.target.dynamic = self.dynamic_targets

    def create_particles(self, x, y):
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(x, y))

    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.screen)

    def display_text(self, text, position, size=36):
        font = pygame.font.Font(None, size)
        render = font.render(text, True, TEXT_COLOR)
        self.screen.blit(render, position)

    def game_loop(self):
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.target.reset()

        while True:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed_time >= TIME_LIMIT:
                if self.score > self.high_score:
                    self.high_score = self.score
                    write_high_score(self.high_score)
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (mouse_x - self.target.x) ** 2 + (mouse_y - self.target.y) ** 2 <= TARGET_RADIUS ** 2:
                        self.score += 1
                        self.create_particles(self.target.x, self.target.y)
                        self.target.reset()

            self.screen.fill(BG_COLOR)
            self.target.update()
            self.target.draw(self.screen)
            self.update_particles()
            self.draw_particles()
            self.display_text(f"Score: {self.score}", (50, 50), 36)
            self.display_text(f"Time: {int(TIME_LIMIT - elapsed_time)}", (SCREEN_SIZE[0] - 200, 50), 36)
            pygame.display.flip()
            clock.tick(60)

    def main_menu(self):
        while True:
            self.screen.fill(BG_COLOR)
            self.display_text("1. Start Game", (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 100))
            self.display_text("2. Settings", (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2))
            self.display_text("3. Quit", (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 + 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "start"
                    elif event.key == pygame.K_2:
                        return "settings"
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()

    def settings_menu(self):
        while True:
            self.screen.fill(BG_COLOR)
            self.display_text(f"1. Fullscreen: {'On' if self.fullscreen else 'Off'}", (50, 100))
            self.display_text(f"2. Dynamic Targets: {'On' if self.dynamic_targets else 'Off'}", (50, 200))
            self.display_text("3. Back", (50, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_2:
                        self.toggle_dynamic_targets()
                    elif event.key == pygame.K_3:
                        return

    def run(self):
        while True:
            choice = self.main_menu()
            if choice == "start":
                self.game_loop()
            elif choice == "settings":
                self.settings_menu()


# Run the game
if __name__ == "__main__":
    Game().run()
