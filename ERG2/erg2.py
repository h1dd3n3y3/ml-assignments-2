import numpy as np, pyswarms as ps

def evaluate_fitness(positions, num_items, max_weight, items):
    total_value = np.dot(positions, items[:, 0]) # Dot product of positions and items value (first column)
    total_weight = np.dot(positions, items[:, 1]) # Dot product of positions and items weight (second column)

    if np.any(total_weight > max_weight): # If any of the total weights are greater than the maximum weight
        return 0
    else: # Else
        return total_value

def optimize_knapsack(num_items, max_weight, items, num_particles, max_iterations):
    bounds = (np.zeros(num_items), np.ones(num_items)) # Bounds for each item (0 or 1)

    def objective_function(positions):
        return -evaluate_fitness(positions, num_items, max_weight, items) # Return negative fitness

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9} # Opions for optimizer
    optimizer = ps.single.GlobalBestPSO(n_particles=num_particles, dimensions=num_items, options=options, bounds=bounds) # Initialize optimizer
    best_position, best_fitness = optimizer.optimize(objective_function, iters=max_iterations) # Optimize

    return best_position

num_items = int(input("Enter number of items: ")) # Number of items to choose from
max_weight = int(input("Enter maximum weight: ")) # Maximum weight that the knapsack can hold
items = np.empty((0, 2), int) # Declare empty array to store items

for i in range(num_items): # In range of number of items
    value = int(input("Enter value of item " + str(i) + ": ")) # Ask user for value of item
    weight = int(input("Enter weight of item " + str(i) + ": ")) # Ask user for weight of item
    items = np.append(items, [[value, weight]], axis=0) # Append value and weight to items array

print("Best solution:", optimize_knapsack(num_items, max_weight, items, num_particles=20, max_iterations=100))
