
import numpy as np
from optimizer import create_empty_solution, set_spacecraft, set_phase
import numpy as np
from optimizer import evaluate_solution

num_orbits = 779

# 1. Create an empty solution
solution = create_empty_solution(num_orbits)

# 2. Select 2 spacecraft in orbit 10
set_spacecraft(solution, 10, 2)

# 3. Set the phase of the first spacecraft
set_phase(solution, 10, 0, np.pi / 2)

# 4. Check the results
print("Total solution size:", len(solution))
print("Spacecraft in orbit 10:", solution[10])
print("Phase of first spacecraft:", solution[num_orbits + 10 * 5])
print("Tests completed!")


from lta_udp import celestial_morse_code
from optimizer import create_random_solution

udp = celestial_morse_code()

solution = create_random_solution(udp, num_spacecraft=50)

print("Solution size:", len(solution))
print("Selected spacecraft:", int(np.sum(solution[:udp.num_orbits])))

evaluate_solution(udp, solution)


from optimizer import create_neighbor

neighbor = create_neighbor(solution, udp)

print("Original spacecraft:", int(np.sum(solution[:udp.num_orbits])))
print("Neighbor spacecraft:", int(np.sum(neighbor[:udp.num_orbits])))

print("Original MSE:", udp.fitness(solution, postprocess=True)[2])
print("Neighbor MSE:", udp.fitness(neighbor, postprocess=True)[2])