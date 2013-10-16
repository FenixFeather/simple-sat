#!/usr/bin/env python
import satGen
import simpleSat

if __name__ == "__main__":
    satGenerator = satGen.Generator()
#    satProblem = satGenerator.uniformRandom(3,10,3)
    satProblem = satGenerator.generate()
#    satProblem = satGenerator.parseText(['c[10, -6, 1]', 'c[4, 3, 2]', 'c[-4, -5, 9]', 'c[9, 9, -4]', 'c[4, -4, -9]', 'c[-3, -10, -8]', 'c[7, 7, 4]', 'c[4, -9, 6]', 'c[7, 3, 1]', 'c[-2, -1, -10]', 'c[-7, 2, 5]', 'c[-8, 9, 10]'])
    solver = simpleSat.Solver()
    solution = solver.solve(satProblem)
    if solution:
        print("\nSolution: " + str(solution.solution))
    else:
        print("Unsat")
