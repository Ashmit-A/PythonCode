import pygame
import random
import math
import time


# Particle class
class Particle:
    def __init__(self, dimensions, bounds, screen_size):
        self.position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
        self.velocity = [random.uniform(-1, 1) for _ in range(dimensions)]
        self.best_position = self.position[:]
        self.best_value = float('inf')
        self.current_value = float('inf')
        self.screen_size = screen_size

    def update_velocity(self, global_best_position, inertia, cognitive, social):
        for i in range(len(self.velocity)):
            r1 = random.random()
            r2 = random.random()
            cognitive_velocity = cognitive * r1 * (self.best_position[i] - self.position[i])
            social_velocity = social * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = inertia * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, bounds):
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]
            # Ensure position is within bounds
            self.position[i] = max(bounds[0], min(bounds[1], self.position[i]))

    def screen_coordinates(self, bounds):
        """Convert function space coordinates to screen space coordinates."""
        x = int(self.screen_size[0] * (self.position[0] - bounds[0]) / (bounds[1] - bounds[0]))
        y = int(self.screen_size[1] * (self.position[1] - bounds[0]) / (bounds[1] - bounds[0]))
        return x, y


def sphere_function(position):
    """Sphere function: f(x) = sum(xi^2 for xi in x)."""
    return sum(x**2 for x in position)


def draw_heatmap(screen, bounds, screen_size, fitness_function):
    """Draw a heatmap where color intensity corresponds to fitness value."""
    for x in range(screen_size[0]):
        for y in range(screen_size[1]):
            # Convert screen coordinates to function space
            fx = bounds[0] + (x / screen_size[0]) * (bounds[1] - bounds[0])
            fy = bounds[0] + (y / screen_size[1]) * (bounds[1] - bounds[0])
            fitness_value = fitness_function([fx, fy])

            # Normalize the fitness value to [0, 255] for color mapping
            normalized_value = min(255, int(255 * fitness_value / 200))
            color = (normalized_value, 0, 255 - normalized_value)  # Gradient: Red to Blue
            screen.set_at((x, y), color)


def pso_visualization(dimensions, bounds, num_particles, max_iterations, screen_size):
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Particle Swarm Optimization Visualization with Heatmap")
    clock = pygame.time.Clock()
    running = True

    # Initialize particles
    particles = [Particle(dimensions, bounds, screen_size) for _ in range(num_particles)]
    global_best_position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
    global_best_value = float('inf')

    inertia = 0.7
    cognitive = 1.5
    social = 1.5

    for _ in range(max_iterations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw heatmap
        draw_heatmap(screen, bounds, screen_size, sphere_function)

        for particle in particles:
            # Evaluate the objective function
            particle.current_value = sphere_function(particle.position)

            # Update the particle's personal best
            if particle.current_value < particle.best_value:
                particle.best_value = particle.current_value
                particle.best_position = particle.position[:]

            # Update the global best
            if particle.current_value < global_best_value:
                global_best_value = particle.current_value
                global_best_position = particle.position[:]

        # Update velocity and position of each particle
        for particle in particles:
            particle.update_velocity(global_best_position, inertia, cognitive, social)
            particle.update_position(bounds)

            # Draw particle
            x, y = particle.screen_coordinates(bounds)
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)

        # Draw global best
        gb_x, gb_y = Particle(dimensions, bounds, screen_size).screen_coordinates(bounds)
        pygame.draw.circle(screen, (255, 0, 0), (gb_x, gb_y), 8)

        pygame.display.flip()
        clock.tick(30)  # Limit frame rate to 10 FPS

        # Slow down for better observation
        time.sleep(0)

        if not running:
            break

    pygame.quit()


# Run PSO visualization
if __name__ == "__main__":
    dimensions = 2  # Number of dimensions
    bounds = (-10, 10)  # Bounds for each dimension
    num_particles = 30  # Number of particles
    max_iterations = 100  # Maximum number of iterations
    screen_size = (800, 600)  # Pygame screen size

    pso_visualization(dimensions, bounds, num_particles, max_iterations, screen_size)
