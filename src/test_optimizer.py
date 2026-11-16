from optimizer import create_empty_solution

# Total number of orbits
num_orbits = 779

# Create an initial solution
solution = create_empty_solution(num_orbits)

# Check the solution
print("Number of selections:", len(solution[:num_orbits]))
print("Number of phases:", len(solution[num_orbits:]))
print("Total solution length:", len(solution))
print("Selected spacecraft:", sum(solution[:num_orbits]))
