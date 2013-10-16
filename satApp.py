#!/usr/bin/env python
import satGen
import simpleSat

if __name__ == "__main__":
    satGenerator = satGen.Generator()
#    satProblem = satGenerator.uniformRandom(3,10,3)
    satProblem = satGenerator.generate()
    solver = simpleSat.Solver()
    solution = solver.solve(satProblem)
    if solution:
        print("\nSolution: " + str(solution.solution))
    else:
        print("Unsat")
