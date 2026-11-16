from optimizer import create_empty_solution, set_spacecraft

num_orbits = 779

solution = create_empty_solution(num_orbits)

# Vendosim 3 spacecraft ne orbiten 10
solution = set_spacecraft(solution, 10, 3)

# Vendosim 2 spacecraft ne orbiten 20
solution = set_spacecraft(solution, 20, 2)

print("Spacecraft in orbit 10:", solution[10])
print("Spacecraft in orbit 20:", solution[20])
print("Total selected spacecraft:", sum(solution[:num_orbits]))