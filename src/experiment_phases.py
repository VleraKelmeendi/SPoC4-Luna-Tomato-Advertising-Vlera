
import numpy as np
from optimizer import create_empty_solution, set_spacecraft, set_phase
from lta_udp import celestial_morse_code

udp = celestial_morse_code()

# Top 10 orbits from Experiment 3
orbit_indices = [162, 155, 399, 402, 403, 404, 408, 184, 377, 409]

# Test 8 different phases
phases = np.linspace(0, 2 * np.pi, 8, endpoint=False)

results = []

for orbit_index in orbit_indices:
    best_mse = float("inf")
    best_phase = None

    for phase in phases:
        solution = create_empty_solution(udp.num_orbits)

        set_spacecraft(solution, orbit_index, 1)
        set_phase(solution, orbit_index, 0, phase)

        result = udp.fitness(solution, postprocess=True)
        mse = result[2]

        if mse < best_mse:
            best_mse = mse
            best_phase = phase

    results.append((orbit_index, best_mse, best_phase))

results.sort(key=lambda item: item[1])

print("\n--- Best orbits after phase optimization ---")

for orbit_index, mse, phase in results:
    print(
        f"Orbit {orbit_index}: "
        f"MSE = {mse:.6f}, "
        f"Phase = {phase:.4f}"
    )
