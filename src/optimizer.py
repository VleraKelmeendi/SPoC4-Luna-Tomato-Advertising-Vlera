import numpy as np

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

    num_orbits = 779

    if number < 0 or number > MAX_PER_ORBIT:
        raise ValueError("Number of spacecraft must be between 0 and 5.")

    if orbit_index < 0 or orbit_index >= num_orbits:
        raise IndexError("Invalid orbit index.")

    solution[orbit_index] = number

    return solution