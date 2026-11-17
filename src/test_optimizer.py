
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
    create_seeded_solution
)


# 1. Krijojme UDP
udp = celestial_morse_code()

# 2. Testojme krijimin e zgjidhjes bosh
num_orbits = udp.num_orbits

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


# 5. Testojme Simulated Annealing
print("\n--- SIMULATED ANNEALING ---")

best = simulated_annealing(
    udp,
    iterations=100,
    initial_temperature=10,
    cooling_rate=0.999
)

print("Best solution size:", len(best))
print(
    "Best spacecraft:",
    int(np.sum(best[:num_orbits]))
)

evaluate_solution(udp, best)


# 6. Ruajme zgjidhjen me te mire
np.save("results/best_solution.npy", best)

print("\nBest solution saved successfully!")


# 7. Testojme nese zgjidhja u ruajt sakte
previous_best = np.load("results/best_solution.npy")

print("\n--- LOADED BEST SOLUTION ---")
evaluate_solution(udp, previous_best)


# 8. Testojme seeded solution
seeded = create_seeded_solution(udp)

print("\n--- SEEDED SOLUTION ---")
evaluate_solution(udp, seeded)
