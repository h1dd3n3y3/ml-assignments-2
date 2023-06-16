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

def create_particle(num_items): # Create particle
    position = [random.randint(0, 1) for _ in range(num_items)]
    velocity = [0] * num_items
    best_position = position.copy()

    return position, velocity, best_position

def update_particle_velocity(particle, best_position, global_best_position): # Update particle velocity
    inertia_weight = 0.3  # Inertia weight
    cognitive_weight = 1.4 # Cognitive weight
    social_weight = 1.4 # Social weight

    for i in range(len(particle[0])): # For each item
        r1 = random.random() # Random number between 0 and 1
        r2 = random.random() # Random number between 0 and 1

        cognitive_velocity = cognitive_weight * r1 * (particle[2][i] - particle[0][i]) # Cognitive velocity
        social_velocity = social_weight * r2 * (global_best_position[i] - particle[0][i]) # Social velocity
        particle[1][i] = inertia_weight * particle[1][i] + cognitive_velocity + social_velocity # Update velocity

def update_particle_position(particle): # Update particle position
    for i in range(len(particle[0])): # For each item
        if random.random() < sigmoid(particle[1][i]): # If random number is less than sigmoid of velocity
            particle[0][i] = 1
        else:
            particle[0][i] = 0 

def sigmoid(x): # Sigmoid function for particle position update
    return 1 / (1 + pow(2.71828, -x)) # 2.71828 = Euler's number

def evaluate_fitness(position, items, max_weight): # Particle fitness evaluation
    total_value = 0 # Initialize total value to 0
    total_weight = 0 # Initialize total weight to 0

    for i in range(len(position)): # For each item
        if position[i] == 1: # If item is in the knapsack
            total_value += items[i][0] # Add item's value to total value
            total_weight += items[i][1] # Add item's weight to total weight

    if total_weight > max_weight: # If total weight exceeds maximum weight
        return 0 
    else: # Else
        return total_value

def update_global_best_position(particles, items, max_weight): # Update global best position
    global_best_position = [0] * len(particles[0][0]) # Initialize global best position to 0
    best_fitness = evaluate_fitness(particles[0][0], items, max_weight) # Initialize best fitness to first particle's fitness

    for particle in particles: # For each particle
        fitness = evaluate_fitness(particle[0], items, max_weight) # Evaluate fitness
        
        if fitness > best_fitness:  # If fitness is better than best fitness
            best_fitness = fitness  # Update best fitness
            global_best_position = particle[0].copy() # Update global best position

    return global_best_position

def run_pso(num_particles, num_items, max_weight, items, max_iterations): # Run PSO function
    particles = [create_particle(num_items) for _ in range(num_particles)] # Create particles
    global_best_position = update_global_best_position(particles, items, max_weight) # Initialize global best position

    for i in range(max_iterations): # In range of maximum iterations
        for particle in particles: # For each particle
            update_particle_velocity(particle, particle[2], global_best_position) # Update particle velocity
            update_particle_position(particle) # Update particle position

        global_best_position = update_global_best_position(particles, items, max_weight) # Update global best position

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

num_particles = 750 # Number of particles
num_items = int(input("Enter number of items: ")) # Prompt user for number of items
max_weight = int(input("Enter maximum weight: ")) # Prompt user for maximum weight
max_iterations = 100 # Maximum iterations
items = []

for i in range(num_items): # For each item
    value = int(input(f"Enter value for item {i+1}: ")) # Prompt user for item value
    weight = int(input(f"Enter weight for item {i+1}: ")) # Prompt user for item weight
    items.append([value, weight]) # Append item to items list

solution = run_pso(num_particles, num_items, max_weight, items, max_iterations) # Run PSO function
print("Best solution:", solution)
