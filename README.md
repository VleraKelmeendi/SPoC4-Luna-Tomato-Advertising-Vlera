# Luna Tomato Advertising – SpOC 4

## Project Overview

This project focuses on solving the **Luna Tomato Advertising (SpOC 4)** optimization challenge.

The objective is to find an efficient spacecraft configuration that reproduces the target Morse code message:

**"TOMATOES FOR SALE"**

The solution uses orbital configurations and spacecraft phase optimization to minimize the reconstruction error while satisfying the challenge constraints.

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

The project uses several optimization techniques:

1. **Initial Solution Generation** – Creates an initial spacecraft configuration.
2. **Simulated Annealing** – Explores different configurations to improve the solution.
3. **Phase Optimization** – Adjusts spacecraft phases to reduce the reconstruction error.
4. **Orbit Optimization** – Tests alternative orbital configurations.
5. **Spacecraft Count Optimization** – Tests whether spacecraft can be added or removed while improving the objective.

The optimization process evaluates candidate solutions using the official challenge evaluator.

## Final Results

The best verified solution achieved the following results:

| Metric | Result |
|---|---:|
| Number of Spacecraft | 60 |
| Mean Squared Error (MSE) | 0.04907749 |
| Maximum Allowed MSE | 0.05 |
| Objective Value | 60 |
| Solution Status | Feasible |

The solution satisfies the required MSE threshold.

## Installation and Setup

Create and activate the Conda environment:

```bash
conda create -n luna python=3.12
conda activate luna
```

Install the required packages:

```bash
pip install numpy heyoka
```

## Running the Project

Run the optimization refinement script from the project root:

```bash
python src/refine_solution.py
```

## Verifying the Final Solution

To verify the saved solution using the official evaluator, run:

```bash
python verify_final.py
```

A successful verification should display:

```text
FINAL VERIFICATION
Objective: 60
Spacecraft: 60
MSE: 0.04907749077490775
SUCCESS: Solution is feasible!
```

## Final Note

The final solution is stored in:

```text
results/best_solution.npy
```

The solution was successfully verified against the challenge evaluator and achieved an MSE below the required threshold of 0.05.
