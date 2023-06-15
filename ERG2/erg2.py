import random

def create_particle(num_items):
    position = [random.randint(0, 1) for _ in range(num_items)]
    velocity = [0] * num_items
    best_position = position.copy()
    return position, velocity, best_position

def update_particle_velocity(particle, best_position, global_best_position):
    inertia_weight = 0.7
    cognitive_weight = 1.4
    social_weight = 1.4

    for i in range(len(particle[0])):
        r1 = random.random()
        r2 = random.random()

        cognitive_velocity = cognitive_weight * r1 * (particle[2][i] - particle[0][i])
        social_velocity = social_weight * r2 * (global_best_position[i] - particle[0][i])
        particle[1][i] = inertia_weight * particle[1][i] + cognitive_velocity + social_velocity

def update_particle_position(particle):
    for i in range(len(particle[0])):
        if random.random() < sigmoid(particle[1][i]):
            particle[0][i] = 1
        else:
            particle[0][i] = 0

def sigmoid(x):
    return 1 / (1 + pow(2.71828, -x))

def evaluate_fitness(position, items, max_weight):
    total_value = 0
    total_weight = 0

    for i in range(len(position)):
        if position[i] == 1:
            total_value += items[i][0]
            total_weight += items[i][1]

    if total_weight > max_weight:
        return 0
    else:
        return total_value

def update_global_best_position(particles, items, max_weight):
    global_best_position = [0] * len(particles[0][0])
    best_fitness = evaluate_fitness(particles[0][0], items, max_weight)

    for particle in particles:
        fitness = evaluate_fitness(particle[0], items, max_weight)
        
        if fitness > best_fitness:
            best_fitness = fitness
            global_best_position = particle[0].copy()

    return global_best_position

def run_pso(num_particles, num_items, max_weight, items, max_iterations):
    particles = [create_particle(num_items) for _ in range(num_particles)]
    global_best_position = update_global_best_position(particles, items, max_weight)

    for _ in range(max_iterations):
        for particle in particles:
            update_particle_velocity(particle, particle[2], global_best_position)
            update_particle_position(particle)

        global_best_position = update_global_best_position(particles, items, max_weight)

    return global_best_position


# Example usage
num_particles = 20
num_items = 10
max_weight = 50
items = [
    [60, 10], [100, 20], [120, 30], [140, 40], [160, 50],
    [180, 10], [200, 20], [220, 30], [240, 40], [260, 50]
]

solution = run_pso(num_particles, num_items, max_weight, items, 100)

print("Best solution:", solution)
