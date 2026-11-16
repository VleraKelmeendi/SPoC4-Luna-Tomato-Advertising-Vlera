
import numpy as np
from itertools import product
from optimizer import create_empty_solution, set_spacecraft, set_phase
from lta_udp import celestial_morse_code

udp = celestial_morse_code()

# Five best orbits and their best phases
orbit_indices = [162, 399, 408, 409, 402]
best_phases = [
    0,
    np.pi,
    7 * np.pi / 4,
    3 * np.pi / 2,
    7 * np.pi / 4
]

best_mse = float("inf")
best_combo = None

# Test every pair of these five orbits
for i, j in product(range(5), repeat=2):
    if i >= j:
        continue

    solution = create_empty_solution(udp.num_orbits)

    for index in [i, j]:
        orbit = orbit_indices[index]
        phase = best_phases[index]

        set_spacecraft(solution, orbit, 1)
        set_phase(solution, orbit, 0, phase)

    result = udp.fitness(solution, postprocess=True)
    mse = result[2]

    if mse < best_mse:
        best_mse = mse
        best_combo = (orbit_indices[i], orbit_indices[j])

print("Best pair:", best_combo)
print("Best MSE:", best_mse)
