#!/usr/bin/env python
from copy import deepcopy
import sys

class Sat():
    def __init__(self, clauseList):
        self.backups = []
        self.constraints = clauseList
        self.solution = []
        self.learnedClauses = []
        self.descriptive = ("-d" in sys.argv)
        
    def __str__(self):
        return str([str(clause) for clause in self.constraints])
        
    def __repr__(self):
        return repr([repr(clause) for clause in self.constraints])
        
    def propagate(self, unit):
        self.describe("{0}\nPropagating with {1}".format(self.getInfo(), str(unit)))
        literal = unit.literals[0]
        self.solution.append(unit)
        self.removeSatisfiedClauses(literal)
        for clause in self.constraints:
            while -literal in clause:
                clause.remove(-literal)
#            print("Testing " + str(clause) + str(len(clause)))
            if len(clause) == 0:      #Contradiction found
                if self.backtrack():  #Backtrack
                    return True       #Backtrack worked
                else:
                    return False      #Backtrack failed, unsat
        self.describe("Result:\n{0}\n".format(self.getInfo()))
        return True
        
    def removeSatisfiedClauses(self, literal):
        i = 0
        while i < len(self.constraints):
            if literal in self.constraints[i]:
                del self.constraints[i]
                continue
            i += 1
            
    def removeSatisfiedClausesInefficientButCool(self, literal):
        self.constraints = [clause for clause in self.constraints if literal not in clause]
        
    def branch(self, unit):
        self.solution.append(unit)
        self.propagate(unit)
        
    def getBranchUnit(self, sign=1):
#        unit = Clause([self.constraints[0].literals[0]*sign])
#        print("Branching on " + str(unit))
#        return unit
        return Clause([self.constraints[0].literals[0]*sign])
        
    def backup(self):
        self.backups.append(deepcopy(self))
        
    def backtrack(self):
        try:
#            print(self.backups)
            lastBackup = self.backups.pop()
            self.backups = lastBackup.backups
            self.constraints = deepcopy(lastBackup.constraints)
            self.solution = deepcopy(lastBackup.solution)
            self.describe("Backtracking...")
            self.propagate(self.getBranchUnit(-1))
            return True
        except IndexError:
            return False
            
    def getUnit(self):
        for clause in self.constraints:
            if clause.isUnit():
                self.describe((str(clause) + " is unit"))
                return clause
            else:
                return None
                
    def getUnitIndex(self):
        i = 0
        while i < len(self.constraints):
            if self.constraints[i].isUnit():
                return i
            else:
                i += 1
        return None
        
    def getSolution(self):
        return self.solution
        
    def __deepcopy__(self, memodict={}):
        result = Sat([deepcopy(clause) for clause in self.constraints])
        result.backups = [sat for sat in self.backups]
        result.solution = [deepcopy(clause) for clause in self.solution]
        return result
        
    def getInfo(self):
        return "Constraints: {0}\nSolution: {1}\nDepth: {2}".format(self.constraints,self.solution,len(self.backups))
        
    def describe(self, description):
        if self.descriptive:
            print(description)
        
class Clause():
    def __init__(self, literalList):
        self.literals = literalList
        
    def __repr__(self):
        return repr("c" + str(self.literals))
        
    def __str__(self):
        return str(self.literals)
        
    def __len__(self):
        return len(self.literals)
        
    def __contains__(self, literal):
        return (literal in self.literals)
        
    def __deepcopy__(self, memodict={}):
        return Clause(deepcopy(self.literals))
    
    def remove(self, literal):
        self.literals.remove(literal)
    
    def isUnit(self):
        return (len(set(self.literals)) == 1)
        
class Solver():
    def __init__(self):
        self.backtrackCounts = []
        self.times = []
        self.sats = 0
        self.n = 1
        
    def solve(self, sat):
        while True:
            if len(sat.constraints) == 0:
                return sat
            unit = sat.getUnit()
            if not unit:
                sat.backup()
                unit = sat.getBranchUnit()
            if not sat.propagate(unit):
                return None
                
