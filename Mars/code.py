import pygame
import heapq
from opensimplex import OpenSimplex

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 4
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN_BASE = (139, 69, 19)

# Initialize OpenSimplex noise generator
tmp = OpenSimplex(seed=420)

# Generate a structured topological map using OpenSimplex noise
# It returns height values as gradients and marks boundaries

def generate_topology():
    scale = 10.0
    topology = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            height = int((tmp.noise2(x / scale, y / scale) + 1) * 5)
            row.append(height)
        topology.append(row)
    return topology

# Generate structured weather hazards using OpenSimplex noise
def generate_weather_hazards():
    scale = 15.0
    return [[1 if tmp.noise2(x / scale, y / scale) > 0.4 else 0 for x in range(COLS)] for y in range(ROWS)]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                tentative_g_score = g_score[current] + 1 + grid[neighbor[0]][neighbor[1]]
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# Setup Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mars Rover Path Detection")

topology = generate_topology()
weather = generate_weather_hazards()
start, goal = (0, 0), (ROWS - 1, COLS - 1)
path = astar_search(topology, start, goal)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            height = topology[y][x]
            color = (BROWN_BASE[0] - height * 5, BROWN_BASE[1] - height * 3, BROWN_BASE[2] - height * 2)
            if topology[y][x] > 7:  # Marking boundaries
                color = BLACK
            if weather[y][x]:
                color = BLUE
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for (x, y) in path:
        pygame.draw.rect(screen, GREEN, (y * GRID_SIZE, x * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (start[1] * GRID_SIZE, start[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, BLACK, (goal[1] * GRID_SIZE, goal[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
