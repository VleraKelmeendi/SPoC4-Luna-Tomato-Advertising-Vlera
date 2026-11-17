
import numpy as np
from src.lta_udp import celestial_morse_code

udp = celestial_morse_code()
solution = np.load("results/best_solution.npy")

result = udp.fitness(solution, postprocess=True)

print("FINAL VERIFICATION")
print("Objective:", result[0])
print("Spacecraft:", result[1])
print("MSE:", result[2])

assert result[2] <= 0.05, "MSE threshold not reached!"
print("SUCCESS: Solution is feasible!")
