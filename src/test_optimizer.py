
import numpy as np

from lta_udp import celestial_morse_code

from optimizer import (
    create_empty_solution,
    set_spacecraft,
    set_phase,
    evaluate_solution,
    create_random_solution,
    create_neighbor,
    simulated_annealing,
    create_seeded_solution,
    improve_phases
)

import os
os.makedirs("results", exist_ok=True)
# 1. Krijojme UDP
udp = celestial_morse_code()
num_orbits = udp.num_orbits


# 2. Testojme krijimin e zgjidhjes bosh
solution = create_empty_solution(num_orbits)

set_spacecraft(solution, 10, 2)
set_phase(solution, 10, 0, np.pi / 2)

print("\n--- BASIC TEST ---")
print("Total solution size:", len(solution))
print("Spacecraft in orbit 10:", solution[10])
print(
    "Phase of first spacecraft:",
    solution[num_orbits + 10 * 5]
)
print("Tests completed!")


# 3. Testojme zgjidhjen random
random_solution = create_random_solution(
    udp,
    num_spacecraft=50
)

print("\n--- RANDOM SOLUTION ---")
print(
    "Selected spacecraft:",
    int(np.sum(random_solution[:num_orbits]))
)

evaluate_solution(udp, random_solution)


# 4. Testojme krijimin e neighbor
neighbor = create_neighbor(random_solution, udp)

print("\n--- NEIGHBOR TEST ---")
print(
    "Original spacecraft:",
    int(np.sum(random_solution[:num_orbits]))
)
print(
    "Neighbor spacecraft:",
    int(np.sum(neighbor[:num_orbits]))
)

print(
    "Original MSE:",
    udp.fitness(random_solution, postprocess=True)[2]
)
print(
    "Neighbor MSE:",
    udp.fitness(neighbor, postprocess=True)[2]
)


# 5. Ngarkojme zgjidhjen me te mire
print("\n--- SIMULATED ANNEALING ---")

try:
    previous_best = np.load("results/best_solution.npy")
    print("Previous best solution loaded!")

except FileNotFoundError:
    previous_best = create_seeded_solution(udp)
    print("Starting from seeded solution!")


# 6. Ekzekutojme Simulated Annealing
best = simulated_annealing(
    udp,
    initial_solution=previous_best,
    iterations=200,
    initial_temperature=5,
    cooling_rate=0.999
)


# 7. Krahasojme zgjidhjen e re me te vjetren
old_fitness = udp.fitness(
    previous_best, postprocess=True
)[0][0]

new_fitness = udp.fitness(
    best, postprocess=True
)[0][0]

print("\n--- BEST SOLUTION COMPARISON ---")
print("Previous fitness:", old_fitness)
print("New fitness:", new_fitness)

if new_fitness < old_fitness:
    best_solution = best
    print("New best solution found!")
else:
    best_solution = previous_best
    print("Previous best solution preserved!")


# 8. Ruajme zgjidhjen me te mire
np.save("results/best_solution.npy", best_solution)

print("\n--- FINAL BEST SOLUTION ---")
print(
    "Spacecraft:",
    int(np.sum(best_solution[:num_orbits]))
)

evaluate_solution(udp, best_solution)

print("\n--- PHASE OPTIMIZATION ---")

improved_solution = improve_phases(
    udp,
    best_solution,
    trials=3
)

old_fitness = udp.fitness(
    best_solution, postprocess=True
)[0][0]

new_fitness = udp.fitness(
    improved_solution, postprocess=True
)[0][0]

if new_fitness < old_fitness:
    best_solution = improved_solution
    np.save("results/best_solution.npy", best_solution)
    print("Phase optimization improved the solution!")
else:
    print("Previous best solution preserved!")

evaluate_solution(udp, best_solution)

print("\n--- SELECTED ORBITS AND PHASES ---")

for orbit in range(num_orbits):
    count = int(best_solution[orbit])

    for spacecraft_index in range(count):
        phase_index = (
            num_orbits
            + orbit * 5
            + spacecraft_index
        )

        phase = best_solution[phase_index]

        print(
            f"Orbit: {orbit}, "
            f"Spacecraft: {spacecraft_index}, "
            f"Phase: {phase:.6f}"
        )


# 9. Testojme seeded solution
seeded = create_seeded_solution(udp)

print("\n--- SEEDED SOLUTION ---")
evaluate_solution(udp, seeded)

np.save("results/best_solution.npy", best_solution)
print("BEST SOLUTION SAVED!")