
import numpy as np
from optimizer import create_empty_solution, set_spacecraft, set_phase

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
