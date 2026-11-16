
from optimizer import create_empty_solution, set_spacecraft, set_phase
from lta_udp import celestial_morse_code

udp = celestial_morse_code()

solution = create_empty_solution(udp.num_orbits)
set_spacecraft(solution, 0, 1)

phases_to_test = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]

for phase in phases_to_test:
    test_solution = solution.copy()
    set_phase(test_solution, 0, 0, phase)

    result = udp.fitness(test_solution, postprocess=True)

    print("Phase:", phase, "| MSE:", result[2])
