import pygame
import random
import math
import time

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
            self.position[i] = max(bounds[0], min(bounds[1], self.position[i]))

    def screen_coordinates(self, bounds):
        x = int(self.screen_size[0] * (self.position[0] - bounds[0]) / (bounds[1] - bounds[0]))
        y = int(self.screen_size[1] * (self.position[1] - bounds[0]) / (bounds[1] - bounds[0]))
        return x, y


def target_function(position, target_position):
    return math.sqrt((position[0] - target_position[0])**2 + (position[1] - target_position[1])**2)


def pso_visualization(dimensions, bounds, num_particles, max_iterations, screen_size, target_position):
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Particle Swarm Optimization Visualization")
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font(None, 36)

    particles = [Particle(dimensions, bounds, screen_size) for _ in range(num_particles)]
    global_best_position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
    global_best_value = float('inf')
    best_iteration = 0

    inertia = 0.7
    cognitive = 1.5
    social = 1.5

    print(f"Running PSO for {max_iterations} iterations.")

    for iteration in range(max_iterations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for particle in particles:
            particle.current_value = target_function(particle.position, target_position)

            if particle.current_value < particle.best_value:
                particle.best_value = particle.current_value
                particle.best_position = particle.position[:]

            if particle.current_value < global_best_value:
                global_best_value = particle.current_value
                global_best_position = particle.position[:]
                best_iteration = iteration

        for particle in particles:
            particle.update_velocity(global_best_position, inertia, cognitive, social)
            particle.update_position(bounds)

            x, y = particle.screen_coordinates(bounds)
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)

        gb_x = int(screen_size[0] * (global_best_position[0] - bounds[0]) / (bounds[1] - bounds[0]))
        gb_y = int(screen_size[1] * (global_best_position[1] - bounds[0]) / (bounds[1] - bounds[0]))
        pygame.draw.circle(screen, (255, 0, 0), (gb_x, gb_y), 8)

        best_value_text = font.render(f"Best Value: {global_best_value:.2e}", True, (255, 255, 255))
        best_iteration_text = font.render(f"Best Iteration: {best_iteration}", True, (255, 255, 255))

        screen.blit(best_value_text, (screen_size[0] - best_value_text.get_width() - 10, 10))
        screen.blit(best_iteration_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

        print(f"Iteration {iteration + 1}/{max_iterations} - Best Value: {global_best_value:.2e}")

        time.sleep(0.1)

        if not running:
            break

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    try:
        max_iterations = int(input("Enter the number of iterations you want to see: "))
    except ValueError:
        print("Please enter a valid integer for the number of iterations.")
        exit()

    dimensions = 2
    bounds = (-100, 100)
    num_particles = 30
    screen_size = (800, 600)

    target_position = [random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])]
    print(f"Target is at: {target_position}")

    pso_visualization(dimensions, bounds, num_particles, max_iterations, screen_size, target_position)