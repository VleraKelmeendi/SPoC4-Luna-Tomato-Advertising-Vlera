
import numpy as np

from lta_udp import celestial_morse_code
from optimizer import (
    improve_phases,
    improve_orbits,
    improve_spacecraft_count,
    evaluate_solution
)

udp = celestial_morse_code()

best_solution = np.load("results/best_solution.npy")

print("\n--- CURRENT BEST SOLUTION ---")
evaluate_solution(udp, best_solution)

best_fitness = udp.fitness(
    best_solution, postprocess=True
)[0][0]

# Perserisim optimizimin e fazave 3 here
for iteration in range(1):
    print(f"\n--- PHASE OPTIMIZATION {iteration + 1}/3 ---")

    improved_solution = improve_phases(
        udp, best_solution, trials=2
    )

    new_fitness = udp.fitness(
        improved_solution, postprocess=True
    )[0][0]

    if new_fitness < best_fitness:
        best_solution = improved_solution.copy()
        best_fitness = new_fitness
        np.save("results/best_solution.npy", best_solution)
        print("New best phase solution saved!")
    else:
        print("Previous best solution preserved!")

    evaluate_solution(udp, best_solution)

# Orbit optimization
print("\n--- ORBIT OPTIMIZATION ---")

improved_solution = improve_orbits(
    udp, best_solution, trials=10
)

new_fitness = udp.fitness(
    improved_solution, postprocess=True
)[0][0]

if new_fitness < best_fitness:
    best_solution = improved_solution.copy()
    best_fitness = new_fitness
    np.save("results/best_solution.npy", best_solution)
    print("New best orbit solution saved!")
else:
    print("Previous best solution preserved!")

# Spacecraft optimization
print("\n--- SPACECRAFT COUNT OPTIMIZATION ---")

improved_solution = improve_spacecraft_count(
    udp, best_solution, trials=3
)

new_fitness = udp.fitness(
    improved_solution, postprocess=True
)[0][0]

if new_fitness < best_fitness:
    best_solution = improved_solution.copy()
    best_fitness = new_fitness
    np.save("results/best_solution.npy", best_solution)
    print("New best spacecraft solution saved!")
else:
    print("Previous best solution preserved!")

print("\n--- FINAL RESULT ---")
evaluate_solution(udp, best_solution)

print("\nBest solution saved in results/best_solution.npy")
