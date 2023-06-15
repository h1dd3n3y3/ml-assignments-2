import random
import numpy as np, pyswarms as ps

def evaluate_fitness(positions, num_items, max_weight, items):
    total_value = 0
    total_weight = 0

    for i in range(num_items):
        if positions[i] == 1:
            total_value += items[i][0]
            total_weight += items[i][1]

    if total_weight > max_weight:
        return 0
    else:
        return total_value

def optimize_knapsack(num_items, max_weight, items, num_particles, max_iterations):
    bounds = (np.zeros(num_items), np.ones(num_items))

    def objective_function(positions):
        return -evaluate_fitness(positions, num_items, max_weight, items)

    optimizer = ps.single.GlobalBestPSO(n_particles=num_particles, dimensions=num_items, bounds=bounds)
    best_position, best_fitness = optimizer.optimize(objective_function, iters=max_iterations)

    return best_position

num_items = 10
max_weight = 50
items = [
    [60, 10], [100, 20], [120, 30], [140, 40], [160, 50],
    [180, 10], [200, 20], [220, 30], [240, 40], [260, 50]
]

best_solution = optimize_knapsack(num_items, max_weight, items, num_particles=20, max_iterations=100)

print("Best solution:", best_solution)
