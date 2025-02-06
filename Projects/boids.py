import pygame as p
import random
import math

# Screen dimensions
WIDTH, HEIGHT = 1300, 700
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Boids Simulation")
p.init()

# Boid parameters
NUM_BOIDS = 150
VISUAL_RANGE = 75
SPEED_LIMIT = 10
MARGIN = 80
TURN_FACTOR = 1
CENTERING_FACTOR = 0.005
AVOID_FACTOR = 0.05
MATCHING_FACTOR = 0.05
MIN_DISTANCE = 20


# Boids data structure
boids = []


def init_boids():
    for _ in range(NUM_BOIDS):

        boids.append({
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "dx": random.uniform(-5, 5),
            "dy": random.uniform(-5, 5),
            "random_color" : (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        })


def distance(boid1, boid2):
    return math.sqrt((boid1["x"] - boid2["x"]) ** 2 + (boid1["y"] - boid2["y"]) ** 2)


def fly_towards_center(boid):
    center_x, center_y, count = 0, 0, 0
    for other in boids:
        if distance(boid, other) < VISUAL_RANGE:
            center_x += other["x"]
            center_y += other["y"]
            count += 1
    if count > 0:
        center_x /= count
        center_y /= count
        boid["dx"] += (center_x - boid["x"]) * CENTERING_FACTOR
        boid["dy"] += (center_y - boid["y"]) * CENTERING_FACTOR


def avoid_others(boid):
    move_x, move_y = 0, 0
    for other in boids:
        if other != boid and distance(boid, other) < MIN_DISTANCE:
            move_x += boid["x"] - other["x"]
            move_y += boid["y"] - other["y"]
    boid["dx"] += move_x * AVOID_FACTOR
    boid["dy"] += move_y * AVOID_FACTOR


def match_velocity(boid):
    avg_dx, avg_dy, count = 0, 0, 0
    for other in boids:
        if distance(boid, other) < VISUAL_RANGE:
            avg_dx += other["dx"]
            avg_dy += other["dy"]
            count += 1
    if count > 0:
        avg_dx /= count
        avg_dy /= count
        boid["dx"] += (avg_dx - boid["dx"]) * MATCHING_FACTOR
        boid["dy"] += (avg_dy - boid["dy"]) * MATCHING_FACTOR


def limit_speed(boid):
    speed = math.sqrt(boid["dx"] ** 2 + boid["dy"] ** 2)
    if speed > SPEED_LIMIT:
        boid["dx"] = (boid["dx"] / speed) * SPEED_LIMIT
        boid["dy"] = (boid["dy"] / speed) * SPEED_LIMIT


def keep_within_bounds(boid):
    if boid["x"] < MARGIN:
        boid["dx"] += TURN_FACTOR
    if boid["x"] > WIDTH - MARGIN:
        boid["dx"] -= TURN_FACTOR
    if boid["y"] < MARGIN:
        boid["dy"] += TURN_FACTOR
    if boid["y"] > HEIGHT - MARGIN:
        boid["dy"] -= TURN_FACTOR


def draw_boid(ctx, boid):
    angle = math.atan2(boid["dy"], boid["dx"])
    size = 10  # Size of the boid
    points = [
        (boid["x"] + math.cos(angle) * size, boid["y"] + math.sin(angle) * size),
        (boid["x"] - math.cos(angle) * size * 0.5 - math.sin(angle) * size * 0.5,
         boid["y"] - math.sin(angle) * size * 0.5 + math.cos(angle) * size * 0.5),
        (boid["x"] - math.cos(angle) * size * 0.5 + math.sin(angle) * size * 0.5,
         boid["y"] - math.sin(angle) * size * 0.5 - math.cos(angle) * size * 0.5)
    ]
    
    p.draw.polygon(ctx, (255, 255, 255), points)

# Main loop
def animation_loop():
    running = True
    clock = p.time.Clock()

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        # Update each boid
        for boid in boids:
            fly_towards_center(boid)
            avoid_others(boid)
            match_velocity(boid)
            limit_speed(boid)
            keep_within_bounds(boid)
            boid["x"] += boid["dx"]
            boid["y"] += boid["dy"]

        # Draw everything
        screen.fill((0,0,0))
        for boid in boids:
            draw_boid(screen, boid)
        p.display.flip()
        clock.tick(60)

    p.quit()


# Initialize and run
init_boids()
animation_loop()