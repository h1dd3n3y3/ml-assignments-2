import numpy as np
import pyswarms as ps

def evaluate_fitness(positions, num_items, max_weight, items):
    total_value = np.dot(positions, items[:, 0])
    total_weight = np.dot(positions, items[:, 1])

    if np.any(total_weight > max_weight):
        return 0
    else:
        return total_value

def optimize_knapsack(num_items, max_weight, items, num_particles, max_iterations):
    bounds = (np.zeros(num_items), np.ones(num_items))

    def objective_function(positions):
        return -evaluate_fitness(positions, num_items, max_weight, items)

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}  # Set your preferred options here

    optimizer = ps.single.GlobalBestPSO(n_particles=num_particles, dimensions=num_items, options=options, bounds=bounds)
    best_position, best_fitness = optimizer.optimize(objective_function, iters=max_iterations)

    return best_position

num_items = int(input("Enter number of items: "))
max_weight = int(input("Enter maximum weight: "))
items = np.empty((0, 2), int)

for i in range(num_items):
    value = int(input("Enter value of item " + str(i) + ": "))
    weight = int(input("Enter weight of item " + str(i) + ": "))
    items = np.append(items, [[value, weight]], axis=0)

best_solution = optimize_knapsack(num_items, max_weight, items, num_particles=20, max_iterations=100)
print("Best solution:", best_solution)
