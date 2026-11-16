from optimizer import create_empty_solution
from lta_udp import celestial_morse_code

# Initialize the official evaluator
udp = celestial_morse_code()

# Create an empty solution
solution = create_empty_solution(udp.num_orbits)

# Evaluate the solution
result = udp.fitness(solution, postprocess=True)

print("Number of orbits:", udp.num_orbits)
print("Objective:", result[0])
print("Selected spacecraft:", result[1])
print("MSE:", result[2])