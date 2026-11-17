import numpy as np
import random
import math

# Maximum number of spacecraft per orbit
MAX_PER_ORBIT = 5

# Allowed phase range
PHASE_MIN = 0.0
PHASE_MAX = 2 * np.pi



def create_empty_solution(num_orbits):
    """Create an empty solution with all phases set to zero."""

    selections = np.zeros(num_orbits, dtype=int)
    phases = np.zeros(num_orbits * MAX_PER_ORBIT)

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

    counts = new_solution[:udp.num_orbits].astype(int)

    add_orbits = np.where(counts < MAX_PER_ORBIT)[0]
    remove_orbits = np.where(counts > 0)[0]

    promising_orbits = [
        155, 162, 184, 377, 399,
        402, 403, 404, 408, 409
    ]

    operation = random.choices(
        ["phase", "add", "remove"],
        weights=[40, 40, 20],
        k=1
    )[0]

    # 1. Ndryshojme fazen
    if operation == "phase" and len(remove_orbits) > 0:

        orbit = random.choice(remove_orbits)
        number = int(new_solution[orbit])
        spacecraft_index = random.randrange(number)

        phase_index = (
            udp.num_orbits
            + orbit * MAX_PER_ORBIT
            + spacecraft_index
        )

        old_phase = new_solution[phase_index]

        if random.random() < 0.5:
            change = random.uniform(-1.0, 1.0)
            new_phase = (old_phase + change) % PHASE_MAX
        else:
            new_phase = random.random() * PHASE_MAX

        new_solution[phase_index] = new_phase

    # 2. Shtojme spacecraft
    elif operation == "add" and len(add_orbits) > 0:

        available_promising = [
            orbit for orbit in promising_orbits
            if counts[orbit] < MAX_PER_ORBIT
        ]

        if available_promising and random.random() < 0.7:
            orbit = random.choice(available_promising)
        else:
            orbit = random.choice(add_orbits)

        number = int(new_solution[orbit])

        set_spacecraft(new_solution, orbit, number + 1)

        phase = random.random() * PHASE_MAX
        set_phase(new_solution, orbit, number, phase)

    # 3. Largojme spacecraft
    elif operation == "remove" and len(remove_orbits) > 0:

        orbit = random.choice(remove_orbits)
        number = int(new_solution[orbit])

        set_spacecraft(new_solution, orbit, number - 1)

    return new_solution



def simulated_annealing(
    udp,
    num_spacecraft=50,
    initial_temperature=5,
    cooling_rate=0.995,
    iterations=100,
    initial_solution=None
):
    if initial_solution is None:
        current_solution = create_seeded_solution(udp)
    else:
        current_solution = initial_solution.copy()

    best_solution = current_solution.copy()

    current_fitness = udp.fitness(
        current_solution, postprocess=True
    )[0][0]

    best_fitness = current_fitness

    temperature = initial_temperature

    print("SA starting fitness:", current_fitness)

    for i in range(iterations):

        neighbor = create_neighbor(current_solution, udp)

        neighbor_fitness = udp.fitness(
            neighbor, postprocess=True
        )[0][0]

        delta = neighbor_fitness - current_fitness

        if delta < 0:
            current_solution = neighbor
            current_fitness = neighbor_fitness

        elif temperature > 1e-12:
            probability = math.exp(
                -delta / temperature
            )

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




def improve_phases(udp, solution, trials=3):
    best_solution = solution.copy()

    best_fitness = udp.fitness(
        best_solution, postprocess=True
    )[0][0]

    active_orbits = np.where(
        best_solution[:udp.num_orbits] > 0
    )[0]

    steps = [0.02, 0.01, 0.005, 0.002]

    for orbit in active_orbits:
        count = int(best_solution[orbit])

        for spacecraft_index in range(count):
            phase_index = (
                udp.num_orbits
                + orbit * MAX_PER_ORBIT
                + spacecraft_index
            )

            for step in steps:
                for direction in [-1, 1]:
                    for _ in range(trials):
                        candidate = best_solution.copy()

                        change = direction * random.uniform(
                            step * 0.5, step
                        )

                        candidate[phase_index] = (
                            candidate[phase_index] + change
                        ) % PHASE_MAX

                        fitness = udp.fitness(
                            candidate, postprocess=True
                        )[0][0]

                        if fitness < best_fitness:
                            best_solution = candidate.copy()
                            best_fitness = fitness

    print("Improved phase fitness:", best_fitness)
    return best_solution


def improve_orbits(udp, solution, trials=5):
    best_solution = solution.copy()

    best_fitness = udp.fitness(
        best_solution, postprocess=True
    )[0][0]

    for _ in range(trials):
        counts = best_solution[:udp.num_orbits].astype(int)

        source_orbits = np.where(counts > 0)[0]
        target_orbits = np.where(counts < MAX_PER_ORBIT)[0]

        if len(source_orbits) == 0 or len(target_orbits) == 0:
            break

        source = random.choice(source_orbits)
        possible_targets = target_orbits[target_orbits != source]

        if len(possible_targets) == 0:
            continue

        target = random.choice(possible_targets)

        source_count = int(best_solution[source])
        source_index = random.randrange(source_count)

        source_phase_index = (
            udp.num_orbits + source * MAX_PER_ORBIT + source_index
        )

        candidate_base = best_solution.copy()

        phase = candidate_base[source_phase_index]

        last_index = source_count - 1
        last_phase_index = (
            udp.num_orbits + source * MAX_PER_ORBIT + last_index
        )

        if source_index != last_index:
            candidate_base[source_phase_index] = (
                candidate_base[last_phase_index]
            )

        candidate_base[last_phase_index] = 0.0
        candidate_base[source] -= 1

        target_count = int(candidate_base[target])

        target_phase_index = (
            udp.num_orbits + target * MAX_PER_ORBIT + target_count
        )

        candidate_base[target] += 1

        for _ in range(2):
            candidate = candidate_base.copy()

            candidate[target_phase_index] = random.uniform(
                PHASE_MIN, PHASE_MAX
            )

            fitness = udp.fitness(
                candidate, postprocess=True
            )[0][0]

            if fitness < best_fitness:
                best_solution = candidate.copy()
                best_fitness = fitness

    print("Improved orbit fitness:", best_fitness)
    return best_solution



def improve_spacecraft_count(udp, solution, trials=20):
    best_solution = solution.copy()

    best_fitness = udp.fitness(
        best_solution, postprocess=True
    )[0][0]

    for _ in range(trials):
        best_candidate = None
        candidate_fitness = best_fitness

        counts = best_solution[:udp.num_orbits].astype(int)

        # 1. Provojme shtimin e spacecraft
        available = np.where(counts < MAX_PER_ORBIT)[0]

        candidate_orbits = random.sample(
            list(available),
            min(5, len(available))
        )

        for orbit in candidate_orbits:
            candidate = best_solution.copy()

            number = int(candidate[orbit])
            candidate[orbit] += 1

            phase_index = (
                udp.num_orbits
                + orbit * MAX_PER_ORBIT
                + number
            )

            candidate[phase_index] = random.uniform(
                PHASE_MIN, PHASE_MAX
            )

            fitness = udp.fitness(
                candidate, postprocess=True
            )[0][0]

            if fitness < candidate_fitness:
                best_candidate = candidate.copy()
                candidate_fitness = fitness

        # 2. Provojme largimin e spacecraft
        selected = np.where(counts > 0)[0]

        candidate_orbits = random.sample(
            list(selected),
            min(5, len(selected))
        )

        for orbit in candidate_orbits:
            number = int(best_solution[orbit])

            for spacecraft_index in range(number):
                candidate = best_solution.copy()

                phase_index = (
                    udp.num_orbits
                    + orbit * MAX_PER_ORBIT
                    + spacecraft_index
                )

                last_index = number - 1

                last_phase_index = (
                    udp.num_orbits
                    + orbit * MAX_PER_ORBIT
                    + last_index
                )

                if spacecraft_index != last_index:
                    candidate[phase_index] = (
                        candidate[last_phase_index]
                    )

                candidate[last_phase_index] = 0.0
                candidate[orbit] -= 1

                fitness = udp.fitness(
                    candidate, postprocess=True
                )[0][0]

                if fitness < candidate_fitness:
                    best_candidate = candidate.copy()
                    candidate_fitness = fitness

        # 3. E ruajme ndryshimin me te mire
        if best_candidate is None:
            break

        best_solution = best_candidate.copy()
        best_fitness = candidate_fitness

    print("Spacecraft optimization fitness:", best_fitness)

    return best_solution
