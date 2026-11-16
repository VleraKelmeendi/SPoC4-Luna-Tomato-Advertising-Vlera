import numpy as np
import random
import math

# Maximum number of spacecraft per orbit
MAX_PER_ORBIT = 5

# Allowed phase range
PHASE_MIN = 0.0
PHASE_MAX = 2 * np.pi


def create_empty_solution(num_orbits):
    """
    Create an initial solution with no selected spacecraft
    and all phases set to zero.
    """

    selections = np.zeros(num_orbits, dtype=int)

    phases = np.zeros(
        num_orbits * MAX_PER_ORBIT,
        dtype=float
    )

    solution = np.concatenate([selections, phases])

    return solution


def set_spacecraft(solution, orbit_index, number):
    """
    Set the number of spacecraft for a specific orbit.
    """

    num_orbits = len(solution) // (MAX_PER_ORBIT + 1)

    if number < 0 or number > MAX_PER_ORBIT:
        raise ValueError("Number of spacecraft must be between 0 and 5.")

    if orbit_index < 0 or orbit_index >= num_orbits:
        raise IndexError("Invalid orbit index.")

    solution[orbit_index] = number

    return solution


def set_phase(solution, orbit_index, spacecraft_index, phase):
    """
    Set the phase of a spacecraft in a specific orbit.
    """

    num_orbits = len(solution) // (MAX_PER_ORBIT + 1)

    if orbit_index < 0 or orbit_index >= num_orbits:
        raise IndexError("Invalid orbit index.")

    if spacecraft_index < 0 or spacecraft_index >= solution[orbit_index]:
        raise IndexError("This spacecraft has not been selected.")

    if phase < PHASE_MIN or phase >= PHASE_MAX:
        raise ValueError("Phase must be between 0 and 2*pi.")

    phase_index = (
        num_orbits
        + orbit_index * MAX_PER_ORBIT
        + spacecraft_index
    )

    solution[phase_index] = phase

    return solution


def evaluate_solution(udp, solution):
    result = udp.fitness(solution, postprocess=True)

    objective = result[0]
    spacecraft = result[1]
    mse = result[2]

    print("Spacecraft:", spacecraft)
    print("MSE:", mse)
    print("Objective:", objective)

    return mse



def create_random_solution(udp, num_spacecraft=50):
    solution = create_empty_solution(udp.num_orbits)

    for _ in range(num_spacecraft):
        orbit = random.randrange(udp.num_orbits)

        if solution[orbit] < MAX_PER_ORBIT:
            spacecraft_index = int(solution[orbit])

            set_spacecraft(solution, orbit, spacecraft_index + 1)

            phase = random.uniform(PHASE_MIN, PHASE_MAX)
            set_phase(solution, orbit, spacecraft_index, phase)

    return solution


def create_neighbor(solution, udp):
    new_solution = solution.copy()

    orbit = random.randrange(udp.num_orbits)
    number = int(new_solution[orbit])

    if number == 0:
        set_spacecraft(new_solution, orbit, 1)
        set_phase(
            new_solution,
            orbit,
            0,
            random.uniform(PHASE_MIN, PHASE_MAX)
        )

    elif number < MAX_PER_ORBIT:
        set_spacecraft(new_solution, orbit, number + 1)
        set_phase(
            new_solution,
            orbit,
            number,
            random.uniform(PHASE_MIN, PHASE_MAX)
        )

    else:
        set_spacecraft(new_solution, orbit, number - 1)

    return new_solution