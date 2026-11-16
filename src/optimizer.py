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
