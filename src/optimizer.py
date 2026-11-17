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

    # Gjejme orbitat ku mund te bejme ndryshime
    counts = new_solution[:udp.num_orbits].astype(int)

    add_orbits = np.where(counts < MAX_PER_ORBIT)[0]
    remove_orbits = np.where(counts > 0)[0]

    # Zgjedhim nje operacion
    operation = random.choice(["add", "remove", "phase"])

    if operation == "add" and len(add_orbits) > 0:

        orbit = random.choice(add_orbits)
        number = int(new_solution[orbit])

        set_spacecraft(new_solution, orbit, number + 1)

        phase = random.random() * PHASE_MAX
        set_phase(new_solution, orbit, number, phase)

    elif operation == "remove" and len(remove_orbits) > 0:

        orbit = random.choice(remove_orbits)
        number = int(new_solution[orbit])

        set_spacecraft(new_solution, orbit, number - 1)

    else:
        if len(remove_orbits) > 0:

            orbit = random.choice(remove_orbits)
            number = int(new_solution[orbit])

            spacecraft_index = random.randrange(number)

            phase = random.random() * PHASE_MAX

            phase_index = (
                udp.num_orbits
                + orbit * MAX_PER_ORBIT
                + spacecraft_index
            )

            new_solution[phase_index] = phase

    return new_solution




def simulated_annealing(
    udp,
    num_spacecraft=50,
    initial_temperature=10,
    cooling_rate=0.999,
    iterations=300,
    initial_solution=None
):
    # Nese kemi zgjidhje paraprake, vazhdojme prej saj
    if initial_solution is None:
        current_solution = create_seeded_solution(udp)
    else:
        current_solution = initial_solution.copy()

    best_solution = current_solution.copy()

    current_fitness = udp.fitness(
        current_solution, postprocess=True
    )[0][0]

    best_fitness = current_fitness

    print("SA starting fitness:", current_fitness)

    temperature = initial_temperature

    for _ in range(iterations):

        neighbor = create_neighbor(current_solution, udp)

        neighbor_fitness = udp.fitness(
            neighbor, postprocess=True
        )[0][0]

        delta = neighbor_fitness - current_fitness

        if delta < 0:
            current_solution = neighbor
            current_fitness = neighbor_fitness

        else:
            probability = math.exp(-delta / temperature)

            if random.random() < probability:
                current_solution = neighbor
                current_fitness = neighbor_fitness

        if current_fitness < best_fitness:
            best_solution = current_solution.copy()
            best_fitness = current_fitness

        temperature *= cooling_rate

    print("SA best fitness:", best_fitness)

    return best_solution



def create_seeded_solution(udp):
    # Krijojme zgjidhje bosh
    solution = create_empty_solution(udp.num_orbits)

    # Orbitat dhe fazat nga eksperimentet tona
    selected_orbits = [
        (162, 0.0),
        (399, np.pi),
        (408, 5.4978)
    ]

    # Vendosim nga nje spacecraft ne secilen orbite
    for orbit, phase in selected_orbits:
        set_spacecraft(solution, orbit, 1)
        set_phase(solution, orbit, 0, phase)

    return solution
