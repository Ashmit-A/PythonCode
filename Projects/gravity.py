import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Constants
G = 6.67430e-2  # Gravitational constant (scaled for visualization)
FPS = 60

# Classes
class Particle:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = mass // 3
        self.color = color
        self.vx = 0
        self.vy = 0

    def apply_force(self, fx, fy):
        """Apply a force to the particle (changes velocity)."""
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax
        self.vy += ay

    def update(self):
        """Update the particle's position and handle wall collisions."""
        self.x += self.vx
        self.y += self.vy

        # Reflect from walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx  # Reverse x-velocity
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))  # Keep inside bounds
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy = -self.vy  # Reverse y-velocity
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))  # Keep inside bounds

    def draw(self, screen):
        """Draw the particle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        """Draw the button on the screen."""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Check if the button is clicked."""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Functions
def calculate_gravitational_force(p1, p2):
    """Calculate the gravitational force between two particles."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distancesq = dx**2 + dy**2
    if distancesq == 0:
        return 0, 0  # Avoid division by zero

    # Clamp minimum distance to avoid extreme forces
    distancesq = max(distancesq, 25)

    force = G * p1.mass * p2.mass / distancesq
    angle = math.atan2(dy, dx)
    fx = math.cos(angle) * force
    fy = math.sin(angle) * force
    return fx, fy

# Initialize particles and buttons
particles = []
for _ in range(20):
    x = random.randint(100, WIDTH - 100)
    y = random.randint(100, HEIGHT - 100)
    mass = random.randint(55, 215)
    color = random.choice([RED, BLUE, WHITE])
    particles.append(Particle(x, y, mass, color))

font = pygame.font.Font(None, 36)
clear_button = Button(600, 20, 180, 40, "Clear Screen", font, GRAY, DARK_GRAY, lambda: particles.clear())

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Draw and handle button interactions
    clear_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if clear_button.is_clicked(event):
                clear_button.action()
            else:
                # Add particles based on mouse click
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:  # Left click
                    new_particle = Particle(mx, my, mass=100, color=RED)
                elif event.button == 3:  # Right click
                    new_particle = Particle(mx, my, mass=200, color=BLUE)
                elif event.button == 2: #middle click
                    new_particle = Particle(mx, my, mass=150, color=WHITE)
                particles.append(new_particle)

    # Calculate forces and update particles
    for i, p1 in enumerate(particles):
        total_fx, total_fy = 0, 0
        for j, p2 in enumerate(particles):
            if i != j:
                fx, fy = calculate_gravitational_force(p1, p2)
                total_fx += fx
                total_fy += fy
        p1.apply_force(total_fx, total_fy)

    # Update and draw particles
    for particle in particles:
        particle.update()
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
