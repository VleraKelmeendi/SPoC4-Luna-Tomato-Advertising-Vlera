# Luna Tomato Advertising – SpOC 4

## Project Overview

This project focuses on solving the **Luna Tomato Advertising (SpOC 4)** optimization challenge.

The main objective is to find an efficient spacecraft configuration that reproduces the target Morse code message:

**"TOMATOES FOR SALE"**

The solution uses different orbital configurations and spacecraft phase optimization to minimize the reconstruction error while satisfying the challenge constraints.

## Project Structure

```text
SpOC4-Luna-Tomato-Advertising/
│
├── data/
│   ├── db_dro.txt
│   ├── db_lyap.txt
│   └── db_axial.txt
│
├── src/
│   ├── lta_udp.py
│   ├── optimizer.py
│   ├── check_data.py
│   ├── test_optimizer.py
│   ├── experiments.py
│   ├── refine_solution.py
│   └── text.py
│
├── results/
│   └── best_solution.npy
│
├── verify_final.py
└── README.md
```

## Technologies Used

- Python 3.12
- NumPy
- heyoka.py
- Randomized Optimization
- Simulated Annealing

## Optimization Approach

The project includes several optimization techniques:

1. **Initial Solution Generation** – Creates an initial spacecraft configuration.
2. **Simulated Annealing** – Explores different configurations to search for improved solutions.
3. **Phase Optimization** – Adjusts spacecraft phases to reduce the reconstruction error.
4. **Orbit Optimization** – Tests alternative orbital configurations.
5. **Spacecraft Count Optimization** – Tests whether the number of spacecraft can be reduced while maintaining a feasible solution.

Candidate solutions are evaluated using the official challenge evaluator.

The final feasible solution was obtained through phase optimization and verified using the official challenge evaluator.

## Final Results

The best verified solution achieved the following results:

| Metric | Result |
|---|---:|
| Number of Spacecraft | 60 |
| Mean Squared Error (MSE) | 0.04907749 |
| Maximum Allowed MSE | 0.05 |
| Objective Value | 60 |
| Solution Status | Feasible |

The solution satisfies the required MSE threshold of 0.05. Since the MSE is below the maximum allowed value, the solution is considered feasible.

## Installation and Setup

Create a Conda environment with Python 3.12:

```bash
conda create -n luna python=3.12
```

Activate the environment:

```bash
conda activate luna
```

Install the required packages:

```bash
pip install numpy heyoka
```

## Running the Project

To run the optimization refinement script from the project root:

```bash
python src/refine_solution.py
```

**Note:** Running the refinement script may update the saved solution in the `results/` directory.

## Verifying the Final Solution

To verify the saved solution using the official challenge evaluator, run:

```bash
python verify_final.py
```

A successful verification should display output similar to:

```text
FINAL VERIFICATION
Objective: 60
Spacecraft: 60
MSE: 0.04907749077490775
SUCCESS: Solution is feasible!
```

## Final Solution

The final verified solution is stored in:

```text
results/best_solution.npy
```

This file contains the spacecraft configuration that achieved the verified result.

## Conclusion

The project successfully produced a feasible solution for the Luna Tomato Advertising (SpOC 4) challenge.

The final configuration uses **60 spacecraft** and achieves an **MSE of 0.04907749**, which is below the required threshold of 0.05.

The solution was verified using the official challenge evaluator.
