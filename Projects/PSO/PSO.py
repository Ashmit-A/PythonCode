import random

class Particle:
    def __init__(self, dimensions, bounds):
        self.position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
        self.velocity = [random.uniform(-1, 1) for _ in range(dimensions)]
        self.best_position = self.position[:]
        self.best_value = float('inf')
        self.current_value = float('inf')

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


def pso(objective_function, dimensions, bounds, num_particles, max_iterations, inertia=0.7, cognitive=1.5, social=1.5):
    particles = [Particle(dimensions, bounds) for _ in range(num_particles)]
    global_best_position = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
    global_best_value = float('inf')

    for iteration in range(max_iterations):
        for particle in particles:
            particle.current_value = objective_function(particle.position)

            if particle.current_value < particle.best_value:
                particle.best_value = particle.current_value
                particle.best_position = particle.position[:]

            if particle.current_value < global_best_value:
                global_best_value = particle.current_value
                global_best_position = particle.position[:]

        for particle in particles:
            particle.update_velocity(global_best_position, inertia, cognitive, social)
            particle.update_position(bounds)

        print(f"Iteration {iteration + 1}/{max_iterations}, Best Value: {global_best_value}")

    return global_best_position, global_best_value


def sphere_function(position):
    return sum(x**2 for x in position)


if __name__ == "__main__":
    dimensions = 3
    bounds = (-10, 10)
    num_particles = 30
    max_iterations = int(input("Enter number of iterations:"))

    best_position, best_value = pso(sphere_function, dimensions, bounds, num_particles, max_iterations)

    print("\nBest Position:", best_position)
    print("Best Value:", best_value)
