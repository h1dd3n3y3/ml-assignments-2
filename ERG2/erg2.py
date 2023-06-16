# Run result for given input:
'''
Enter number of items: 10
Enter value for item 1: 60
Enter weight for item 1: 10
Enter value for item 2: 100
Enter weight for item 2: 20
Enter value for item 3: 120
Enter weight for item 3: 30
Enter value for item 4: 140
Enter weight for item 4: 40
Enter value for item 5: 160
Enter weight for item 5: 50
Enter value for item 6: 180
Enter weight for item 6: 10
Enter value for item 7: 200
Enter weight for item 7: 20
Enter value for item 8: 220
Enter weight for item 8: 30
Enter value for item 9: 240
Enter weight for item 9: 40
Enter value for item 10: 260
Enter weight for item 10: 50
Best solution: [0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
'''

import random

def create_particle(num_items):
    position = [random.randint(0, 1) for _ in range(num_items)]
    velocity = [0] * num_items
    best_position = position.copy()
    return position, velocity, best_position

def update_particle_velocity(particle, best_position, global_best_position):
    inertia_weight = 0.3
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


'''
Ready example (uncomment to run):

num_particles = 750
num_items = 10
max_weight = 50
max_iterations = 100
items = [
    [60, 10], [100, 20], [120, 30], [140, 40], [160, 50],
    [180, 10], [200, 20], [220, 30], [240, 40], [260, 50]
]
'''

num_particles = 750
num_items = int(input("Enter number of items: "))
max_weight = int(input("Enter maximum weight: "))
max_iterations = 100
items = []

for i in range(num_items):
    value = int(input(f"Enter value for item {i+1}: "))
    weight = int(input(f"Enter weight for item {i+1}: "))
    items.append([value, weight])

solution = run_pso(num_particles, num_items, max_weight, items, max_iterations)
print("Best solution:", solution)
