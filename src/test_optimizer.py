
import numpy as np
from itertools import product
from optimizer import create_empty_solution, set_spacecraft, set_phase
from lta_udp import celestial_morse_code

udp = celestial_morse_code()

orbit_indices = [0, 188, 479]
phases = [0, np.pi / 2, np.pi, 3 * np.pi / 2]

best_mse = float("inf")
best_phases = None

for phase_combo in product(phases, repeat=3):
    solution = create_empty_solution(udp.num_orbits)

    for orbit_index, phase in zip(orbit_indices, phase_combo):
        set_spacecraft(solution, orbit_index, 1)
        set_phase(solution, orbit_index, 0, phase)

    result = udp.fitness(solution, postprocess=True)
    mse = result[2]

    if mse < best_mse:
        best_mse = mse
        best_phases = phase_combo

print("Best MSE:", best_mse)
print("Best phases:", best_phases)
