
import numpy as np

from src.lta_udp import celestial_morse_code
from src.optimizer import simulated_annealing, evaluate_solution

# Ngarkojme evaluatorin
udp = celestial_morse_code()

# Ngarkojme zgjidhjen me te mire
best_solution = np.load("results/best_solution.npy")

print("\n--- BEFORE ANNEALING ---")
evaluate_solution(udp, best_solution)

# Testojme simulated annealing
improved_solution = simulated_annealing(
    udp,
    initial_temperature=5,
    cooling_rate=0.995,
    iterations=100,
    initial_solution=best_solution
)

print("\n--- AFTER ANNEALING ---")
evaluate_solution(udp, improved_solution)

# E ruajme vetem nese eshte me e mire
old_fitness = udp.fitness(best_solution, postprocess=True)[0][0]
new_fitness = udp.fitness(improved_solution, postprocess=True)[0][0]

if new_fitness < old_fitness:
    np.save("results/best_solution.npy", improved_solution)
    print("\nNew best solution saved!")
else:
    print("\nPrevious best solution preserved!")
