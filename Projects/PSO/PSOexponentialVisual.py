import numpy as np
import pygame

def rastrigin(x):
    """Rastrigin function for optimization testing."""
    return 10 * len(x) + sum(x**2 - 10 * np.cos(2 * np.pi * x))

class ExponentialPSO:
    def __init__(self, num_particles, dim, bounds, max_iter, w_max=0.9, w_min=0.4, c1=2.0, c2=2.0, lambda_decay=0.02):
        self.num_particles = num_particles
        self.dim = dim
        self.bounds = np.array(bounds)
        self.max_iter = max_iter
        self.w_max = w_max
        self.w_min = w_min
        self.c1 = c1
        self.c2 = c2
        self.lambda_decay = lambda_decay
        
        # Initialize particles
        self.positions = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (num_particles, dim))
        self.velocities = np.random.uniform(-1, 1, (num_particles, dim))
        self.personal_best_positions = np.copy(self.positions)
        self.personal_best_scores = np.array([rastrigin(p) for p in self.positions])
        
        # Initialize global best
        best_idx = np.argmin(self.personal_best_scores)
        self.global_best_position = np.copy(self.personal_best_positions[best_idx])
        self.global_best_score = self.personal_best_scores[best_idx]
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("PSO Visualization")
        self.clock = pygame.time.Clock()
    
    def optimize(self):
        for t in range(self.max_iter):
            w = self.w_max * np.exp(-self.lambda_decay * t)  # Exponential decay of inertia weight
            
            for i in range(self.num_particles):
                r1, r2 = np.random.rand(self.dim), np.random.rand(self.dim)
                cognitive = self.c1 * r1 * (self.personal_best_positions[i] - self.positions[i])
                social = self.c2 * r2 * (self.global_best_position - self.positions[i])
                self.velocities[i] = w * self.velocities[i] + cognitive + social
                self.positions[i] += self.velocities[i]
                
                # Clamp positions within bounds
                self.positions[i] = np.clip(self.positions[i], self.bounds[:, 0], self.bounds[:, 1])
                
                # Evaluate fitness
                score = rastrigin(self.positions[i])
                
                # Update personal best
                if score < self.personal_best_scores[i]:
                    self.personal_best_scores[i] = score
                    self.personal_best_positions[i] = np.copy(self.positions[i])
                
            # Update global best
            best_idx = np.argmin(self.personal_best_scores)
            if self.personal_best_scores[best_idx] < self.global_best_score:
                self.global_best_score = self.personal_best_scores[best_idx]
                self.global_best_position = np.copy(self.personal_best_positions[best_idx])
                
            print(f"Iteration {t+1}/{self.max_iter} - Best Score: {self.global_best_score:.6f}")
            
            # Visualization
            self.screen.fill((0, 0, 0))
            for pos in self.positions:
                x, y = int((pos[0] - self.bounds[0][0]) * 500 / (self.bounds[0][1] - self.bounds[0][0])), \
                       int((pos[1] - self.bounds[1][0]) * 500 / (self.bounds[1][1] - self.bounds[1][0]))
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 3)
            pygame.display.flip()
            self.clock.tick(10)
        
        pygame.quit()
        return self.global_best_position, self.global_best_score

# Usage
bounds = [(-5.12, 5.12)] * 2  # 2D problem within [-5.12, 5.12] range
pso = ExponentialPSO(num_particles=30, dim=2, bounds=bounds, max_iter=100)
best_position, best_score = pso.optimize()
print(f"Optimal Solution: {best_position}, Score: {best_score}")
